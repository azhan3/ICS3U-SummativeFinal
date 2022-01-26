import tkinter as tk
from tkinter import *
from Backend import Start
import pymongo
import dns
import re

import config
from storage import apiURI
import keyboard
from tkinter import ttk

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

client = pymongo.MongoClient(apiURI)
dbname = "CompSci"
db = client[dbname]
collection = db["login"]
collectionGestures = db["Gestures"]


def CreateLabel(x, y, canvas, text, page, textColor):
    label = Label(page, text=text, borderwidth=0, bg="white")
    label.config(highlightbackground=textColor, font=("Rockwell", 10), foreground=textColor)
    canvas.create_window(x, y, window=label)
    return label


class Register:
    def __init__(self):
        self.page = tk.Toplevel()
        self.RegistrationPage = Frame(self.page)
        self.width = 480
        self.height = 650
        self.bg = PhotoImage(file="bg2.png")
        self.RegistrationPage.pack(fill=BOTH, expand=YES)
        self.NameVar = StringVar()
        self.UsernameVar = StringVar()
        self.PasswordVar = StringVar()
        self.EmailVar = StringVar()
        self.ConfirmBtn = None
        self.ValidName = False
        self.ValidUsername = False
        self.ValidPassword = False
        self.ValidEmail = False
        self.NameVar.trace("w", lambda name, index, mode, sv=self.NameVar: self.NameTrack())
        self.UsernameVar.trace("w", lambda name, index, mode, sv=self.UsernameVar: self.UsernameTrack())
        self.PasswordVar.trace("w", lambda name, index, mode, sv=self.PasswordVar: self.PasswordTrack())
        self.EmailVar.trace("w", lambda name, index, mode, sv=self.EmailVar: self.EmailTrack())

        self.canvas = ResizingCanvas(self.RegistrationPage, width=self.width, height=self.height, bg="red",
                                     highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=YES)
        self.canvas.create_image(self.width / 2, self.height / 2, image=self.bg)
        self.canvas.create_rectangle(self.width / 8, self.height / 8, self.width / 8 * 7, self.height - self.height / 8,
                                     fill="white")
        self.canvas.addtag_all("all")
        self.page.title("Register")
        self.Labels()
        self.Buttons()
        self.NameLabel = CreateLabel(self.width / 2, self.height / (self.height / 230), self.canvas,
                                     "",
                                     self.RegistrationPage,
                                     "green")
        self.UsernameLabel = CreateLabel(self.width / 2, self.height / (self.height / 293), self.canvas,
                                         "",
                                         self.RegistrationPage,
                                         "green")
        self.PasswordLabel = CreateLabel(self.width / 2, self.height / (self.height / 355), self.canvas,
                                         "",
                                         self.RegistrationPage,
                                         "green")
        self.EmailLabel = CreateLabel(self.width / 2, self.height / (self.height / 420), self.canvas,
                                      "",
                                      self.RegistrationPage,
                                      "green")
        self.SubmitLabel = CreateLabel(self.width / 2, self.height / (self.height / 475), self.canvas,
                                       "",
                                       self.RegistrationPage,
                                       "red")

        self.RegistrationPage.mainloop()

    def Labels(self):
        NameLabel = Label(self.RegistrationPage, text="Name", bg="white", font=("Rockwell", 12))
        self.canvas.create_window(self.width / 4, self.height / 3.25, window=NameLabel)
        NameEntry = Entry(self.RegistrationPage, textvariable=self.NameVar, width=int(self.width / (self.width / 35)),
                          bd=1,
                          relief="solid",
                          bg="#DEDEDE",
                          font=("roboto", 15))
        self.canvas.create_window(self.width / 1.7, self.height / 3.25, width=self.width / 2, window=NameEntry)

        UsernameLabel = Label(self.RegistrationPage, text="Username", bg="white", font=("Rockwell", 12))
        self.canvas.create_window(self.width / 4, self.height / 2.45, window=UsernameLabel)

        UsernameEntry = Entry(self.RegistrationPage, textvariable=self.UsernameVar,
                              width=int(self.width / (self.width / 35)),
                              bd=1,
                              relief="solid",
                              bg="#DEDEDE",
                              font=("roboto", 15))
        self.canvas.create_window(self.width / 1.7, self.height / 2.45, width=self.width / 2, window=UsernameEntry)

        PasswordLabel = Label(self.RegistrationPage, text="Password", bg="white", font=("Rockwell", 12))
        self.canvas.create_window(self.width / 4, self.height / 1.98, window=PasswordLabel)

        PasswordEntry = Entry(self.RegistrationPage, textvariable=self.PasswordVar, show="*",
                              width=int(self.width / (self.width / 35)),
                              bd=1,
                              relief="solid",
                              bg="#DEDEDE",
                              font=("roboto", 15))
        self.canvas.create_window(self.width / 1.7, self.height / 1.98, width=self.width / 2, window=PasswordEntry)

        EmailLabel = Label(self.RegistrationPage, text="Email", bg="white", font=("Rockwell", 12))
        self.canvas.create_window(self.width / 4, self.height / 1.66, window=EmailLabel)

        EmailEntry = Entry(self.RegistrationPage, textvariable=self.EmailVar, width=int(self.width / (self.width / 35)),
                           bd=1,
                           relief="solid",
                           bg="#DEDEDE",
                           font=("roboto", 15))
        self.canvas.create_window(self.width / 1.7, self.height / 1.66, width=self.width / 2, window=EmailEntry)

        RegistrationLabel = Label(self.RegistrationPage, text='Registration', bg="white", font=("Rockwell", 20))
        self.canvas.create_window(self.width / 2, self.height / 5.5, window=RegistrationLabel)

    def Buttons(self):
        self.ConfirmBtn = Button(self.RegistrationPage, text="Sign Up", bg='#8B8B8B', command=self.SubmitRegistration,
                                 font=("roboto", 10))
        self.canvas.create_window(self.width / 2, self.height / 1.45, width=self.width / 4, window=self.ConfirmBtn)

    def SubmitRegistration(self):
        if all(v is True for v in [self.ValidName, self.ValidUsername, self.ValidPassword, self.ValidEmail]):
            collection.insert_one(
                {"username": self.UsernameVar.get(), "email": self.EmailVar.get(), "password": self.PasswordVar.get(),
                 "name": self.NameVar.get()})
            collectionGestures.insert_one(
                {"username": self.UsernameVar.get(), f"{self.UsernameVar.get()}OpenPalm": "Move Mouse",
                 f"{self.UsernameVar.get()}Fist": "No Action", f"{self.UsernameVar.get()}IndexFinger": "Left Click",
                 f"{self.UsernameVar.get()}SwipeAction": "Swipe", f"{self.UsernameVar.get()}SpiderMan": "Volume Slider",
                 f"{self.UsernameVar.get()}OK": "Pause Action", f"{self.UsernameVar.get()}Telephone": "Drag Mouse"})
            self.ConfirmBtn["state"] = "disabled"
            self.page.destroy()
        else:
            self.SubmitLabel.config(text="Invalid Information")

    def NameTrack(self):
        Name = self.NameVar.get()
        if len(Name.strip()) == 0:
            self.NameLabel.config(text="Name must be 1 or more characters", fg="red")
            self.ValidName = False
        else:
            self.NameLabel.config(text="Name is Good!", fg="green")
            self.ValidName = True

    def UsernameTrack(self):
        Username = self.UsernameVar.get()
        if len(Username.strip()) < 4:
            self.UsernameLabel.config(text="Username must be longer than 3 characters", fg="red")
            self.ValidUsername = False
        elif collection.find_one({"username": Username}):
            self.UsernameLabel.config(text="Username is Already Taken", fg="red")
            self.ValidUsername = False
        else:
            self.UsernameLabel.config(text="Username is Good!", fg="green")
            self.ValidUsername = True

    def PasswordTrack(self):
        Password = self.PasswordVar.get()
        if len(Password.strip()) < 5:
            self.PasswordLabel.config(text="Password must be 5 or more characters", fg="red")
            self.ValidPassword = False
        else:
            self.PasswordLabel.config(text="Password is Good!", fg="green")
            self.ValidPassword = True

    def EmailTrack(self):
        Email = self.EmailVar.get()
        if not re.fullmatch(regex, Email):
            self.EmailLabel.config(text="Invalid Email", fg="red")
            self.ValidEmail = False
        elif collection.find_one({"email": Email}):
            self.EmailLabel.config(text="Email is Already Registered", fg="red")
            self.ValidEmail = False
        else:
            self.EmailLabel.config(text="Email is Good!", fg="green")
            self.ValidEmail = True


class ResizingCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        WScale = float(event.width) / self.width
        HScale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        self.config(width=self.width, height=self.height)
        self.scale("all", 0, 0, WScale, HScale)


class Dimensions:
    def __init__(self):
        self.width = 1000
        self.height = 650


class Login(Dimensions):
    def __init__(self):
        super().__init__()
        self.pages = Tk()
        self.pages.wm_iconbitmap('logo.png')
        self.LoginPage = Frame(self.pages)
        self.Username = None
        self.Password = None
        self.WelcomeName = None
        self.SubmitBtn = None
        self.SignUpBtn = None
        self.ContinueAsGuest = None
        self.label = None

        self.LoginPage.pack(fill=BOTH, expand=YES)

        self.bg = PhotoImage(file="bg.png")
        self.canvas = ResizingCanvas(self.LoginPage, width=self.width, height=self.height, bg="red",
                                     highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=YES)
        self.canvas.create_image(self.width / 2, self.height / 2, image=self.bg)
        self.canvas.create_rectangle(self.width / 3, self.height / 6.5, self.width / 3 * 2,
                                     self.height - self.height / 6.5, fill="white")
        self.canvas.addtag_all("all")
        self.pages.title("Login")
        self.Labels()
        self.Buttons()
        self.pages.bind('<Return>', self.CheckExistence)
        self.LoginPage.mainloop()

    def Labels(self):
        LabelOne = Label(self.canvas, text='Sign in', bg="white")
        LabelOne.config(font=("Roboto", int((self.width + self.height) / 2 / 27.5)))
        self.canvas.create_window(self.width / 2, self.height / 3.75, window=LabelOne)

        UsernameLabel = Label(self.LoginPage, text="Username", bg="white")
        self.canvas.create_window(self.width / 2.5, self.height / 2.65, window=UsernameLabel)

        self.Username = ttk.Entry(self.LoginPage, width=int(self.width / (self.width / 35)),
                                  font=("roboto", 15))
        self.canvas.create_window(self.width / 2, self.height / 2.35, width=self.width / 4, window=self.Username)

        PasswordLabel = Label(self.LoginPage, text="Password", bg="white")
        self.canvas.create_window(self.width / 2.5, self.height / 2.05, window=PasswordLabel)

        self.Password = ttk.Entry(self.LoginPage, show='*', width=int(self.width / (self.width / 35)),
                                  font=("roboto", 15))
        self.canvas.create_window(self.width / 2, self.height / 1.85, width=self.width / 4, window=self.Password)

        someLabel = Label(self.LoginPage, text="or", bg="white")
        self.canvas.create_window(self.width / 2.33, self.height / 1.45, window=someLabel)

    def Buttons(self):
        self.SubmitBtn = ttk.Button(self.LoginPage, text="Login",
                                    command=self.CheckExistence)
        self.canvas.create_window(self.width / 2, self.height / 1.6, width=self.width / 4, window=self.SubmitBtn)

        self.SignUpBtn = ttk.Button(self.LoginPage, text="Register", command=Register)
        self.canvas.create_window(self.width / 2.42, self.height / 1.45, window=self.SignUpBtn)

        self.ContinueAsGuest = ttk.Button(self.LoginPage, text="Continue as Guest", command=self.StartAsGuest)
        self.canvas.create_window(self.width / 1.95, self.height / 1.45, window=self.ContinueAsGuest)

    def StartAsGuest(self):
        self.pages.destroy()
        config.Username = "Guest"
        MainPage()

    def CheckExistence(self):
        username = self.Username.get()
        password = self.Password.get()
        if collection.find_one({"username": username}) is not None and (
                collection.find_one({"username": username})["password"]) == password:
            self.WelcomeName = (collection.find_one({"username": username}))["name"]
            self.pages.destroy()
            config.Username = (collection.find_one({"username": username}))["username"]
            MainPage()
            return True
        elif self.label is None:
            self.label = Label(self.LoginPage, text="Invalid Username or Password", borderwidth=1, relief="solid")
            self.label.config(highlightbackground="red", font=("Rockwell", 12), foreground="red")
            self.canvas.create_window(self.width / 2, self.height / 3, window=self.label)
            return


class MainPage(Dimensions):
    def __init__(self):
        super().__init__()
        self.temp = Tk()
        self.OpenPalm = StringVar()
        self.Fist = StringVar()
        self.IndexFinger = StringVar()
        self.SwipeAction = StringVar()
        self.SpiderMan = StringVar()
        self.OK = StringVar()
        self.Telephone = StringVar()
        self.temp.wm_iconbitmap('logo.png')
        self.bg = PhotoImage(file="bg.png")
        self.MainPage = Frame(self.temp)
        self.Guest = True if config.Username == "Guest" else False
        self.Actions = [self.OpenPalm, self.Fist, self.IndexFinger, self.SwipeAction, self.SpiderMan, self.OK,
                        self.Telephone]
        self.ActionsString = ["OpenPalm", "Fist", "IndexFinger", "SwipeAction", "SpiderMan", "OK",
                              "Telephone"]
        for i in zip(self.Actions, self.ActionsString):
            i[0].set(collectionGestures.find_one({"username": config.Username})[f"{config.Username}{i[1]}"])

        self.ActionsFunctions = [self.OpenPalmFunction, self.FistFunction, self.IndexFingerFunction,
                                 self.SwipeActionFunction, self.SpiderManFunction, self.OKFunction,
                                 self.TelephoneFunction]
        self.width_size = ["Left Click", "Right Click", "Swipe", "Move Mouse", "Drag Mouse", "Volume Slider", "Mouse Scroll",
                           "Pause", "Draw", "DrawUp", "Clear Drawing", "No Action"]
        self.MainPage.pack(fill=BOTH, expand=YES)

        self.canvas = ResizingCanvas(self.MainPage, width=self.width, height=self.height, bg="red",
                                     highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=YES)
        self.canvas.create_image(self.width / 2, self.height / 2, image=self.bg)
        self.canvas.create_rectangle(self.width - 10, 10, 10, self.height - 10, fill="white")
        print(config.Username)
        self.Buttons()
        self.MainPage.mainloop()

    def Buttons(self):
        StartButton = Button(self.MainPage, text="Start", bg="white", bd=0, command=self.Start)
        self.canvas.create_window(self.width / 2, self.height / 1.5, window=StartButton)

        for i, j in enumerate(self.Actions[0:4]):
            self.menu = OptionMenu(self.MainPage, j, *self.width_size,
                                   command=self.ActionsFunctions[i])
            self.canvas.create_window(i * 1.25 * 150 + 225, self.height / 5, window=self.menu)
            label = Label(self.MainPage, text=self.ActionsString[i], bg="white")
            self.canvas.create_window(i * 1.25 * 150 + 225, self.height / 5 - 30, window=label)
        for i, j in enumerate(self.Actions[4:7]):
            self.menu = OptionMenu(self.MainPage, j, *self.width_size,
                                   command=self.ActionsFunctions[i + 4])
            self.canvas.create_window(i * 1.25 * 150 + 300, self.height / 3, window=self.menu)
            label = Label(self.MainPage, text=self.ActionsString[i + 4], bg="white")
            self.canvas.create_window(i * 1.25 * 150 + 300, self.height / 3 - 30, window=label)

    def OpenPalmFunction(self, choice):
        choice = self.OpenPalm.get()
        if not self.Guest:
            collectionGestures.update_one({f"{config.Username}OpenPalm":
                                               collectionGestures.find_one({"username": config.Username})[
                                                   f"{config.Username}OpenPalm"]},
                                          {"$set": {f"{config.Username}OpenPalm": choice}})
        print(collectionGestures.find_one({"username": config.Username})[f"{config.Username}OpenPalm"])
        print("OpenPalm " + choice)

    def FistFunction(self, choice):
        choice = self.Fist.get()
        if not self.Guest:
            collectionGestures.update_one({f"{config.Username}Fist":
                                               collectionGestures.find_one({"username": config.Username})[
                                                   f"{config.Username}Fist"]},
                                          {"$set": {f"{config.Username}Fist": choice}})
        print(collectionGestures.find_one({"username": config.Username})[f"{config.Username}Fist"])
        print("Fist " + choice)

    def IndexFingerFunction(self, choice):
        choice = self.IndexFinger.get()
        if not self.Guest:
            collectionGestures.update_one({f"{config.Username}IndexFinger":
                                               collectionGestures.find_one({"username": config.Username})[
                                                   f"{config.Username}IndexFinger"]},
                                          {"$set": {f"{config.Username}IndexFinger": choice}})
        print(collectionGestures.find_one({"username": config.Username})[f"{config.Username}IndexFinger"])
        print("Index " + choice)

    def SwipeActionFunction(self, choice):
        choice = self.SwipeAction.get()
        if not self.Guest:
            collectionGestures.update_one({f"{config.Username}SwipeAction":
                                               collectionGestures.find_one({"username": config.Username})[
                                                   f"{config.Username}SwipeAction"]},
                                          {"$set": {f"{config.Username}SwipeAction": choice}})
        print(collectionGestures.find_one({"username": config.Username})[f"{config.Username}SwipeAction"])
        print("Swipe " + choice)

    def SpiderManFunction(self, choice):
        choice = self.SpiderMan.get()
        if not self.Guest:
            collectionGestures.update_one({f"{config.Username}SpiderMan":
                                               collectionGestures.find_one({"username": config.Username})[
                                                   f"{config.Username}SpiderMan"]},
                                          {"$set": {f"{config.Username}SpiderMan": choice}})
        print(collectionGestures.find_one({"username": config.Username})[f"{config.Username}SpiderMan"])
        print("Spider Man " + choice)

    def OKFunction(self, choice):
        choice = self.OK.get()
        if not self.Guest:
            collectionGestures.update_one({f"{config.Username}OK":
                                               collectionGestures.find_one({"username": config.Username})[
                                                   f"{config.Username}OK"]},
                                          {"$set": {f"{config.Username}OK": choice}})
        print(collectionGestures.find_one({"username": config.Username})[f"{config.Username}OK"])
        print("OK " + choice)

    def TelephoneFunction(self, choice):
        choice = self.Telephone.get()
        if not self.Guest:
            collectionGestures.update_one({f"{config.Username}Telephone":
                                               collectionGestures.find_one({"username": config.Username})[
                                                   f"{config.Username}Telephone"]},
                                          {"$set": {f"{config.Username}Telephone": choice}})
        print(collectionGestures.find_one({"username": config.Username})[f"{config.Username}Telephone"])
        print("Telephone " + choice)

    def Start(self):
        for i in range(len(self.Actions)):
            config.GestureDict[self.ActionsString[i]] = self.Actions[i].get()
        print(config.GestureDict)
        self.temp.destroy()
        Start()

A = Login()
