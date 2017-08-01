# -*- coding:utf-8 -*-
from Tkinter import *
import os
import requests
import json


class GUIDemo(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        global ewb, ewords

        if not os.path.exists('./EnWordBase.json'):
            web = requests.get(
                "https://raw.githubusercontent.com/voidism/Modify-Input-Type-Automatically/master/EnWordBase.json")
            dic = web.json()
            for i in range(len(dic['words'])):
                if not dic['words'][i].islower():
                    dic['words'][i] = dic['words'][i].lower()
            with open('EnWordBase.json', 'w') as file1:
                json.dump(dic, file1)
            file1.close()
            print 'Dictionary Loaded!'

        with open('EnWordBase.json', 'r') as file2:
            ewb = json.load(file2)
        file2.close()
        ewords = ewb['words']

    def search(self):
        global ewb, ewords
        w = self.inputField.get()
        if w in ewords:
            self.outputText["text"] = w + " is found in " + str(ewords.index(w)) + "th position"
        else:
            self.outputText["text"] = w + " not found"

    def addword(self):
        global ewb, ewords
        w = str(self.inputField.get())
        if w in ewords:
            self.outputText["text"] = w + " is found in " + str(ewords.index(w)) + "th position"
        else:
            ewb['words'].append(w)
            with open('EnWordBase.json', 'w') as file1:
                json.dump(ewb, file1)
            file1.close()
            self.outputText["text"] = "database uploaded with " + w + " added"

    def delete(self):
        global ewb, ewords
        w = self.inputField.get()
        if w in ewords:
            self.outputText["text"] = w + " is found in " + str(ewords.index(w)) + "th position"
            ewb['words'].remove(w)
            with open('EnWordBase.json', 'w') as file1:
                json.dump(ewb, file1)
            file1.close()
            self.outputText["text"] = "database uploaded with " + w + " deleted"
        else:
            self.outputText["text"] = w + " not found"

    def createWidgets(self):
        self.inputText = Label(self)
        self.inputText.grid(row=0, column=0)
        self.inputField = Entry(self)
        self.inputField["width"] = 50
        self.inputField.grid(row=0, column=1, columnspan=5)

        self.outputText = Label(self)
        self.outputText["text"] = "Input the word you want to search or add."
        self.outputText.grid(row=1, column=0, columnspan=7)

        self.add = Button(self)
        self.add["text"] = "Add"
        self.add.grid(row=2, column=2)
        self.add["command"] = self.addword

        self.srh = Button(self)
        self.srh["text"] = "Search"
        self.srh.grid(row=2, column=3)
        self.srh["command"] = self.search

        self.dele = Button(self)
        self.dele["text"] = "Delete"
        self.dele.grid(row=2, column=4)
        self.dele["command"] = self.delete

        self.displayText = Label(self)
        self.displayText["text"] = u"Copyright © 2017 Jexus Chuang. All rights reserved."
        self.displayText.grid(row=3, column=0, columnspan=7)


if __name__ == '__main__':
    root = Tk()
    root.title(string="Dictionary Add & Delete System")
    app = GUIDemo(master=root)
    app.mainloop()
