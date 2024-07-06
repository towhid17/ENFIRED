import time

import conf.exp_conf as ip
import utils.file_operation as fo
import sdn.flow_stats as fs
from algo.LoadBalancer import LoadBalancer


# fog = 0 means cloud

class DSLoadBalancer(LoadBalancer):
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
                if float(self.device_delay[device]) > self.net_info.device_delay_threshold[device]:
                    selected_fog = self.select_fog_node(device, self.device_delay)
                    if selected_fog != -1:
                        self.reassign_fog(device, selected_fog)
                    else:
                        self.reassign_tolerant_devices_to_cloud(self.net_info.device_fog[device])
                    
            LoadBalancer.reassign_devices_after_load_balance(self.reassign_devices, self.net_info)

            time.sleep(2)

            self.reassign_devices = []
            for fog in range(1, ip.nFog + 1):
                if self.is_fog_overloaded(fog):
                    self.reassign_tolerant_devices_to_cloud(fog)
                elif self.fog_load[fog] < ip.fog_capacity_threshold * 1024 / 2:
                    self.reassign_tolerant_devices_to_fog(fog)

            LoadBalancer.reassign_devices_after_load_balance(self.reassign_devices, self.net_info)

            time.sleep(ip.load_balance_period)
            time_count += ip.load_balance_period

    def reassign_fog(self, device, selected_fog):
        self.reassign_devices.append(device)
        prev_fog = self.net_info.device_fog[device]
        self.net_info.device_fog[device] = selected_fog
        self.update_fog_load(selected_fog, device, prev_fog)
        self.update_device_delay(device, self.device_delay, selected_fog)

    def is_fog_overloaded(self, fog_id):
        return self.fog_load[fog_id] > ip.fog_capacity_threshold * 1024

    def select_fog_node(self, device, device_delay):
        avg_delay = []
        device_count_fog = []
        for i in range(ip.nFog + 1):
            avg_delay.append(0)
            device_count_fog.append(0)
        for i in range(ip.nDevices):
            avg_delay[self.net_info.device_fog[i]] += float(device_delay[i])
            device_count_fog[self.net_info.device_fog[i]] += 1
        for i in range(ip.nFog + 1):
            if device_count_fog[i] > 1:
                avg_delay[i] /= device_count_fog[i]
        
        min_load = 99999999
        selected_fog = -1

        device_gateway = device // ip.device_per_router

        for i in self.net_info.gateway_fog_cluster[device_gateway]:
            if avg_delay[i] < device_delay[device] and self.fog_load[i] < ip.fog_capacity_threshold * 1024:
                if min_load>self.fog_load[i]:
                    min_load=self.fog_load[i]
                    selected_fog=i
                    
        return selected_fog

    def update_fog_load(self, selected_fog, device, prev_fog):
        self.fog_load[prev_fog] -= self.device_load[device]
        self.fog_load[selected_fog] += self.device_load[device]

    def update_device_delay(self, device, device_delay, selected_fog):
        avg_delay = 0
        device_count_fog = 0
        for i in range(ip.nDevices):
            if self.net_info.device_fog[i] == selected_fog:
                avg_delay += float(device_delay[i])
                device_count_fog += 1
        if device_count_fog > 1:
            avg_delay /= device_count_fog
        self.device_delay[device] = avg_delay

    def reassign_tolerant_devices_to_cloud(self, fog_id):
        if fog_id != 0:
            for i in range(ip.nDevices):
                if self.is_fog_overloaded(fog_id) and self.fog_load[0] < ip.cloud_capacity_threshold * 1024:
                    if self.net_info.device_fog[i] == fog_id and not self.net_info.device_delay_sensitive[i]:
                        self.reassign_fog(i, 0)
                else:
                    break

    def reassign_tolerant_devices_to_fog(self, fog_id):
        if fog_id != 0:
            for i in range(ip.nDevices):
                if self.fog_load[fog_id] < ip.fog_capacity_threshold * 1024 / 2:
                    if self.net_info.device_fog[i] == 0 and not self.net_info.device_delay_sensitive[i]:
                        self.reassign_fog(i, fog_id)
                        break
                else:
                    break