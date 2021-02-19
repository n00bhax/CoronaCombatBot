from PIL import ImageGrab
import time
import pyautogui
from PIL import Image
import numpy as np
import cv2
import threading

gameSize = 778
speed = 335 # pixels per second
direction = 'stay'
bullets = None
frame = Image.open("./aGameWindow.png")

def getEnemiesLocation(frame: Image):

    im = cv2.cvtColor(np.asarray(frame), cv2.COLOR_RGB2HSV)
    crop_im = im[49:gameSize - 130, 0: gameSize]
    mask = cv2.inRange(crop_im, np.array([0, 100, 30]), np.array([50, 255, 200]))

    mask = cv2.erode(mask, None, iterations=1)

    cv2.imshow('enemies', mask)
    cv2.waitKey(1)

    if len(np.argwhere(mask == 255)[:, 1]) > 0:
        return np.unique(np.argwhere(mask == 255)[:, 1])


def getBulletLocation():

    global bullets
    global frame


    im = cv2.cvtColor(np.asarray(frame), cv2.COLOR_RGB2HSV)
    crop_im = im[49:gameSize-10, 0: gameSize]
    mask = cv2.inRange(crop_im, np.array([14, 90, 210]), np.array([36, 255, 255]))

    #Image.fromarray(mask).show()
    #res = cv2.bitwise_and(im,im,mask= mask)
    #Image.fromarray(res).show()

    mask = cv2.erode(mask, None, iterations=1)

    cv2.imshow('bullets', mask)
    cv2.waitKey(0)

    if len(np.argwhere(mask == 255)[:, 1]) > 0:
        bullets = np.unique(np.argwhere(mask == 255)[:, 1])


def getPlayerLocation(frame: Image):

    im = np.asarray(frame)

    crop_im = im[gameSize-130:gameSize, 0: gameSize]

    mask = cv2.inRange(crop_im, np.array([110, 170, 170]), np.array([130, 180, 190]))

    cv2.imshow('player', mask)
    cv2.waitKey(1)

    if len(np.argwhere(mask == 255)) > 0:
        return np.argwhere(mask == 255)[0][1]


def isInDanger(bullets, location):

    if bullets is not None:
        for b in bullets:
            if location - 40 < b < location + 40:
                print("DANGER")
                return True

    return False


def willHitEnemy(enemies, location):

    if enemies is not None:
        for e in enemies:
            if location - 5 < e < location + 5:
                return True
        return False
    return True


def screenGrab():

    global frame

    while True:
        box = (4428, 1230, 5206, 2008)
        frame = ImageGrab.grab(box, False, True).convert('RGB')
        time.sleep(1/30)


def move():

    global direction

    while True:
        d = direction
        if d != 'stay':
            pyautogui.keyDown(d)
            time.sleep(0.1)
            pyautogui.keyUp(d)


def think():

    global direction
    global bullets
    global frame

    while True:

        #frame = screenGrab()
        #frame = Image.open("./aGameWindow2.png")

        location = getPlayerLocation(frame)

        if location is not None:

            bullets_current = bullets

            if isInDanger(bullets_current, location):

                bullets_on_right = location < bullets_current
                if sum(bullets_on_right) > len(bullets_current)/2:
                    direction = 'left'
                else:
                    direction = 'right'

                print("EVADING")

            else:

                enemies = getEnemiesLocation(frame)

                if willHitEnemy(enemies, location):

                    direction = 'stay'

                else:

                    if location < min(enemies): #laat dit afhangen van de richting waarin de enemies bewegen
                        key = 'right'
                        location += 50
                    else:
                        key = 'left'
                        location -= 50

                    if not isInDanger(bullets_current, location):
                        direction = key
        else:
            direction = 'stay'

        #print(direction)


def main():

    t = threading.Thread(target=move)
    t1 = threading.Thread(target=think)
    frame_thread = threading.Thread(target=screenGrab)
    bullets_thread = threading.Thread(target=getBulletLocation)

    t.start()
    t1.start()
    frame_thread.start()
    bullets_thread.start()

    t.join()


if __name__ == '__main__':
    main()