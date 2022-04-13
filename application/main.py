from tkinter import *
from tkinter import ttk
from tkinter import Tk
from tkinter import font
from tkinter import messagebox
import json
import yaml
from threading import Thread
from stomp_ws.client import Client
from interfaces import observer
from application import img as images
from camera.controller import CameraController
from rest.restclient import SscClient
from pathlib import Path


class Application(ttk.Frame, observer.ConnectionObserver):
    def __init__(self, master=None, ws_uri=None, topic=None, service_uri=None, width=1366, height=780):
        ttk.Frame.__init__(self, master, borderwidth=5, relief="ridge", width=width, height=height)
        self._configureFromFile()
        self.grid(column=0, row=0)
        self.client = Client(ws_uri, self)
        self.sscClient = SscClient(service_uri, self.config['plc']['id'])
        self.topic = topic
        self.logo = PhotoImage(file=images.LOGO)
        self.logoLepark = PhotoImage(file=images.LOGO_LEPARK)
        self.logoMultiverso = PhotoImage(file=images.LOGO_MULTIVERSO)
        self.cameralbl = None
        master.iconphoto(True, self.logo)
        """
        Create interface component 
        """
        self.frame = ttk.Frame(self, borderwidth=1, relief="ridge", width=width, height=height - 20)
        self.highlightFont = font.Font(family='Helvetica', name='appHighlightFont', size=30, weight='bold')
        self.subheaderFont = font.Font(family='Helvetica', name='subHighlightFont', size=20, weight='bold')
        self.bodyFont = font.Font(family='Helvetica', name='appBodyFont', size=18, weight='bold')

        self._createWidgets(self.frame, width - 10, height - 80)
        self.connected = FALSE

        self.cam = CameraController(self.cameralbl, self.sscClient)
        self._createBinding()

    def _createBinding(self):

        self.master.bind('<Control-Up>', lambda e: self.connect())
        self.master.bind('<Control-Left>', lambda e: self.close())
        self.master.bind('<Control-Down>', lambda e: self.scancode())

    def _createWidgets(self, frame, width, height):

        frame.place(x=1, y=1, width=width, height=height)
        start = 100
        self.logoLabel = ttk.Label(self,
                                   image=self.logoMultiverso,
                                   compound=LEFT)
        self.logoLabel.place(x=(width // 2) - 50, y=2)

        # Create the application variable.
        self.header = StringVar()
        self.header.set(self.config['header']['text'])

        self.sheader = StringVar()
        self.sheader.set(self.config['subheader']['text'])

        self.titleText = StringVar()
        self.titleText.set("")
        # Set it to some value.
        self.bodyText = StringVar()
        self.bodyText.set("")

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

        self.titlelbl = ttk.Label(frame, width=width // 2,
                                  textvariable=self.titleText,
                                  justify='center',
                                  font=self.highlightFont)

        self.titlelbl.place(x=(width // 2) - (width // 4), y=start + 150)

        self.bodylbl = ttk.Label(frame,
                                 width=width // 2,
                                 textvariable=self.bodyText,
                                 justify='center',
                                 font=self.bodyFont)

        self.bodylbl.place(x=(width // 2) - (width // 4) - 100, y=start + 200)

        self.cameralbl = ttk.Label(frame,
                                   width=width // 2,
                                   )

        self.cameralbl.place(x=(width // 2) - (width // 4) - 100, y=400)
        """
        Costruzione del footer dell'interfaccia
        """
        # self._buildfooter(frame, width, height)

    def _configureFromFile(self):
        home = str(Path.home())
        with open(r'' + home + '/config/gui.yaml') as file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            self.config = yaml.load(file, Loader=yaml.FullLoader)
            # for item, doc in config.items():
            #    print(item, ":", len(doc))
            # self.header.set(config['header']['text'])
            # self.sheader.set(config['subheader']['text'])

    def _buildfooter(self, frame, width, height):
        self.connectBtn = ttk.Button(self, text='Connect', command=self.connect)
        self.connectBtn.place(x=80, y=height + 1)

        self.quitBtn = ttk.Button(self, text="Quit", command=self.close)
        self.quitBtn.place(x=0, y=height + 1)

        self.scanBtn = ttk.Button(self, text='Scan', command=self.scancode)
        self.scanBtn.place(x=161, y=height + 1)

    def connect(self):
        if not self.client.connected:
            thread = Thread(target=self.client.connect,
                            kwargs=
                            {'connectCallback': self.onConnected, 'timeout': 10000})
            thread.daemon = True
            thread.start()
            # self.client.connect(connectCallback=self.onConnected, timeout=10000)

    def close(self):
        if self.connected:
            self.client.disconnect()

        self.cam.onClose()
        self.quit()

    def onReceiveMessage(self, frame):
        message = json.loads(frame.body)
        # print("Tipo messaggio: %s" % message['type'])
        # print("Titolo messaggio: %s" % message['title'])
        self.titleText.set(message['title'])
        # print("Body messaggio: %s" % message['body'])
        self.bodyText.set(message['body'])
        # print("Sorgente messaggio: %s" % message['plc_source'])

    def onConnected(self, frame):
        self.connected = TRUE
        # self.connectBtn.config(state=DISABLED)
        self.client.subscribe(self.topic, callback=self.onReceiveMessage)
        messagebox.showinfo("Service", "Connection established")

    def scancode(self):
        self.cam.startCapture()

    def notifyOnClose(self, observable=None, message=None, exception=None):
        print("notifyOnClose")
        self.connected = FALSE
        # self.connectBtn.config(state=ACTIVE)

    def notifyOnOpen(self, observable=None, message=None, exception=None):
        print("notifyOnOpen")

    def notifyOnError(self, observable=None, message=None, exception=None):
        print("notifyOnError")
        messagebox.showerror("Service", message)
        self.connected = FALSE
        # self.connectBtn.config(state=ACTIVE)


if __name__ == '__main__':
    root = Tk()
    icon = PhotoImage(file=images.LOGO)
    root.iconphoto(True, icon)
    app = Application(root, "ws://service.local:8080/ssc/prenostazione-risorse/websocket",
                      "/info",
                      "http://service.local:8080/ssc", 1366, 768)
    root.title('SSC')
    app.mainloop()
