import time
from picamera2 import Picamera2, Preview
from datetime import datetime

def capture_images(interval=5, duration=60):
    picam2 = Picamera2()
    config = picam2.create_still_configuration(main={"size": (4608, 2592)})
    picam2.configure(config)
    picam2.start()

    start_time = time.time()

    try:
        while time.time() - start_time < duration:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            image_path = f'image_{timestamp}.jpg'
            picam2.capture_file(image_path)
            print(f'Captured {image_path}')
            time.sleep(interval)
    finally:
        picam2.stop()

if __name__ == '__main__':
    capture_images(interval=5, duration=60)