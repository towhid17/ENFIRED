import sys
import time

sys.path.append('../Final')

import conf.exp_conf as ip
import sdn.flow_stats as fs
import utils.file_operation as fo


def update_device_throughput():
    device_throughput = []
    for i in range(0, ip.nDevices):
        device_throughput.append(
            fs.get_throughput(str(i // ip.device_per_router), str(i % ip.device_per_router + 1)))
        fo.update_device_load_csv(i, device_throughput[i] / 1024)
        print(i, device_throughput[i] / 1024)



def periodic_device_traffic_update(net):
    net['cloud'].cmdPrint(
        'sudo python3 periodic_updates/traffic_update.py' + ' &')


if __name__ == '__main__':
    while True:
        update_device_throughput()
        time.sleep(ip.delay_update_period)
