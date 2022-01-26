import time
import cv2 as cv
import numpy as np
import math
import pyautogui
import config

class Write:
    def __init__(self):
        self.clocX = None
        self.clocY = None
        self.DrawPause = False
        self.cIndexFingerLocX = None
        self.cIndexFingerLocY = None
        self.size = 5
        self.Array = []
        self.BigArray = []
    def Draw(self):
        self.DrawPause = False
        self.Array.append((1280 - self.clocX, self.clocY))


        #cv.putText(img, "Swipe", (10, 250), cv.FONT_HERSHEY_DUPLEX, 3, (0, 255, 0), 2, cv.LINE_AA)