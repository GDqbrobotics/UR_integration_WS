import random
from paho.mqtt import client as mqtt_client

class MQTT_SUB:
    def __init__(self, broker='broker.emqx.io', port=1883, topic="python/mqtt"):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client_id = f'subscribe-{random.randint(0, 100)}'
        self.received_msg = False

    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc, properties):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print(f"Failed to connect, return code {rc}")

        client = mqtt_client.Client(client_id=self.client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def subscribe(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            self.received_msg = True

        client.subscribe(self.topic)
        client.on_message = on_message
    
    def reset_received_msg(self):
        self.received_msg = False

    def run(self):
        client = self.connect_mqtt()
        self.subscribe(client)
        client.loop_forever()

if __name__ == '__main__':
    x = MQTT_SUB()
    x.run()