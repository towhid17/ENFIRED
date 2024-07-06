import random

import conf.exp_conf as ip
import sdn.flow as fl


# fog = 0 means cloud in device_fog

def init_assign_all_devices_to_cloud(device_fog, ip_app, ip_device, ip_cloud, port_gateway_app, deviceMac):
    for item in range(0, ip.nDevices):
        device_fog[item] = 0
    for item in range(0, ip.nDevices):
        add_single_flow(device_fog, item, ip_app, ip_cloud, ip_device, ip_cloud, port_gateway_app, deviceMac)


def init_fog_cloud_assignment(device_fog, ip_app, ip_device, ip_fog, ip_cloud, port_gateway_app, deviceMac):
    for i in range(0, ip.nDevices):
        add_single_flow(device_fog, i, ip_app, ip_cloud, ip_device, ip_fog, port_gateway_app, deviceMac)


def fog_cloud_reassignment(reassign_devices, device_fog, ip_app, ip_device, ip_fog, ip_cloud, port_gateway_app, deviceMac):
    for j in range(0, len(reassign_devices)):
        i = reassign_devices[j]
        add_single_flow(device_fog, i, ip_app, ip_cloud, ip_device, ip_fog, port_gateway_app, deviceMac)


def add_single_flow(device_fog, i, ip_app, ip_cloud, ip_device, ip_fog, port_gateway_app, deviceMac):
    if device_fog[i] != 0:
        outport = str(device_fog[i] + 2)
        fog_ip = ip_fog[device_fog[i] - 1]
    else:
        outport = str(ip.nFog + 3)
        fog_ip = ip_cloud
    inport = str(1)
    gateway_no = i // ip.device_per_router
    gateway_switch_no = ip.nRouters + gateway_no
    gsw_str = str(gateway_switch_no)
    if gateway_switch_no // 10 == 0:
        gsw_str = "0" + str(gateway_switch_no)
    current_node = gsw_str
    flow_count = i
    dst_ip = ip_app[i]
    src_ip = ip_device[i]
    src_mac = deviceMac[src_ip]
    dst_mac = deviceMac[dst_ip]

    # print("add flow: \noutport: " + outport + " \nsw: " + current_node + " \nsrc_ip: " + src_ip + " \nfog_ip: " + fog_ip)

    fl.add_flow(outport, inport, current_node, flow_count,
                src_ip, dst_ip, src_mac, dst_mac, fog_ip)
