#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Running....

import paho.mqtt.client as mqtt #import the client1
import time
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient, Point, WriteOptions
import json
import random

   
#  MQTT Subscribe and Write data to influx:

bucket = "EMS"
broker_address="3.7.85.13"

# Topic for Energy data
TopicEM = "JBMGroup/em3phase"

# Topic for Machine data
TopicMch = "JBMGroup/MachineData/#"


def on_message(client1, userdata, message):
    
    try:
            rawdata = str(message.payload.decode("utf-8"))
            data = json.loads(rawdata)
            countOff = 0;
            countOn = 0;
            for keys in data:
                if (keys[0:2] == "EM"):
                    
                    if (data.get(keys) != 0):
                        countOn= countOn+1;
                        
                    if (data.get(keys) == 0):
                        countOff = countOff+1;
            
            data["Active_Meters"] = countOn
            data["Inactive_Meters"] = countOff
            
            
            print(data)
#             return data
            
            availableTagCount = print("Total available tags:",len(data))           


    except:
            print("Error in receiving data.")
  
                            
                                       

    with InfluxDBClient(url="http://localhost:8086", token="2aCMvt4a8dhSLvjJzZHydvCyBfZiH_PcHCipkZHQQR66QGD9cx4E3gcsSY-XKx-M5sDwipcaAXyxO1KyZvddwQ==", org="JBM") as _client:

            with _client.write_api(write_options=WriteOptions(batch_size=500,
                                                          flush_interval=10_000,
                                                          jitter_interval=2_000,
                                                          retry_interval=5_000,
                                                          max_retries=5,
                                                          max_retry_delay=30_000,
                                                          exponential_base=2)) as _write_client:


                try:
#                     _write_client.write("EMS", "JBM", {"measurement": "EMSJ2", "tags": {"machineId": data['machineId'] },
#                                                         "fields": data})
                    print(data)
                    _write_client.write("EMS", "JBM", {"measurement": "EMSJ2New", "fields": data})
#                     

                   
                                                        
                except:
                    print("Error Occured... ",Exception)       
            
    
# if __name__ == "__main__":
#     bucket = "EMS"
#     broker_address="3.7.85.13"


# Topic for Energy data
TopicEM = "JBMGroup/em3phase"

# Topic for Machine data
TopicMch = "JBMGroup/MachineData/#"
clientX = str(random.randint(0, 9)) # every time a new client instance is created.
print("creating new instance")
client1 = mqtt.Client(clientX)  #create new instance
client1.on_message=on_message #attach function to callback
print("connecting to broker")
client1.connect(broker_address) #connect to broker
client1.loop_start() #start the loop
    # client1.loop_forever()


print("Subscribing to topic", TopicMch)
client1.subscribe(TopicMch)
    # client1.subscribe("JBMGroup/em3phase/#")
time.sleep(8) # wait
        # client.loop_stop() #stop the loop
while True:
    try:
        client1.loop_start()
        print("looping")
    except Exception as e:
        print(e)
    time.sleep(3)
         
           
        


# In[ ]:




