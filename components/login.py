from tkinter import ttk
from tkinter import StringVar
from tkinter.simpledialog import Dialog


class LoginDialog(Dialog):
     

    def __init__(self, parent, title, errors=''):
        self._pw = StringVar()
        self._user = StringVar()
        self._error = StringVar(value=errors)          
        super().__init__(parent, title=title)
        

    def body(self, frame):
       
        ttk.Label(frame, text='Login SSC').grid(row=0)
        if self._error.get():
            ttk.Label(frame, textvariable=self._error).grid(row=1)
