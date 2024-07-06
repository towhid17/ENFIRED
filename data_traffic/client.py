import socket
import sys
import time

sys.path.append('../Final')

import data_traffic.data_sample as ds
import conf.exp_conf as ip


def start_data_transmission(HOST, PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect((HOST, PORT))

    while True:
        start_time = time.time()
        ds.sent_sample(s, HOST, PORT)
        end_time = time.time()
        print("delay: "+str((end_time-start_time)*1000))
        time.sleep(ip.sample_period)
    s.close()


if __name__ == "__main__":
    HOST = sys.argv[1]
    PORT = 12345
    start_data_transmission(HOST, PORT)
