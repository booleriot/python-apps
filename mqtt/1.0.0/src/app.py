from ast import Return
import asyncio
import json
from urllib import response
import itertools
import paho.mqtt.client as mqtt
import time
import logging
from walkoff_app_sdk.app_base import AppBase

class MQTTClient:
    def __init__(self, broker_address, broker_port, username, password, client_id):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.username = username
        self.password = password
        self.client_id = client_id
        self.connect_success = False
        self.msg = None
    
    def on_connect(self, client, userdata, flags, rc):
        print("mqtt_client {} connected with result code {}".format(client, rc))
        if rc == 0:
            self.connect_success = True
        else:
            self.connect_success = False

    def on_message(self, client, userdata, msg):
        print("mqtt_client {} received message on topic {}".format(client, msg.topic))
        self.msg = msg
    
    def connect(self):
        self.client = mqtt.Client(client_id=self.client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.broker_address, self.broker_port, 60)
        self.client.loop_start()
    
    def subscribe(self, topic):
        self.client.subscribe(topic)
    
    def publish(self, topic, message):
        json_msg = json.dumps(message)
        reulst_msg = json_msg.encode("utf-8")
        self.client.publish(topic, reulst_msg)


class MQTT(AppBase):
    __version__ = "1.0.0"
    app_name = "MQTT"  # this needs to match "name" in api.yaml

    def __init__(self, redis, logger, console_logger=None):
        self.connect_success = False
        self.msg = None
        self.mqtt_client=None
        super().__init__(redis, logger, console_logger)
    # Write your data inside this function
    def subcribe_msg(self, server, port, user, password,subtopic):
        self.mqtt_client = MQTTClient(server, int(port), user, password, "walkoff")
        self.mqtt_client.connect()
        self.mqtt_client.subscribe(subtopic)
        while self.mqtt_client.msg is None:
            time.sleep(5)
        response = {
                    "message": f"connect is {self.mqtt_client.connect_success}",
                    "topic":self.mqtt_client.msg.topic,
                    "payload":self.mqtt_client.msg.payload.decode("utf-8"),
        }
        
        return response
    
    def send_msg(self, server, port, user, password,sendtopic, sendmsg):
        self.mqtt_client = MQTTClient(server, int(port), user, password, "walkoff")
        self.mqtt_client.connect()
        while self.mqtt_client.connect_success is False:
            time.sleep(2)
        self.mqtt_client.publish(sendtopic, sendmsg)
        response = {
                    "message": f"connect is {self.mqtt_client.connect_success}",
                    "topic":sendtopic,
                    "payload":sendmsg
        }
        return response
    

if __name__ == "__main__":
    MQTT.run()
