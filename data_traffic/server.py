import json
import socket
import sys


def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    # s.listen(5)
    print("Server is listening on {}:{}".format(HOST, PORT))

    # try:
        # conn, addr = s.accept()
        # print("Connected by", addr)
    while True:
        # data = conn.recv(2048)
        # json_data = json.loads(data.decode('utf-8'))
        data, addr = s.recvfrom(1024)
        json_data = data.decode()
        parsed_data = json.loads(json_data)
        print("Received JSON data:", parsed_data)
    # finally:
    #     conn.close()
    # s.close()


if __name__ == "__main__":
    HOST = sys.argv[1]
    PORT = 12345
    start_server()
