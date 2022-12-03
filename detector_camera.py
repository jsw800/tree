import cv2
from websocket import create_connection
from PIL import Image
import time
import sys
import os
import threading

"""
    This file runs on a machine with an onboard camera.
    It connects to the server (detector_server.py) running on the raspberry pi and sends
    messages to the server so that it iteratively turns on each successive light,
    captures an image of the scene with that light on and saves the image to the directory
    supplied as the first arg of the program.

    Before the program begins capturing images, there is a calibration step where a camera window
    opens and allows you to verify the camera is pointing at the tree correctly. When you are ready
    to begin capturing images, focus the camera window and press "q" and the process will begin

    Example usage:
    # position the camera facing the tree in front
    python camera.py x
    # calibrate the camera and press q to start

    # then position the camera facing the tree from the right side
    python camera.py y
    # calibrate the camera and press q to start
    
    # then position the camera facing the tree from behind
    python camera.py x_reverse
    
    # then position the camera facing the tree from the left side
    python camera.py y_reverse

    After this process, the images for each LED will be in the
    images/x, images/y, images/x_reverse, and images/y_reverse directories.
"""


def calibrate(cam):
    while True:
        ret, frame = cam.read()

        cv2.imshow('frame', frame)

        # q to break out of calibration step
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


def save_image(image, index, direction):
    os.system('rm ' + 'images/' + direction + '/' + str(index) + '.png 2> /dev/null')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(image)
    im.save('images/' + direction + '/' + str(index) + '.png')


def capture_image(cam, index):
    result, image = cam.read()

    if result:
        thread = threading.Thread(target=save_image, args=(image, index, sys.argv[1]))
        thread.start()


def main():
    cam = cv2.VideoCapture(0)

    calibrate(cam)

    ws = create_connection('ws://10.0.0.50:8765')
    for i in range(100):
        ws.send(str(i))
        time.sleep(0.2)
        capture_image(cam, i)

    ws.close()

    ws = create_connection('ws://10.0.0.50:8765')
    for i in range(100, 200):
        ws.send(str(i))
        time.sleep(0.2)
        capture_image(cam, i)

    ws.close()
  
    cam.release()


if __name__ == "__main__":
    main()
