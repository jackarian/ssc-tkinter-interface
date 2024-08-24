import json
from pathlib import Path
from threading import Thread
from tkinter import *
from tkinter import Tk
from tkinter import font
from tkinter import messagebox
from tkinter import ttk

import yaml

from application import img as images
from interfaces import observer
from qr_serial.serial_controller import QrCodeSerialController
from rest.restclient import SscClient
from stomp_ws.client import Client
from components import login


class Application(ttk.Frame, observer.ConnectionObserver):
    def __init__(self, master=None, ws_uri=None, topic=None, service_uri=None, width=800, height=480, claz=None):
        try:
            super().__init__(master, borderwidth=5, relief="ridge", width=width, height=height)
            self._configureFromFile()
            self.grid(column=0, row=0)
            self.client = Client(ws_uri, self)
            self.sscClient = SscClient(service_uri, self.config['plc']['id'])
            self.topic = topic
            self.logo = PhotoImage(file=images.LOGO)
            self.logoLepark = PhotoImage(file=images.LOGO_LEPARK)
            self.logoMultiverso = PhotoImage(file=images.LOGO_MULTIVERSO)
            self.cameralbl = None
            self.canvas = None
            self.messageType = {
                0: '#FC1919',
                1: '#2981c3',
                2: '#2981c3'
            }
            master.iconphoto(True, self.logo)
            """
            Create interface component 
            """
            
            self.highlightFont = font.Font(family='Liberation Sans', name='appHighlightFont', size=30, weight='bold')
            self.subheaderFont = font.Font(family='Liberarion Sans', name='messageFont', size=9, weight='bold')
            self.bodyFont      = font.Font(family='Liberation Sans', name='appBodyFont', size=18, weight='bold')
           
            self.frame = ttk.Frame(self, borderwidth=0, relief="ridge", width=width, height=height)
            self._createHeader(self.frame, width - 10, height - 80)
            self._createCanvas(self.frame, width - 10, height - 80)
            # self._createWidgets(self.frame, width - 10, height - 80)
            self._buildfooter(self.frame, width - 10, height - 80)
            self.connected = FALSE
            if claz is not None:
                self.cam = claz(self.cameralbl, self.sscClient)
            self._createBinding()
            self.canvas.itemconfigure(self.cMessageTitle, text="Header")
            self.canvas.itemconfigure(self.cMessageBody, text="Body")
            self.canvas.itemconfigure(self.cHeader, text=self.config['header']['text'])
            self.canvas.itemconfigure(self.cBody, text=self.config['subheader']['text'])
            self.pack()
            # self.server = Server(MyGpio('test'))
            # self.server.run()
        except Exception as e:
                print(e)
       

    def _createCanvas(self, frame, width, height, start=10):
        self.cwidth = width - 10
        self.cheight = height//2
        self.canvas = Canvas(frame, width=self.cwidth / 2, height=self.cheight,borderwidth=0, relief="ridge")
        self.canvas.place(x=width // 2 - (self.cwidth // 4), y=start+100)
        
        xpos = (self.cwidth / 2) - ((self.cwidth / 2 - 10) / 2)
        self.cHeader = self.canvas.create_text(xpos, 20,
                                                     width=self.cwidth / 2 - 10,
                                                     font='appHighlightFont', fill='#2981c3', justify='center')
        self.cBody = self.canvas.create_text(xpos, 70,
                                                    width=self.cwidth / 2 - 10,
                                                    font='appBodyFont', fill='#2981c3', justify='center')
      
        self.cMessageTitle = self.canvas.create_text(xpos, 120,
                                                     width=self.cwidth / 2 - 10,
                                                     font='appBodyFont', fill='#2981c3', justify='center')
        self.cMessageBody = self.canvas.create_text(xpos, 170,
                                                    width=self.cwidth / 2 - 10,
                                                    font='messageFont', fill='#2981c3', justify='center')
        

    def _createBinding(self):

        self.master.bind('<Control-Up>', lambda e: self.connect())
        self.master.bind('<Control-Left>', lambda e: self.close())
        self.master.bind('<Control-Down>', lambda e: self.scancode())
        self.master.bind('<Control-Right>', lambda e: self._showLogin())

    def _createHeader(self, frame, width, height, start=100):

        frame.place(x=1, y=1, width=width, height=height)
        self.logoLabel = ttk.Label(self,
                                   image=self.logoMultiverso,
                                   compound=LEFT)
        self.logoLabel.place(x=(width // 2) - 50, y=2)
        # Create the application variable.
        '''
        self.header = StringVar()
        self.header.set(self.config['header']['text'])

        self.sheader = StringVar()
        self.sheader.set(self.config['subheader']['text'])
        self.headerlbl = ttk.Label(frame, width=width // 2,
                                   textvariable=self.header,
                                   justify='center',
                                   font=self.highlightFont,
                                   foreground='#2981c3')
        self.headerlbl.place(x=(width // 2) - self.highlightFont.measure(self.config['header']['text']) // 2,
                             y=start + 50)
        
        self.sheaderlbl = ttk.Label(frame, width=width // 2,
                                    textvariable=self.sheader,
                                    justify='center',
                                    font=self.subheaderFont,
                                    foreground='#2981c3')        
        self.sheaderlbl.place(x=(width // 2) - self.subheaderFont.measure(self.config['subheader']['text']) // 2,
                              y=start + 100)        
        '''
        
    def _showLogin(self):
        loginDialog = login.LoginDialog(self.master,'Login','errors')
        print(loginDialog._user)

         
    
    def _configureFromFile(self):
        home = str(Path.home())
        with open(r'' + home + '/config/gui.yaml') as file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            self.config = yaml.load(file, Loader=yaml.FullLoader)
            for item, doc in self.config.items():
                print(item, ":", doc)

    def _buildfooter(self, frame, width, height):
        # self.connectBtn = ttk.Button(self, text='Connect', command=self.connect)
        # self.connectBtn.place(x=80, y=height + 1)

        # self.quitBtn = ttk.Button(self, text="Quit", command=self.close)
        # self.quitBtn.place(x=0, y=height + 1)

        # self.scanBtn = ttk.Button(self, text='Scan', command=self.scancode)
        # self.scanBtn.place(x=161, y=height + 1)
        self.quitBtn = ttk.Button(self, text="Pulisci Schermo", command=self._clearMessage)
        self.quitBtn.place(x=0, y=height + 1)

    def connect(self):
        if not self.client.connected:
            thread = Thread(target=self.client.connect,
                            kwargs=
                            {'connectCallback': self.onConnected, 'timeout': 10000})
            thread.daemon = True
            thread.start()

    def close(self):
        if self.connected:
            self.client.disconnect()

        self.cam.onClose()
        self.quit()

    def onReceiveMessage(self, frame):
        message = json.loads(frame.body)
        self.canvas.itemconfigure(self.cMessageTitle, fill=self.messageType[message['type']])
        self.canvas.itemconfigure(self.cMessageTitle, text=message['title'])
        self.canvas.itemconfigure(self.cMessageBody, fill=self.messageType[message['type']])
        self.canvas.itemconfigure(self.cMessageBody, text=message['body'])

    def _clearMessage(self):
        self.canvas.itemconfigure(self.cMessageTitle, text="")
        self.canvas.itemconfigure(self.cMessageBody, text="")

    def onConnected(self, frame):
        self.connected = TRUE
        # self.connectBtn.config(state=DISABLED)
        self.client.subscribe(self.topic, callback=self.onReceiveMessage)
        messagebox.showinfo("Service", "Connection established")

    def scancode(self):
        self.cam.startCapture()

    def notifyOnClose(self, observable=None, message=None, exception=None):
        self.connected = FALSE
        # self.connectBtn.config(state=ACTIVE)

    def notifyOnOpen(self, observable=None, message=None, exception=None):
        # print("notifyOnOpen")
        pass

    def notifyOnError(self, observable=None, message=None, exception=None):
        messagebox.showerror("Service", message)
        self.connected = FALSE
        # self.connectBtn.config(state=ACTIVE)


if __name__ == '__main__':
    root = Tk()
    icon = PhotoImage(file=images.LOGO)
    root.iconphoto(True, icon)
    app = Application(root, "ws://service.local:8080/ssc/prenostazione-risorse/websocket",
                      "/info",
                      "http://service.local:8080/ssc",
                       root.winfo_screenmmwidth(), 
                       root.winfo_screenheight(), 
                       QrCodeSerialController)
    root.title('SSC')
    app.mainloop()
