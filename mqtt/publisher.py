
import random
import time

from paho.mqtt import client as mqtt_client


broker = 'localhost'
port = 1883
topic = "python/mqtt"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'
commandFile = "targets.txt"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client,commandFile):
    f = open(commandFile, "r")
    lines = f.readlines()
    print(f"{len(lines)} pick positions read from file")
    for line in lines:
        input("Press any Key to send next pick position")
        msg = line
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
    print(f"End of the list. Closing Publisher.")


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client,commandFile)
    client.loop_stop()


if __name__ == '__main__':
    run()
