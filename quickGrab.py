from PIL import ImageGrab
import os
import time


def screenGrab():
    box = (4428, 1230, 5206, 2008)
    im = ImageGrab.grab(box, False, True)
    im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) +
            '.png', 'PNG')


def main():
    screenGrab()


if __name__ == '__main__':
    main()