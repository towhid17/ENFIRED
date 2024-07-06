import sys
import time

import paho.mqtt.client as mqtt

sys.path.append('../Final')

from conf import exp_conf as ip

import utils.file_operation as fo

received_timestamps = []
tick = 0
device_no = 0
directory_name = "exp_results/" + ip.exp_id


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("topic/iot_"+str(device_no))


def on_message(client, userdata, msg):
    global tick
    tick += 1
    received_timestamp = time.time()
    sent_timestamp = float(msg.payload.decode())
    time_diff = (received_timestamp - sent_timestamp) * 1000
    received_timestamps.append(time_diff)
    if tick % 7 == 0:
        avg = sum(received_timestamps) / len(received_timestamps)
        fo.update_device_delay_csv(device_no, avg)
        file_name = directory_name + "/device_" + str(device_no) + ".txt"
        fo.append_periodic_delay_update(file_name, received_timestamps)
        received_timestamps.clear()
    
    if tick == 40:
        exit()


def main(host, d_no):
    global device_no
    device_no = d_no

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(host, 1883, 60)

    client.loop_forever()


if __name__ == "__main__":
    host = sys.argv[1]
    d_no = int(sys.argv[2])
    main(host, d_no)
