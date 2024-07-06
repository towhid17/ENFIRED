import time

import conf.exp_conf as ip
import utils.file_operation as fo
import sdn.flow_stats as fs
from algo.LoadBalancer import LoadBalancer


class LeastLinkUtilization(LoadBalancer):
    def __init__(self, net_info):
        self.device_load = None
        self.device_delay = None
        self.fog_load = None
        self.net_info = net_info
        self.reassign_devices = []

    def load_balance(self):
        time_count = 0
        while True:
            self.device_delay = fo.read_device_delay_csv()
            self.fog_load = LoadBalancer.get_fog_load()
            self.device_load = fo.read_device_load_csv()

            self.reassign_devices = []

            for device in range(ip.nDevices):
                if self.is_fog_overloaded(self.net_info.device_fog[device]):
                    selected_fog = self.select_fog_node()
                    if selected_fog != self.net_info.device_fog[device]:
                        self.reassign_fog(device, selected_fog)
                    
            LoadBalancer.reassign_devices_after_load_balance(self.reassign_devices, self.net_info)

            time.sleep(ip.load_balance_period)
            time_count += ip.load_balance_period

    def reassign_fog(self, device, selected_fog):
        self.reassign_devices.append(device)
        prev_fog = self.net_info.device_fog[device]
        self.net_info.device_fog[device] = selected_fog
        self.update_fog_load(selected_fog, device, prev_fog)
       
    def is_fog_overloaded(self, fog_id):
        return self.fog_load[fog_id] > ip.fog_capacity_threshold * 1024

    def select_fog_node(self):
        min_load = 99999999
        selected_fog = -1
        for fog in range(1, ip.nFog+1):
            if self.fog_load[fog] < min_load:
                min_load = self.fog_load[fog]
                selected_fog = fog
        
        return selected_fog

    def update_fog_load(self, selected_fog, device, prev_fog):
        self.fog_load[prev_fog] -= self.device_load[device]
        self.fog_load[selected_fog] += self.device_load[device]


