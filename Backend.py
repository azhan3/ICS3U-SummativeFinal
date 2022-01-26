import cv2 as cv
import time
import BackendClasses
import tkinter as tk
from tkinter import *
import config
from PIL import Image, ImageTk
from config import mouse, Button
import numpy as np
from TextRecog import ocr_core

CamWidth, CamHeight = 1920, 1080

detector = BackendClasses.HandControl()
MouseMovement = BackendClasses.MouseMovement()


def a():
    pass


# Main Window
class MainWindow:
    def __init__(self, window, cap):
        for i in config.GestureDict:
            print(config.GestureDict[i])
        self.Dictionary = {"Move Mouse": detector.MoveMouse,
                           "Left Click": MouseMovement.MouseSingleClickLeft,
                           "Right Click": MouseMovement.MouseSingleClickRight,
                           "Volume Slider": lambda: detector.CheckLevel(config.VolumeUp, config.VolumeDown),
                           "No Action": self.NoAction,
                           "Pause Action": lambda: MouseMovement.Pause(self.img2),
                           "Drag Mouse": detector.HoldMouse,
                           "Mouse Scroll": lambda: detector.CheckLevel(config.ScrollUp, config.ScrollDown),
                           "Swipe": lambda: detector.RecordSwipe(self.img2, self.ExecutedFunction),
                           "Draw": detector.Draw,
                           "DrawUp": detector.DrawUp,
                           "Clear Drawing": detector.ClearDrawings
                           }
        self.MouseDict = {"Open Palm": self.Dictionary[config.GestureDict["OpenPalm"]],
                          "Fist": self.Dictionary[config.GestureDict["Fist"]],
                          "Index Finger": self.Dictionary[config.GestureDict["IndexFinger"]],
                          "Swipe Action": self.Dictionary[config.GestureDict["SwipeAction"]],
                          "No Action": self.NoAction,
                          "Spider-Man": self.Dictionary[config.GestureDict["SpiderMan"]],
                          "OK": self.Dictionary[config.GestureDict["OK"]],
                          "Telephone": self.Dictionary[config.GestureDict["Telephone"]]
                          }

        """self.MouseDict = {"Open Palm": detector.MoveMouse, "Fist": h, "Index Finger": lambda: detector.Draw(self.img2)#MouseMovement.MouseSingleClickLeft
            , "Swipe Action": lambda: detector.RecordSwipe(self.img2, self.ExecutedFunction), "No Action": h, "Spider-Man": lambda: detector.CheckLevel(config.VolumeUp, config.VolumeDown), "OK": lambda: MouseMovement.Pause(self.img2), "Telephone": detector.HoldMouse}"""

        self.wScr, self.hScr = 1920.0, 1080.0
        self.Time = None
        self.cap = cap
        self.cap.set(3, 1920)
        self.cap.set(4, 1080)
        self.p = "No Action"
        self.window = window
        self.interval = 20
        self.canvas_dot = None
        self.canvas_line_X = None
        self.canvas_line_Y = None
        self.PreviousAction = "No Action"
        self.PreviouPrevioussAction = "No Action"
        self.ShowHands = True
        self.x1 = 640
        self.y1 = 360
        self.ShowHandsDict = {True: self.Image, False: self.NotImage}
        btn = tk.Button(self.window, text='Switch View', width=40,
                        height=3, relief=RIDGE, bd='5', command=self.ChangeView)
        btn.place(x=1280, y=0)

        self.update_image()

    def NoAction(self):
        mouse.release(Button.left)
        config.OKTime = None

    def update_image(self):
        self.canvas = Canvas(self.window, width=1280, height=720, bg="black")
        self.canvas.grid(row=0, column=0)
        success, img = self.cap.read()
        img = detector.Landmarks(img)
        lmList = detector.findLm(img)
        self.img2 = cv.flip(img, 1)
        self.img2 = cv.cvtColor(self.img2, cv.COLOR_BGR2RGB)
        self.ExecutedFunction = "No Action"
        if lmList is not None:
            self.x1, self.y1 = detector.NewLoc(self.wScr, self.hScr)
            self.PreviouPrevioussAction = self.PreviousAction
            self.PreviousAction = self.p
            self.p = detector.CheckAction(self.img2, MouseMovement.PauseOrNot)
            if self.p == self.PreviousAction == self.PreviouPrevioussAction:
                self.ExecutedFunction = self.p
            else:
                self.ExecutedFunction = self.PreviouPrevioussAction
            if not MouseMovement.PauseOrNot:
                # self.MouseDict["Swipe Action"]()
                self.MouseDict[self.ExecutedFunction]()
            elif MouseMovement.PauseOrNot and self.ExecutedFunction == "OK":
                self.MouseDict[self.ExecutedFunction]()
            else:
                config.OKTime = None

            detector.ChangeLoc()
        if MouseMovement.PauseOrNot is False:
            cv.putText(self.img2, self.ExecutedFunction, (10, 450), cv.FONT_HERSHEY_DUPLEX, 3, (0, 255, 0), 2,
                       cv.LINE_AA)
        else:
            cv.putText(self.img2, "Paused", (10, 450), cv.FONT_HERSHEY_DUPLEX, 3, (0, 255, 0), 2, cv.LINE_AA)
        if time.time() - config.SwipeTime < 2:
            cv.putText(self.img2, str(round(time.time() - config.SwipeTime, 1)), (10, 100), cv.FONT_HERSHEY_DUPLEX, 3,
                       (0, 255, 0),
                       2, cv.LINE_AA)
        self.canvas.delete()
        self.ShowHandsDict[self.ShowHands]()
        self.window.after(self.interval, self.update_image)

    def ChangeView(self):
        self.ShowHands = not self.ShowHands

    def Image(self):

        grayImage = cv.cvtColor(self.img2, cv.COLOR_BGR2GRAY)
        (thresh, self.blackAndWhiteImage) = cv.threshold(grayImage, 255, 255, cv.THRESH_BINARY)
        detector.DrawLetter(self.blackAndWhiteImage)
        if self.ExecutedFunction == "OK":
            cv.imwrite(r"C:\Users\alexz\Downloads\helloa.jpg", self.blackAndWhiteImage)
            print([self.blackAndWhiteImage])
            print(ocr_core(r"C:\Users\alexz\Downloads\helloa.jpg"))
        cv.circle(self.blackAndWhiteImage, (1280 - self.x1 + 20, self.y1), 5, (255, 255, 255), -1)
        self.image = Image.fromarray(self.blackAndWhiteImage)
        self.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=NW, image=self.image)

    def NotImage(self):
        self.canvas_line_X = self.canvas.create_line(1280 - self.x1, 720, 1280 - self.x1, 0, fill="white", width=5)
        self.canvas_line_Y = self.canvas.create_line(0, self.y1, 1280, self.y1, fill="white", width=5)
        self.canvas_dot = self.canvas.create_oval(1280 - self.x1 + 10, self.y1 + 10, 1280 - self.x1 - 10,
                                                  self.y1 - 10,
                                                  fill="red")


def Start():
    root = Tk()
    root.geometry('1590x720')
    root.maxsize(1590, 720)
    MainWindow(root, cv.VideoCapture(0))
    root.mainloop()


if __name__ == "__main__":
    Start()

"""if __name__ == "__main__":
    main()"""
