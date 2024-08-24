import tkinter as tk
from tkinter import  font
if __name__ == '__main__':

 root = tk.Tk()
 screen_width = root.winfo_screenwidth()
 screen_height = root.winfo_screenheight()
 print(screen_width)
 print(screen_height)
 print(font.families())
 print('names')
 print(font.names())