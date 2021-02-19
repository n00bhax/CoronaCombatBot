from PIL import ImageGrab
import os
import time
import pyautogui

def screenGrab():

    time.sleep(1)

    box = (4428, 1230, 5206, 2008)
    im = ImageGrab.grab(box, False, True)
    im.save(os.getcwd() + '\\before.png', 'PNG')

    pyautogui.keyDown('right')
    time.sleep(0.2)
    pyautogui.keyUp('right')

    box = (4428, 1230, 5206, 2008)
    im = ImageGrab.grab(box, False, True)
    im.save(os.getcwd() + '\\after.png', 'PNG')

# 67 pixels in 0.2 seconds
# -> 335 pixels per seconds

def main():
    screenGrab()


if __name__ == '__main__':
    main()