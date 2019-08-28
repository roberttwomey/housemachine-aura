
import time
import picamera


# from here: 
#   https://www.raspberrypi.org/forums/viewtopic.php?f=43&t=82691&start=25

frames = 10

def filenames():
    frame = 0
    while frame < frames:
        yield 'image%02d.jpg' % frame
        frame += 1

with picamera.PiCamera() as camera:
    camera.resolution = (2592,1944)
    camera.framerate = 30
    camera.start_preview()
    # Give the camera some warm-up time
    time.sleep(2)
    start = time.time()
    camera.capture_sequence(filenames(), use_video_port=True)
    finish = time.time()
print('Captured %d frames at %.2ffps' % (
    frames,
    frames / (finish - start)))