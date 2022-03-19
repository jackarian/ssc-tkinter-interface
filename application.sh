#!/usr/bin/env python3
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from application import  main

app = main.Application()
app.master.title('Sample application')
app.master.minsize(820, 480)
app.master.maxsize(820, 480)
app.mainloop()