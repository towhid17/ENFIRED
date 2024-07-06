import random

import conf.exp_conf as ip
import utils.file_operation as fo


class NetInfo:
    def __init__(self):
        self.device_delay_sensitive = None
        self.ip_cloud = None
        self.ip_gateway = []
        self.ip_fog = []
        self.ip_device = []
        self.ip_app = []
        self.ip_gateway_device = []
        self.ip_gateway_app = []
        self.ip_fog_eth = []
        self.ip_cloud_eth = None

        self.device_mac = {}

        # port mapping
        # if gateway == i (0, nRouters-1), (re-routing) switch == 2*i+1
        self.port_gateway_fog = 2
        self.port_gateway_app = 4 + ip.nFog
        self.port_gateway_cloud = 2 + ip.nFog
        self.port_fog = ip.nRouters

        self.device_fog = [0 for i in range(ip.nDevices)]
        self.device_flow = [i for i in range(1, ip.nDevices + 1)]
        self.delay_threshold_pre_calc = ip.delay_pre_calc
        self.ratio_sensitive_tolerant = ip.ratio_sensitive_tolerant
        self.device_delay_threshold = [100 for i in range(ip.nDevices)]
        self.gateway_nearest_fog = [0 for i in range(ip.nRouters)]
        self.gateway_fog_cluster = None

        # ip addresses
        # ip device
        for i in range(ip.nDevices):
            self.ip_device.append('10.0.0.' + str(i + 1))

        # ip gateway
        for i in range(ip.nRouters):
            self.ip_gateway.append('10.0.0.' + str(i + ip.nDevices + 1))

        # ip fog
        for i in range(ip.nFog):
            self.ip_fog.append('10.0.0.' + str(i + ip.nDevices + ip.nRouters + 1))

        # ip cloud
        self.ip_cloud = '10.0.0.' + str(ip.nDevices + ip.nRouters + ip.nFog + 1)

        # ip app
        for i in range(ip.nApps):
            self.ip_app.append('10.0.0.' + str(i + ip.nDevices + ip.nRouters + ip.nFog + 2))

        # cluster (this need to be updated according to the network topology)
        self.gateway_nearest_fog = [2, 4]
        self.gateway_fog_cluster = [[1,2,3], [4,5,6]]

    def assign_delay_threshold(self):
        for item in range(int(ip.nDevices * ip.ratio_sensitive_tolerant)):
            self.device_delay_threshold[item] = random.randint(self.delay_threshold_pre_calc[0],
                                                               self.delay_threshold_pre_calc[1])

        for item in range(int(ip.nDevices * ip.ratio_sensitive_tolerant), ip.nDevices):
            self.device_delay_threshold[item] = random.randint(self.delay_threshold_pre_calc[1],
                                                               self.delay_threshold_pre_calc[3])

        random.shuffle(self.device_delay_threshold)
        self.device_delay_sensitive = fo.save_device_category_and_threshold(self.device_delay_threshold,
                                                                            self.delay_threshold_pre_calc)

    def create_fog_device_map(self):
        for i in range(ip.nDevices):
            if self.device_delay_threshold[i] >= self.delay_threshold_pre_calc[2]:
                self.device_fog[i] = 0
            else:
                self.device_fog[i] = self.gateway_nearest_fog[i//ip.device_per_router]

        fo.save_fog_device_map(self.device_fog)
