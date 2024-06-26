import os
import cv2
import time
import datetime
from picamera2 import Picamera2, Preview
import libcamera

from dustycam import config

from logging import basicConfig, getLogger, INFO
basicConfig(level=INFO)
logger = getLogger(__name__)

def detect_motion(picam2, low_res_config, high_res_config, action):
    # Initialize the camera with low resolution configuration
    picam2.configure(low_res_config)
    #picam2.controls.set_controls( { "AfMode" : libcamera.controls.AfModeEnum.Continuous, "AfMetering" : libcamera.controls.AfMeteringEnum.Windows,  "AfWindows" : [ (768,432,1536,864) ] } )

    picam2.start()

    # Capture the first frame
    frame1 = picam2.capture_array()
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
    gray1 = cv2.GaussianBlur(gray1, (31, 31), 0)

    current_config = picam2.camera_controls
    # Print out the current configuration
    logger.info("Current lowres Camera Configuration:")
    current_controls = picam2.controls
    logger.info(f"Current lowres Camera 'controls': {current_controls}")


    while True:
        # Capture the next frame
        frame2 = picam2.capture_array()
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
        gray2 = cv2.GaussianBlur(gray2, (31, 31), 0)

        # Compute the absolute difference between the current frame and the first frame
        diff = cv2.absdiff(gray1, gray2)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        # Find contours of the moving objects
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # If motion is detected, trigger the action
        if contours:
            action(picam2, high_res_config, low_res_config)

        # Update the first frame to the current frame
        gray1 = gray2

        # Optional: Display the frame with contours for debugging
        #cv2.drawContours(frame2, contours, -1, (0, 255, 0), 2)
        #cv2.imshow('Motion Detection', frame2)

        # Exit if 'q' is pressed
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

        time.sleep(.2)

    picam2.stop()
    cv2.destroyAllWindows()

def take_high_res_images(picam2, high_res_config, low_res_config, num_images=3):
    print("Motion detected! Taking high-resolution images...")
    
    # Switch to high resolution mode once before capturing images
    picam2.switch_mode(high_res_config)
    
    for i in range(num_images):
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        image_path = os.path.join(images_folder_path, f'image_{timestamp}_{i+1}.jpg')
        
        #TODO: Try writing exif data to the image using picam2.capture_file(image_path, exif_data)
        picam2.capture_file(image_path)
        
        # Print controls of picam2 
        logger.info(f"-Camera 'controls' after taking high resolution image {i+1}: {picam2.preview_configuration.controls}")
        current_config = picam2.camera_controls
        
        # Print out the current configuration
        print(f"Current Camera Configuration after image {i+1}:")
        for control, value in current_config.items():
            print(f"{control}: {value}")
        
        print(f"High-resolution image {i+1} saved as {image_path}")

    # Switch back to low resolution mode
    picam2.switch_mode(low_res_config)




# Initialize Picamera2
picam2 = Picamera2()

#make directory in home folder to save images
import os 
folder_name = "dustycam_images"
images_folder_path = os.path.expanduser(f'~/{folder_name}')
os.makedirs(images_folder_path, exist_ok=True)
print(f"Images will be saved in {os.path.expanduser(f'~/{folder_name}')}")

# Configure low resolution for motion detection
low_res_config = picam2.preview_configuration
low_res_config.main.size = (320, 240)
#low_res_config.main.format = "RGB888"
low_res_config.controls.FrameRate = 30
#low_res_config.controls.AfMode = libcamera.controls.AfModeEnum.Manual
#low_res_config.controls.LensPosition = 0.0

#low_res.controls.set_controls( { "AfMode" : libcamera.controls.AfModeEnum.Continuous, "AfMetering" : libcamera.controls.AfMeteringEnum.Windows,  "AfWindows" : [ (768,432,1536,864) ] } )
logger.info(f"Camera 'controls' before start recording: {low_res_config.controls}")

# Configure high resolution for capturing images
high_res_config = picam2.still_configuration
high_res_config.main.size = (4056, 3040)  # Adjust the resolution as needed
#high_res_config.main.format = "RGB888"
#high_res_config.controls.AfMode = libcamera.controls.AfModeEnum.Manual
#high_res_config.controls.LensPosition = 0.0

# Start motion detection
detect_motion(picam2, low_res_config, high_res_config, take_high_res_images)

logger.warn("TEST")
