#!/usr/bin/env python

import sys
import time

import sdn.forwarding_table as ft
import sdn.net_controller as nc
import utils.file_operation as fo
from algo.LoadBalancerFactory import LoadBalancerFactory
import conf.exp_conf as ip

net_ctrl = nc.NetworkController()

if __name__ == "__main__":
    fo.write_exp_conf()

    fo.delete_core_files()

    net_ctrl.get_connected_topo_info()

    fo.create_device_load_csv()
    fo.create_device_delay_csv()
    fo.create_fog_load_csv()
    
    net_ctrl.net_info.assign_delay_threshold()
    net_ctrl.net_info.create_fog_device_map()

    

    ft.init_fog_cloud_assignment(net_ctrl.net_info.device_fog, net_ctrl.net_info.ip_app,
                                 net_ctrl.net_info.ip_device,
                                 net_ctrl.net_info.ip_fog, net_ctrl.net_info.ip_cloud,
                                 net_ctrl.net_info.port_gateway_app, net_ctrl.net_info.device_mac)

    time.sleep(5)

    algo = ip.algo
    load_balancer = LoadBalancerFactory.create_load_balancer(algorithm=algo, net_info=net_ctrl.net_info)
    load_balancer.load_balance()
