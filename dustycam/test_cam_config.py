import sys
import time
import cv2
import numpy as np
import logging
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QPushButton, QCheckBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QPalette
from picamera2 import Picamera2, controls
from picamera2.previews.qt import QGlPicamera2

# Configure logging
logging.basicConfig(filename='output.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class CameraControlApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.picam2 = Picamera2()
        self.setup_camera()

        # Set up a timer to update the image display
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)  # Update every 100 ms

        self.picam2.post_callback = self.request_callback

    def initUI(self):
        self.setWindowTitle('Lens Position Control')

        self.layout = QVBoxLayout()

        self.lens_position_label = QLabel('Lens Position: 0.0', self)
        self.layout.addWidget(self.lens_position_label)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)  # Scale factor of 10 for 0.0 to 10.0 with 0.1 increments
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.update_lens_position)

        self.layout.addWidget(self.slider)

        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)

        self.metadata_label = QLabel(self)
        self.metadata_label.setFixedWidth(400)
        self.metadata_label.setAlignment(Qt.AlignTop)
        self.layout.addWidget(self.metadata_label)

        self.setLayout(self.layout)

    def setup_camera(self):
        camera_config = self.picam2.create_preview_configuration()
        self.picam2.configure(camera_config)
        self.picam2.start()

        # Give the camera some time to adjust
        time.sleep(2)

        # Retrieve initial lens position
        self.update_lens_position_label()

    def update_lens_position(self, value):
        lens_position = value / 10.0  # Scale back to 0.0 to 10.0 range
        self.picam2.set_controls({'LensPosition': lens_position})
        self.update_lens_position_label()

    def update_lens_position_label(self):
        metadata = self.picam2.capture_metadata()
        lens_position = metadata.get('LensPosition', 0.0)
        self.lens_position_label.setText(f'Lens Position: {lens_position:.1f}')
        logging.info(f'Lens Position: {lens_position}')

    def update_frame(self):
        frame = self.picam2.capture_array()

        # Log frame shape and type for debugging
        logging.info(f'Frame shape: {frame.shape}, Frame dtype: {frame.dtype}')

        # Determine the format and convert accordingly
        if frame.shape[2] == 3:  # Assume YUV420 format
            try:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_YUV2RGB_I420)
            except cv2.error as e:
                logging.error(f'Error converting YUV to RGB: {e}')
                return
        elif frame.shape[2] == 4:  # Assume RGBA format
            try:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
            except cv2.error as e:
                logging.error(f'Error converting BGRA to RGB: {e}')
                return
        else:
            logging.error(f'Unexpected number of channels: {frame.shape[2]}')
            return
        
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(image))

    def request_callback(self, request):
        metadata = request.get_metadata()
        self.metadata_label.setText(''.join(f"{k}: {v}\n" for k, v in metadata.items()))

    def closeEvent(self, event):
        self.picam2.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CameraControlApp()
    ex.show()
    sys.exit(app.exec_())
