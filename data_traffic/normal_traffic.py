import time


class NormalTraffic:
    def __init__(self, net, nDevices, nApps, ip_device, ip_app):
        self.net = net
        self.nDevices = nDevices
        self.nApps = nApps
        self.ip_device = ip_device
        self.ip_app = ip_app

    # start server on application
    def start_server_on_app(self):
        for i in range(self.nApps):
            self.net['a' + str(i)].cmdPrint('python3 data_traffic/server.py ' + self.ip_app[i] + ' &')

    # send device to application data
    def send_data_from_iot_to_app(self):
        for i in range(self.nDevices):
            self.net['d' + str(i)].cmdPrint('python3 data_traffic/client.py ' + self.ip_app[i] + ' &')

    def start_data_transfer(self):
        self.start_server_on_app()
        time.sleep(5)
        self.send_data_from_iot_to_app()
