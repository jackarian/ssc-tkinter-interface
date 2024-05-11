from paho.mqtt import client as mqtt_client


class Client(mqtt_client.Client):
    def __init__(self, broker='localhost', port=1883, login='admin', password=None, topic=None, client_id='ssc-server'):
        self.broker = broker
        self.port = port
        self.login = login
        self.password = password
        self.topic = topic
        super(Client, self).__init__(client_id)

    def _on_connect(self, client, userdata, flags, rc):
        print("Connected with result")


if __name__ == '__main__':
    client = Client()
