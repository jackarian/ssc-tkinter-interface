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
        self.quitButton = ttk.Button(self, text='Test connection to service', command=self.connect)
        self.quitButton.grid(column=3, row=2)
        self.ok = ttk.Button(self, text="Okay")
        self.ok.grid(column=4, row=2)
        self.cancel = ttk.Button(self, text="Cancel")

    def connect(self):
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
