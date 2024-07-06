import requests

import sdn.flow_stats as fs
from utils.net_info import NetInfo


class NetworkController:

    def __init__(self):
        self.switch = {}
        self.hostPorts = {}
        self.net_info = NetInfo()

    def get_connected_topo_info(self):
        try:
            enable_stats = "http://localhost:8080/wm/statistics/config/enable/json"
            requests.put(enable_stats)
            self.net_info.device_mac, self.switch, self.hostPorts = fs.device_information()
            print("\n\n############ Topology ############\n\n")
            print("\n\nSwitch: ", self.switch)
            print("\nIP & MAC\n\n", self.net_info.device_mac)
            print("\nHost::Switch Ports\n\n", self.hostPorts)
            print("\n\n#######################################\n\n")
        except Exception as e:
            print("Error in deviceInfo\n")
