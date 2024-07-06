import json

import requests


def device_information():
    device_mac = {}
    switch = {}
    host_ports = {}
    url = "http://localhost:8080/wm/device/"
    response = requests.get(url)
    if response.ok:
        data = json.loads(response.content)
        switch_dpid = ""
        data = data['devices']
        # print(data)
        for item in data:
            if item == "devices":
                continue
            if item['ipv4']:
                ip_address = item['ipv4'][0].encode('ascii', 'ignore')
                mac = item['mac'][0].encode('ascii', 'ignore')
                ip_address = ip_address.decode('utf-8')
                mac = mac.decode('utf-8')
                device_mac[ip_address] = mac
                for j in item['attachmentPoint']:
                    for key in j:
                        temp = key.encode('ascii', 'ignore')
                        if temp == "switch":
                            switch_dpid = j[key].encode('ascii', 'ignore')
                            switch[ip_address] = switch_dpid
                        elif temp == "port":
                            port_number = j[key]
                            switch_short = switch_dpid.split(":")[7]
                            host_ports[ip_address + "::" + switch_short] = str(port_number)

    return device_mac, switch, host_ports


def get_throughput(sw_dpid, port):
    url = "http://localhost:8080/wm/statistics/bandwidth/" + \
          sw_dpid + "/" + port + "/json"
    response = requests.get(url)
    if response.ok:
        j_data = json.loads(response.content)
        cost_tx = 0
        cost_rx = 0
        for item in j_data:
            if not isinstance(item, dict):
                continue
            if item['port'] == port:
                cost_tx = cost_tx + int(item['bits-per-second-tx'])
                cost_rx = cost_rx + int(item['bits-per-second-rx'])
        return cost_tx + cost_rx
    else:
        response.raise_for_status()
        return 0
