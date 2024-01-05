# # Complete project details at https://RandomNerdTutorials.com
# # https://randomnerdtutorials.com/micropython-mqtt-esp32-esp8266/

import time

import esp
import machine
import micropython
import network
import ubinascii
from umqttsimple import MQTTClient

esp.osdebug(None)
import gc

gc.collect()

ssid = "internets"
password = "reservoir"
mqtt_server = "192.168.7.160"
user_name = b"mqtt_user"
mqtt_password = b"assword"
# EXAMPLE IP ADDRESS
# mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b"notification"
topic_pub = b"stove/stack/temp"
topic_pub2 = b"stove/top/temp"

last_message = 0
message_interval = 5
counter = 0

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    pass

print("Connection successful")
print(station.ifconfig())
