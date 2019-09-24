import paho.mqtt.client as mqtt
import threading, time
import os
import json
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)

class MQTTCONFIG():
  TOPIC_V100_IN = "et/01/+/in"
  TOPIC_V100_OUT = 'et/01/+/out'
  BROKER_URL = 'www.ethings.vn'
  BROKER_PORT = 1883
  BROKER_USER = 'MQmodem'
  BROKER_PASS = 'ethingsMQ100'
  SSL_FILE = ''

  ssl_enable = 0

def rule_process(rule, thing, thingdata):
  try:
    if rule.rule_type == 1: #equal
      ret = (thingdata.conv_value == float(rule.rule_value))
    elif rule.rule_type == 2: #upper
      ret = (thingdata.conv_value > float(rule.rule_value))
    elif rule.rule_type == 3: #under
      ret = (thingdata.conv_value > float(rule.rule_value))
    elif rule.rule_type == 4: #in range
      minx, maxx = rule.rule_value.split(',')
      ret = ((thingdata.conv_value < float(maxx)) and (thingdata.conv_value > float(minx)))
    elif rule.rule_type == 5: #out range
      minx, maxx = rule.rule_value.split(',')
      ret = ((thingdata.conv_value > float(maxx)) or (thingdata.conv_value < float(minx)))
    elif rule.rule_type == 6: #null
      ret = (thingdata.conv_value is None)
    
    if ret:
      from rulereport.models import RuleEngineReport
      report = RuleEngineReport.objects.create(name=thing.things_alt, value=thingdata.conv_value, 
                    ruleengine_id=rule.id, thing_id=thing.id)
      report.save()
      #print("rule_process: " + report.name + " done!")
  except Exception as ex:
    #print("rule_process: " + str(ex))
    logger.error("rule_process: " + str(ex))
  

def convert_data_type(thing, thingdata):
    from pymodbus.constants import Endian
    from pymodbus.payload import BinaryPayloadDecoder

    try:
      decoder = BinaryPayloadDecoder.fromRegisters(thingdata.raw_value, Endian.Big)
      if thing.things_type == 1:   # BIT        
          thingdata.value = decoder.decode_bits()
      elif thing.things_type == 2:   # BYTE
          thingdata.value = decoder.decode_8bit_int()  
          thingdata.conv_value = ((thingdata.value & int(thing.things_mask, 16)) * thing.things_gain) + thing.things_offset      
      elif thing.things_type == 3:   # UBYTE
          thingdata.value = decoder.decode_8bit_uint()
          thingdata.conv_value = ((thingdata.value & int(thing.things_mask, 16)) * thing.things_gain) + thing.things_offset
      elif thing.things_type == 4:   # SHORT
          thingdata.value = decoder.decode_16bit_int()
          thingdata.conv_value = ((thingdata.value & int(thing.things_mask, 16)) * thing.things_gain) + thing.things_offset
      elif thing.things_type == 5:   # USHORT
          thingdata.value = decoder.decode_16bit_uint()
          thingdata.conv_value = ((thingdata.value & int(thing.things_mask, 16)) * thing.things_gain) + thing.things_offset
      elif thing.things_type == 6:   # INT32
          thingdata.value = decoder.decode_32bit_int()
          thingdata.conv_value = ((thingdata.value & int(thing.things_mask, 16)) * thing.things_gain) + thing.things_offset
      elif thing.things_type == 7:   # UINT32
          thingdata.value = decoder.decode_32bit_uint()
          thingdata.conv_value = ((thingdata.value & int(thing.things_mask, 16)) * thing.things_gain) + thing.things_offset
      elif thing.things_type == 9:   # INT64
          thingdata.value = decoder.decode_64bit_int()
          thingdata.conv_value = ((thingdata.value & int(thing.things_mask, 16)) * thing.things_gain) + thing.things_offset
      elif thing.things_type == 10:   # UINT64
          thingdata.value = decoder.decode_64bit_uint()
          thingdata.conv_value = ((thingdata.value & int(thing.things_mask, 16)) * thing.things_gain) + thing.things_offset
      elif thing.things_type == 8:   # FLOAT
          thingdata.value = decoder.decode_32bit_float()
          thingdata.conv_value = ((thingdata.value) * thing.things_gain) + thing.things_offset
      elif thing.things_type == 11:   # DOUBLE
          thingdata.value = decoder.decode_64bit_float()
          thingdata.conv_value = ((thingdata.value) * thing.things_gain) + thing.things_offset
      
    except Exception as ex:
      #print("convert_data_type:" + str(ex))
      logger.error("convert_data_type: " + str(ex))

def on_publish(client,userdata,result):
    #print("Device 1 : Data published.")
    pass

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTTCONFIG.TOPIC_V100_IN)

def on_message(client, userdata, msg):
    #topic et/01/G02102018027/in
    '''{"messageType": "Periodic", "payload":[{"data": [{"size": 1, 
    "functionCode": 4, "value": [1925], "address": 24}, {"size": 1, 
    "functionCode": 4, "value": [0], "address": 25}], "version": 1.2, "slave": 10},
    {"data": [{"size": 2, "functionCode": 4, "value": [16482, 58454], "address": 0}, 
    {"size": 2, "functionCode": 4, "value": [18157, 1313], "address": 10}], 
    "version": 1.2, "slave": 1}], "sentDate": "2019-08-31 23:37:19"}'''
    from things.models import ThingData
    from things.models import Thing
    from gateway.models import Gateway
    from device.models import Device
    from ruleengine.models import RuleEngine

    payload = msg.payload.decode()
    #print(payload)
    try:
      provider, msg_version, gateway_name, direct = msg.topic.split('/')
    
      if provider == 'et' and msg_version == '01' and direct == 'in':
        jdata = json.loads(payload)
        #print(jdata)
        try:
          if jdata['messageType'] == 'Periodic':
            #gw = Gateway.objects.all().filter(name=gateway_name)
            jpayload_arr = jdata['payload']
            try:
              devs = Device.objects.all().filter(gateway_id__name=gateway_name)
            except:
              pass

            #print(devs)
            for jp in jpayload_arr:
              dev = devs.get(dev_address=int(jp['slave']))
              #things = Thing.objects.all().filter(device_id=dev)
              for point in jp['data']:
                try:
                  #thing = things.get(things_fcode=point['functionCode'],
                  #                      things_address=point['address'])
                  thing = Thing.objects.get(device_id=dev,
                      things_fcode=int(point['functionCode']),
                      things_address=int(point['address']))
                  #print(thing)
                  if thing is not None:
                    # save data to Database. Version 1.0.0, I dont care system perfromance.
                    thingdata = ThingData.objects.create(things_id=thing.id, name=thing.things_alt)
                    thingdata.raw_value = point['value']
                    convert_data_type(thing, thingdata)
                    thingdata.save()
                    # load all rule engine for thing, process them and save to rule report.
                    rules = RuleEngine.objects.all().filter(thing_id=thing.id)
                    #print('*****************', rules)
                    for rule in rules:
                      rule_process(rule, thing, thingdata)
                except:
                  pass
            
        except Exception as ex:
          #print("filter: " + str(ex), payload)
          logger.error("mqtt payload: " + payload + str(ex))
    except Exception as ex:
      #print(str(ex) + msg.topic)
      logger.error("mqtt topic: " + msg.topic + str(ex))

client =mqtt.Client("et-01-pid-" + str(os.getpid()))
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
#client.on_log = on_log
#client.on_disconnect = on_disconnect
cuser = MQTTCONFIG.BROKER_USER
cpass = MQTTCONFIG.BROKER_PASS

if MQTTCONFIG.ssl_enable == 0:
    client.username_pw_set(cuser, cpass)
elif MQTTCONFIG.ssl_enable == 1:
    import ssl
    ssl.match_hostname = lambda cert, hostname: True
    client.username_pw_set(cuser, cpass)
    client.tls_set(MQTTCONFIG.SSL_FILE, tls_version=ssl.PROTOCOL_TLSv1_2)
    client.tls_insecure_set(False)

import sys
def mqtt_init():
  #print("mqtt client start")
  try:
    client.connect(MQTTCONFIG.BROKER_URL, port=MQTTCONFIG.BROKER_PORT)
    client.loop_forever(.01)
    # while True:
    #   time.sleep(1)
    #   print('hello world')
    
    sys.exit()
  except Exception as ex:
    #print(str(ex))
    logger.error("mqtt_init: " + str(ex))

def datasource_mqtt_init():
  mqtt_thread = threading.Thread(target=mqtt_init, name="mqtt_thread")
  mqtt_thread.start()
  #print("created thread for mqtt client" + str(os.getpid()))

#test
# mqtt_init()