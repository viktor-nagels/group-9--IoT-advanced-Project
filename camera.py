from picamera import PiCamera
from time import sleep

camera = PiCamera()
# TODO deze rotatie kan nog aangepast worden A.D.H.V. hoe de camera geposisioneert staat
camera.rotation = 180

camera.start_preview()
sleep(2)
camera.capture('/home/pi/images/photo.jpg')  # TODO make location for the pictures
camera.stop_preview()
