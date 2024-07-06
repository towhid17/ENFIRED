import os
import sys
import time

sys.path.append('../Final')

from conf import exp_conf as ip
from utils.net_info import NetInfo


def open_broker_on_gateways(net):
    for i in range(ip.nApps):
        net['a' + str(i)].cmdPrint('mosquitto &')


def start_publisher_on_devices(net):
    ni = NetInfo()
    for i in range(ip.nDevices):
        net['d' + str(i)].cmdPrint('sudo python3 mqtt/pub.py ' + ni.ip_app[i] + ' ' + str(i) + ' &')


def start_subscriber_on_app(net):
    ni = NetInfo()
    for i in range(ip.nApps):
        net['d' + str(i)].cmdPrint('sudo python3 mqtt/sub.py ' + ni.ip_app[i] + ' ' + str(i) + ' &')
        time.sleep(0.2)




def periodic_device_delay_update(net):
    directory_name = "exp_results/" + ip.exp_id
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    for i in range(ip.nDevices):
        file_name = directory_name + "/device_" + str(i) + ".txt"
        file = open(file_name, "w")
        file.close()

    open_broker_on_gateways(net)
    time.sleep(2)

    while True:
        start_publisher_on_devices(net)
        time.sleep(2)
        start_subscriber_on_app(net)
        time.sleep(50)
