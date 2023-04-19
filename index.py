import sys
import time
import cv2
import keyboard
import numpy as np
import pyautogui
from PIL import ImageGrab

height = 1920
width = 1080

chat_start_x = 468
chat_start_y = 622
chat_end_x = 738
chat_end_y = 644

fishing_rod_x = 1200
fishing_rod_y = 905

__timer = time.time()
__total_runs = 0


def detected_up(image):
    lower = np.array([255, 204, 0], dtype="uint8")
    upper = np.array([255, 204, 0], dtype="uint8")

    return apply_mask(image, lower, upper)


def detected_down(image):
    lower = np.array([0, 255, 0], dtype="uint8")
    upper = np.array([0, 255, 0], dtype="uint8")

    return apply_mask(image, lower, upper)


def apply_mask(image, lower, upper):
    mask = cv2.inRange(image, lower, upper)
    pixels = cv2.countNonZero(mask)

    return pixels


def catch():
    global __timer
    global __total_runs
    time.sleep(5)

    keyboard.press('f1')

    pyautogui.moveTo(fishing_rod_x, fishing_rod_y)
    pyautogui.click(fishing_rod_x, fishing_rod_y)

    clicks = 0
    start = time.time()

    while True:
        if clicks > 0 and time.time() - __timer >= 5:
            __timer = time.time()
            __total_runs += 1
            print('Run is over')
            print(f'Total runs: {__total_runs}')
            print('Reloading...')
            break
        if time.time() - __timer >= 60 * 5:
            print('Exiting by time...')
            sys.exit(0)
        if time.time() - start >= 5:
            print('Reloading...')
            break

        image = np.array(ImageGrab.grab(bbox=(chat_start_x, chat_start_y, chat_end_x, chat_end_y)))

        if detected_up(image) == 548:
            pyautogui.press('up')
            __timer = time.time()
            start = time.time()
            clicks += 1
            continue
        if detected_down(image) == 676:
            pyautogui.press('down')
            __timer = time.time()
            start = time.time()
            clicks += 1
            continue
    catch()


def main():
    print('Starting...')
    pyautogui.moveTo(height / 2, width / 2)
    pyautogui.click(height / 2, width / 2)
    catch()


if __name__ == '__main__':
    main()
