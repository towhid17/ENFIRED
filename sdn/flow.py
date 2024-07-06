import json
import requests

from subprocess import Popen, PIPE

import conf.exp_conf as ip


def add_flow(out_port, in_port, current_node, flow_count, src_ip, dst_ip, src_mac, dst_mac, fog_ip):
    static_flow_url = "http://127.0.0.1:8080/wm/staticflowentrypusher/json"

    flowF = {
        "switch": "00:00:00:00:00:00:00:" + current_node,
        "name": "flow-mod-" + str(flow_count) + "-F",
        "cookie": "0",
        "priority": "32768",
        "in_port": in_port,
        "eth_type": "0x0800",
        "ipv4_src": src_ip,
        "ipv4_dst": dst_ip,
        "eth_src": src_mac,
        "eth_dst": dst_mac,
        "active": "true",
        "actions": "output=" + out_port
    }

    json_data = json.dumps(flowF)
    cmd = "curl -s -d \'" + json_data + "\' " + static_flow_url
    system_command(cmd)

    flowFarp = {
        "switch": "00:00:00:00:00:00:00:" + current_node,
        "name": "flow-mod-" + str(flow_count) + "-Farp",
        "cookie": "0",
        "priority": "32768",
        "in_port": in_port,
        "eth_type": "0x0806",
        "active": "true",
        "actions": "output=" + out_port
    }

    json_data = json.dumps(flowFarp)
    cmd = "curl -s -d \'" + json_data + "\' " + static_flow_url
    system_command(cmd)

    flowR = {
        "switch": "00:00:00:00:00:00:00:" + current_node,
        "name": "flow-mod-" + str(flow_count) + "-R",
        "cookie": "0",
        "priority": "32768",
        "in_port": out_port,
        "eth_type": "0x0800",
        "ipv4_src": dst_ip,
        "ipv4_dst": src_ip,
        "eth_src": dst_mac,
        "eth_dst": src_mac,
        "active": "true",
        "actions": "output=" + in_port
    }

    json_data = json.dumps(flowR)
    cmd = "curl -s -d \'" + json_data + "\' " + static_flow_url
    system_command(cmd)

    flowRarp = {
        "switch": "00:00:00:00:00:00:00:" + current_node,
        "name": "flow-mod-" + str(flow_count) + "-Rarp",
        "cookie": "0",
        "priority": "32768",
        "in_port": out_port,
        "eth_type": "0x0806",
        "active": "true",
        "actions": "output=" + in_port
    }

    json_data = json.dumps(flowRarp)
    cmd = "curl -s -d \'" + json_data + "\' " + static_flow_url
    system_command(cmd)


def delete_flow(flow_count):
    cmd  = "curl -X DELETE -d \'{\"name\":\"flow-mod-" + str(flow_count) + "-F\"}\' http://127.0.0.1:8080/wm/staticflowentrypusher/json"
    system_command(cmd)

    cmd = "curl -X DELETE -d \'{\"name\":\"flow-mod-" + str(flow_count) + "-Farp\"}\' http://127.0.0.1:8080/wm/staticflowentrypusher/json"
    system_command(cmd)

    cmd = "curl -X DELETE -d \'{\"name\":\"flow-mod-" + str(flow_count) + "-R\"}\' http://127.0.0.1:8080/wm/staticflowentrypusher/json"
    system_command(cmd)

    cmd = "curl -X DELETE -d \'{\"name\":\"flow-mod-" + str(flow_count) + "-Rarp\"}\' http://127.0.0.1:8080/wm/staticflowentrypusher/json"
    system_command(cmd)


def system_command(cmd):
    terminal_process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    terminal_output, stderr = terminal_process.communicate()
    print(terminal_output)


def delete_routing_flow(reassigned_devices):
    for item in range(len(reassigned_devices)):
        delete_flow(reassigned_devices[item])


def delete_all_flow():
    for item in range(ip.nDevices):
        delete_flow(item)