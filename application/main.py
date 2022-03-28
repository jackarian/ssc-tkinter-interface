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
        self.createWidgets()

    def createWidgets(self):
        self.titlelbl = ttk.Label(self, text="Title")
        self.titlelbl.grid(column=3, row=1)
        self.body = ttk.Label(self, text="Body")
        self.body.grid(column=3, row=2)
        self.connectBtn = ttk.Button(self, text='Test connection to service', command=self.connect)
        self.connectBtn.grid(column=3, row=4)

        self.quitBtn = ttk.Button(self, text="Quit", command=self.quit)
        self.quitBtn.grid(column=4, row=4)

    def connect(self):
        if not self.client.connected:
          self.client.connect()
          self.client.subscribe(self.topic, callback=self.onReceiveMessage)

    def onReceiveMessage(self, frame):
        message = json.loads(frame.body)
        print("Tipo messaggio: %s" % message['type'])
        print("Titolo messaggio: %s" % message['title'])
        print("Body messaggio: %s" % message['body'])
        print("Sorgente messaggio: %s" % message['plc_source'])


if __name__ == '__main__':
    root = Tk()
    app = Application(root, "ws://localhost:8080/ssc/prenostazione-risorse/websocket", "/info")
    root.title('SSC')
    root.minsize(820, 480)
    root.maxsize(820, 480)
    app.mainloop()
