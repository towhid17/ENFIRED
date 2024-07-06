import json


def generate_random_data():
    data = {
        "key_1": "value_1",
        "key_2": "value_2",
        "key_3": "value_3",
        "key_4": "value_4",
        "key_5": "value_5"
    }
    return data


def sent_sample(socket, host, port):
    json_data = generate_random_data()
    # print(json_data)
    json_str = json.dumps(json_data)

    # socket.sendall(json_str.encode('utf-8'))
    socket.sendto(json_str.encode(), (host, port))
    print("JSON data sent to server.")
