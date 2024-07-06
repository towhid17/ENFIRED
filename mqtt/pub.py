import sys

import paho.mqtt.client as mqtt
import time

device_no = 0

def main(host):
    global device_no
    device_no = d_no
    client = mqtt.Client()
    client.connect(host, 1883, 60)

    time_count = 0

    while True:
        timestamp = time.time()
        payload = str(timestamp)
        client.publish("topic/iot_"+str(device_no), payload)
        time.sleep(1)
        time_count += 1

        if time_count == 60:
            break
        


if __name__ == "__main__":
    host = sys.argv[1]
    d_no = int(sys.argv[2])
    main(host)
