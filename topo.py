#!/usr/bin/python
import time

from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import Node, OVSSwitch
from mininet.node import RemoteController
from mininet.topo import Topo
import threading

import conf.exp_conf as ip
import data_traffic.background_traffic as bt
from data_traffic.normal_traffic import NormalTraffic
from utils.net_info import NetInfo
import mqtt.periodic_delay_update as du
import periodic_updates.traffic_update as tu

# ///////////////////////////////-------------- topology ------------ ////////////////////////////////////////#
# iot -> iot_switch -> gateways(switch+host) -> fog/cloud(switch+host) -> app_switch -> applications/servers #
# ///////////////////////////////-------------- topology ------------ ////////////////////////////////////////#

gateways = []
fog_nodes = []
devices = []
apps = []
iot_switches = []
gateway_switches = []
fog_switches = []
app_switch = None
cloud_switch = None

cloud = None

iot_switches_count = ip.nRouters
gateway_switches_count = ip.nRouters
fog_switches_count = ip.nFog
cloud_switch_count = 1
app_switch_count = 1


class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
    def build(self, **_opts):
        # add iot devices
        for i in range(ip.nDevices):
            d = self.addHost('d' + str(i), ip='10.0.0.' + str(i + 1) + '/24')
            devices.append(d)

        # add switch
        # add iot switch
        for i in range(iot_switches_count):
            s = self.addSwitch('s' + str(i), cls=OVSSwitch, protocols="OpenFlow13")
            iot_switches.append(s)

        # add gateway switch
        for i in range(gateway_switches_count):
            s = self.addSwitch('s' + str(i + iot_switches_count), cls=OVSSwitch, protocols="OpenFlow13")
            gateway_switches.append(s)

        # add fog switch
        for i in range(fog_switches_count):
            s = self.addSwitch('s' + str(i + iot_switches_count + gateway_switches_count), cls=OVSSwitch, protocols="OpenFlow13")
            fog_switches.append(s)

        global cloud_switch, app_switch
        # add cloud switch
        cloud_switch = self.addSwitch('s' + str(iot_switches_count + gateway_switches_count + fog_switches_count), cls=OVSSwitch, protocols="OpenFlow13")

        # add app switch
        app_switch = self.addSwitch('s' + str(iot_switches_count + gateway_switches_count + fog_switches_count + 1), cls=OVSSwitch, protocols="OpenFlow13")

        # add gateways/routers
        for i in range(ip.nRouters):
            r = self.addHost('r' + str(i),  ip='10.0.0.' + str(i + ip.nDevices + 1) + '/24')
            gateways.append(r)

        # add fog node using openflow switch
        for i in range(ip.nFog):
            f = self.addHost('f' + str(i), 
                             ip='10.0.0.' + str(ip.nRouters + ip.nDevices + i + 1) + '/24')
            fog_nodes.append(f)

        # cloud node like fog node
        global cloud
        cloud = self.addHost('cloud', 
                             ip='10.0.0.' + str(ip.nRouters + ip.nDevices + ip.nFog + 1) + '/24')

        # add app
        for i in range(ip.nApps):
            a = self.addHost('a' + str(i), ip='10.0.0.' + str(ip.nRouters + ip.nDevices + ip.nFog + i + 2) + '/24')
            apps.append(a)

        # connect with switch
        # iot -> iot_switch
        for i in range(iot_switches_count):
            for j in range(ip.device_per_router):
                start = i * ip.device_per_router
                self.addLink(iot_switches[i], devices[start + j])

        # iot_switch -> gateway_switch
        for i in range(iot_switches_count):
            self.addLink(gateway_switches[i], iot_switches[i], bw=7)
            # gateways -> gateway_switch
            self.addLink(gateways[i], gateway_switches[i], bw=7)

        # gateway_switch -> fog_switch
        for i in range(ip.nRouters):
            if i==0:
                for j in range(ip.nFog):
                    d = ip.nearest_fog_link_delay + j*ip.link_delay_gap
                    d = str(d)+'ms'
                    self.addLink(gateway_switches[i], fog_switches[j], delay=d, bw=10)
            else:
                for j in range(ip.nFog):
                    d = ip.nearest_fog_link_delay + (ip.nFog-1-j)*ip.link_delay_gap
                    d = str(d)+'ms'
                    self.addLink(gateway_switches[i], fog_switches[j], delay=d, bw=10)
            # gateway_switch -> cloud_switch
            self.addLink(gateway_switches[i], cloud_switch, delay='150ms', bw=15)

        # fog_switch -> fog
        for i in range(ip.nFog):
            self.addLink(fog_nodes[i], fog_switches[i])

        # cloud_switch -> cloud
        self.addLink(cloud, cloud_switch)

        # fog_switch -> app_switch
        for i in range(ip.nFog):
            self.addLink(fog_switches[i], app_switch)

        # cloud_switch -> app_switch
        self.addLink(cloud_switch, app_switch)

        # app_switch -> app
        for i in range(ip.nApps):
            self.addLink(apps[i], app_switch)



        for i in range(ip.nRouters):
            self.addLink(gateways[i], app_switch)


def run():
    # ///////////////////////////////////////-------------- create topology ------------ ////////////////////////////////////////#
    topo = NetworkTopo()
    net = Mininet(topo=topo, controller=lambda name: RemoteController(name, ip='127.0.0.1', protocol='tcp', port=6653),
                  link=TCLink, autoSetMacs=True)
    net.start()
    CLI(net)

    # ///////////////////////////////////////-------------- start simulation ------------ ////////////////////////////////////////#
    net_info = NetInfo()

    mqtt_thread = threading.Thread(target=du.periodic_device_delay_update, args=(net,))
    mqtt_thread.start()

    # du.periodic_device_delay_update(net)

    tu.periodic_device_traffic_update(net)

    normal_traffic = NormalTraffic(net, ip.nDevices, ip.nApps, net_info.ip_device, net_info.ip_app)
    normal_traffic.start_data_transfer()

    bt.start_background_traffic(net, gateways, fog_nodes, cloud, apps, devices)

    time.sleep(ip.sim_time)

    # ///////////////////////////////////////-------------- stop simulation ------------ ////////////////////////////////////////#
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
