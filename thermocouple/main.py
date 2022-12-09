# This is your main script.
#--------------------------------------------------------------
# Complete project details at https://RandomNerdTutorials.com
# https://randomnerdtutorials.com/micropython-mqtt-esp32-esp8266/

# import machine
from time import sleep
import math

def temp_f(data):
  temp = data[0] << 8 | data[1] 
  if temp & 0x0001:
    return float('NaN') # Fault reading data. 
  temp >>= 2
  if temp & 0x2000:
    temp -= 16384 # Sign bit set, take 2's compliment.
    # convert to F
  return temp * 0.25/5*9+32

def get_temp(data, the_pin):
  machine.Pin(the_pin, machine.Pin.OUT).value(0) 
  spi.readinto(data) 
  machine.Pin(the_pin, machine.Pin.OUT).value(1) 
  return data

def sub_cb(topic, msg):
  print((topic, msg))
  if topic == b'notification' and msg == b'received':
    print('ESP received hello message')

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

spi = machine.SPI(1, baudrate=5000000, polarity=0, phase=0)
# cs = machine.Pin(13, machine.Pin.OUT)
# cs2 = machine.Pin(15, machine.Pin.OUT)

data = bytearray(4) 
data2 = bytearray(4) 

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

# moving average equation
alpha = 1/10 # number of points to average
# new_temp = alpha * data_point + (1 - alpha) * old_temp

# initialize temp variables
f_ave_old = 60
f2_ave_old = 60

while True:
  try:
    client.check_msg()
    if (time.time() - last_message) > message_interval:
      get_temp(data, 13)  #D7
      get_temp(data2, 15)
      f = temp_f(data)
      f2 = temp_f(data2)

      f_ave = round(alpha * f + (1 - alpha) * f_ave_old, 0)
      f2_ave = round(alpha * f2 + (1 - alpha) * f2_ave_old, 0)

      print("")
      print("stack temp in F is ", f_ave, " not ", f)
      print("top temp in F is ", f2_ave, " not ", f2)

      if not math.isnan(f_ave):
        client.publish(topic_pub, str(f_ave))
      if not math.isnan(f2_ave):
        client.publish(topic_pub2, str(f2_ave))

      last_message = time.time()
      if math.isnan(f_ave):
        f_ave_old = f
      else:
        f_ave_old = f_ave

      if math.isnan(f2_ave):
        f2_ave_old = f2
      else:
        f2_ave_old = f2_ave

  except OSError as e:
    restart_and_reconnect()