import time

import conf.exp_conf as ip
import utils.file_operation as fo
import sdn.flow_stats as fs
from algo.LoadBalancer import LoadBalancer


class NearestFog(LoadBalancer):
    def __init__(self, net_info):
        self.net_info = net_info
        self.reassign_devices = []

    def load_balance(self):
        self.reassign_devices = []

        for device in range(ip.nDevices):
            selected_fog = device // ip.device_per_router + 1
            self.reassign_fog(device, selected_fog)
            
        LoadBalancer.reassign_devices_after_load_balance(self.reassign_devices, self.net_info)

        time.sleep(ip.sim_time)

    def reassign_fog(self, device, selected_fog):
        self.reassign_devices.append(device)
        self.net_info.device_fog[device] = selected_fog
       
