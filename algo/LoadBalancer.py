from abc import ABC, abstractmethod
import sys

sys.path.append('../Final')

import conf.exp_conf as ip
import sdn.flow_stats as fs
import utils.file_operation as fo
import sdn.flow as fl
import sdn.forwarding_table as ft


class LoadBalancer(ABC):
    @abstractmethod
    def load_balance(self):
        pass

    @staticmethod
    def get_fog_load():
        fog_throughput = []
        for i in range(0, ip.nFog + 1):
            fog_throughput.append(fs.get_throughput(str(ip.nRouters * 2 + i), str(ip.nRouters + 1)) / 1024)
            fo.update_fog_load_csv(i, fog_throughput[i])
            print("Fog " + str(i) + " throughput: " + str(fog_throughput[i]))
        return fog_throughput

    @staticmethod
    def reassign_devices_after_load_balance(reassign_devices, net_info):
        if len(reassign_devices):
            fo.save_fog_device_map(net_info.device_fog)
            fl.delete_routing_flow(reassign_devices)
            ft.fog_cloud_reassignment(reassign_devices, net_info.device_fog, net_info.ip_app,
                                      net_info.ip_device, net_info.ip_fog,
                                      net_info.ip_cloud, net_info.port_gateway_app, net_info.device_mac)
