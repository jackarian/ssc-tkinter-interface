from tkinter import *
from tkinter import ttk
from tkinter import Tk
from tkinter import font
from tkinter import messagebox
import json
from stomp_ws.client import Client
from application import img as images


class Application(ttk.Frame):
    def __init__(self, master=None, ws_uri=None, topic=None, width=820, height=480):
        ttk.Frame.__init__(self, master, borderwidth=5, relief="ridge", width=width, height=height)
        self.grid(column=0, row=0)
        self.client = Client(ws_uri)
        self.topic = topic
        self.logo = PhotoImage(file=images.LOGO)
        self.logoLepark = PhotoImage(file=images.LOGO_LEPARK)
        master.iconphoto(True, self.logo)
        """
        Crete interface component 
        """
        self.frame = ttk.Frame(self, borderwidth=1, relief="ridge", width=width, height=height - 20)
        self.highlightFont = font.Font(family='Helvetica', name='appHighlightFont', size=16, weight='bold')
        self.bodyFont = font.Font(family='Helvetica', name='appBodyFont', size=12, weight='bold')

        self._createWidgets(self.frame, width - 10, height - 80)
        self.connected = FALSE

    def _createWidgets(self, frame, width, height):
        self.logoLabel = ttk.Label(self,
                                   text="",
                                   image=self.logoLepark,
                                   compound=LEFT)
        self.logoLabel.place(x=0, y=0)
        frame.place(x=1, y=1, width=width, height=height)

        # Create the application variable.
        self.titleText = StringVar()
        self.titleText.set("Title")
        # Set it to some value.
        self.bodyText = StringVar();
        self.bodyText.set("Body")

        self.titlelbl = ttk.Label(frame, width=width // 2,
                                  textvariable=self.titleText,
                                  justify='center',
                                  font=self.highlightFont,
                                  background="#FFF",
                                  foreground="red")
        self.titlelbl.place(x=(width // 2) - (width // 4), y=10)

        self.bodylbl = ttk.Label(frame,
                                 width=width // 2,
                                 textvariable=self.bodyText,
                                 justify='center',
                                 font=self.bodyFont,
                                 background="#FEF",
                                 foreground="red")

        self.bodylbl.place(x=(width // 2) - (width // 4) - 100, y=100)

        self._buildfooter(frame, width, height)

    def _buildfooter(self, frame, width, height):
        self.connectBtn = ttk.Button(self, text='Connect', command=self.connect)
        self.connectBtn.place(x=80, y=height + 1)

        self.quitBtn = ttk.Button(self, text="Quit", command=self.close)
        self.quitBtn.place(x=0, y=height + 1)

    def connect(self):
        if not self.client.connected:
            self.client.connect(connectCallback=self.onConnected)
            self.client.subscribe(self.topic, callback=self.onReceiveMessage)

    def close(self):
        if self.connected:
            self.client.disconnect()

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
        self.connectBtn.config(state=DISABLED)
        messagebox.showinfo("Service", "Connection established")


if __name__ == '__main__':
    root = Tk()
    icon = PhotoImage(file=images.LOGO)
    root.iconphoto(True, icon)
    app = Application(root, "ws://localhost:8080/ssc/prenostazione-risorse/websocket", "/info")
    root.title('SSC')
    root.minsize(820, 480)
    root.maxsize(820, 480)
    app.mainloop()
