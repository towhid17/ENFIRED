import socket
import sys
import time

sys.path.append('../Final')

from conf import exp_conf as ip
from utils.net_info import NetInfo

import data_traffic.data_sample as ds
import utils.file_operation as fo


def get_devices_under_fog_router(fog_no, router_no, net_info):
    devices = []
    for i in range(ip.nDevices):
        if net_info.device_fog[i] == fog_no and i // ip.device_per_router == router_no:
            devices.append(i)
    return devices


def start_delay_update(HOST, PORT, router_no, fog_no, net_info):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect((HOST, PORT))

    time_count = 0

    while True:
        start_time = time.time()
        ds.sent_sample(s, HOST, PORT)
        end_time = time.time()
        delay = (end_time - start_time) * 1000

        print("Delay: " + str(delay) + " ms")

        devices = get_devices_under_fog_router(fog_no, router_no, net_info)
        fo.update_device_delay_csv(devices, delay)

        fo.save_delay_update_time_count_fog_id_delay(router_no, fog_no, delay, time_count)

        time.sleep(ip.delay_update_period)
        time_count += ip.delay_update_period
    s.close()


def open_server_on_fog(net):
    ni = NetInfo()
    for i in range(ip.nFog):
        net['f' + str(i)].cmdPrint('sudo python3 data_traffic/server.py ' + ni.ip_fog[i] + ' &')
    net['cloud'].cmdPrint('sudo python3 data_traffic/server.py ' + ni.ip_cloud + ' &')


def periodic_device_delay_update(net):
    open_server_on_fog(net)
    for i in range(ip.nRouters):
        for j in range(ip.nFog):
            net['r' + str(i)].cmdPrint(
                'sudo python3 periodic_updates/delay_update.py ' + str(i) + ' ' + str(j) + ' &')
            time.sleep(0.5)


if __name__ == "__main__":
    router_no = int(sys.argv[1])
    fog_no = int(sys.argv[2])

    net_info = NetInfo()

    HOST = net_info.ip_fog[fog_no]
    PORT = 12345

    start_delay_update(HOST, PORT, router_no, fog_no, net_info)
