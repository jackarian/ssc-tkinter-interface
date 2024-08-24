from picamera2.picamera2 import Picamera2, Preview
from libcamera import ColorSpace
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(colour_space=ColorSpace.Sycc())
