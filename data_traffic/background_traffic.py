import random
import sys
import time
import os

sys.path.append('../Final')

import conf.exp_conf as ip
import mqtt.periodic_delay_update as du


def generate_distinct_random_list(n):
    size = n // 2
    if size > n:
        size = n
    random_list = random.sample(range(0, n), size)
    return random_list

def start_iperf_servers(net, fog_nodes, base_port, cloud, apps, devices):
    for i in range(ip.nFog):
        server = net[fog_nodes[i]]
        server.cmd('iperf -u -s -p ' + str(base_port) + ' &')
    server = net[cloud]
    server.cmd('iperf -u -s -p ' + str(base_port) + ' &')

    for i in range(ip.nApps):
        server = net[apps[i]]
        server.cmd('iperf -u -s -p ' + str(base_port) + ' &')
    
    for i in range(ip.nDevices):
        server = net[apps[i]]
        client = net[devices[i]]
        iperf_single(client, server, ip.device_load, ip.sim_time, 5001)


def iperf_single(client, server, udp_bw='4M', period=5, port=5001):
    print("iperf(c, s): %s and %s" % (client.name, server.name))
    client.cmd(
        'iperf -u -i 5 -t ' + str(period) + ' -c ' + server.IP() + ' -p ' + str(port) + ' -b ' + udp_bw + ' &')


def background_traffic(net, gateways, fog_nodes, cloud, rbw, rbwc, base_port):
    targeted_fog = generate_distinct_random_list(ip.nFog)
    for i in range(0, ip.nRouters):
        for j in targeted_fog:
            client = net[gateways[i]]
            server = net[fog_nodes[j]]
            iperf_single(client, server, udp_bw=rbw, period=ip.iperf_period, port=base_port)
        client = net[gateways[i]]
        server = net[cloud]
        iperf_single(client, server, udp_bw=rbwc, period=ip.iperf_period, port=base_port)


def start_background_traffic(net=None, gateways=None, fog_nodes=None, cloud=None, apps=None, devices=None):
    base_port = 5001
    rbw = ip.fog_capacity_threshold
    rbw = str(rbw) + 'M'
    rbwc = ip.cloud_capacity_threshold
    rbwc = str(rbwc) + 'M'
    start_iperf_servers(net, fog_nodes, base_port, cloud, apps, devices)
    
    directory_name = "exp_results/" + ip.exp_id
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    for i in range(ip.nDevices):
        file_name = directory_name + "/device_" + str(i) + ".txt"
        file = open(file_name, "w")
        file.close()

    du.open_broker_on_gateways(net)
    time.sleep(2)
    
    time_count = 0

    while True:
        if (time_count % (ip.iperf_interval + ip.iperf_period)) == 0 or time_count == 0:
            background_traffic(net, gateways, fog_nodes, cloud, rbw, rbwc, base_port)
        
        if (time_count % 50) == 0 or time_count == 0:
            du.start_publisher_on_devices(net)
            time.sleep(2)
            time_count += 2
            du.start_subscriber_on_app(net)
            
        time.sleep(1)
        time_count += 1