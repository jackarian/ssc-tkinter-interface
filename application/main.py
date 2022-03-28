from tkinter import *
from tkinter import ttk
import json
from stomp_ws.client import Client


class Application(ttk.Frame):
    def __init__(self, master=None, ws_uri=None, topic=None):
        ttk.Frame.__init__(self, master, borderwidth=5, relief="ridge", width=820, height=480)
        self.grid(column=0, row=0)
        self.client = Client(ws_uri)
        self.topic = topic
        self.frame = ttk.Frame(self, borderwidth=1, relief="ridge", width=820, height=400)

        self.createWidgets(self.frame)
        self.connected = FALSE

    def createWidgets(self, frame):

        frame.place(x=0, y=0, width=810, height=400)
        self.titlelbl = ttk.Label(frame, text="Title")
        self.titlelbl.grid(column=10, row=1, columnspan=50)

        self.bodylbl = ttk.Label(frame, text="Body")
        self.bodylbl.grid(column=0, row=2, columnspan=50)

        self.connectBtn = ttk.Button(self, text='Connect', command=self.connect)
        self.connectBtn.place(x=80, y=401)

        self.quitBtn = ttk.Button(self, text="Quit", command=self.close)
        self.quitBtn.place(x=0, y=401)

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
        self.titlelbl['text'] = message['title']
        # print("Body messaggio: %s" % message['body'])
        self.bodylbl['text'] = message['body']
        # print("Sorgente messaggio: %s" % message['plc_source'])

    def onConnected(self, frame):
        self.connected = TRUE


if __name__ == '__main__':
    root = Tk()
    app = Application(root, "ws://localhost:8080/ssc/prenostazione-risorse/websocket", "/info")
    root.title('SSC')
    root.minsize(820, 480)
    root.maxsize(820, 480)
    app.mainloop()
