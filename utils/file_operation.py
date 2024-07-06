import csv
import os
import fcntl
import shutil

import conf.exp_conf as ip

file_path = "core_files/"


def create_csv(file_name, items):
    with open(file_path + file_name, 'w') as file1:
        writer = csv.writer(file1)
        for i in range(items):
            row = [i, 0]
            print(row)
            writer.writerow(row)
    file1.close()


# def update_csv(file_name, key, value, items):
#     with open(file_path + file_name, 'r') as file1:
#         reader = csv.reader(file1)
#         data = list(reader)
#     file1.close()
#
#     with open(file_path + file_name, 'w') as file1:
#         writer = csv.writer(file1)
#         print(data)
#         for i in range(items):
#             if i == key:
#                 row = [i, value]
#             else:
#                 row = [i, data[i][1]]
#             writer.writerow(row)
#     file1.close()


def update_csv(file_name, key, value, items):
    lock_path = os.path.join(file_path, f"{file_name}.lock")
    
    # Acquire a lock before modifying the file
    with open(lock_path, 'w') as lock_file:
        fcntl.flock(lock_file, fcntl.LOCK_EX)
        
        temp_data = []
        with open(os.path.join(file_path, file_name), 'r') as file1:
            reader = csv.reader(file1)
            for row in reader:
                if row and row[0] == str(key):
                    row[1] = str(value)
                temp_data.append(row)
        
        with open(os.path.join(file_path, file_name), 'w', newline='') as file1:
            writer = csv.writer(file1)
            writer.writerows(temp_data)
    
        # Release the lock after modifying the file
        fcntl.flock(lock_file, fcntl.LOCK_UN)


# def update_csv(file_name, key, value, items):
#     temp_data = []
#     with open(os.path.join(file_path, file_name), 'r') as file1:
#         reader = csv.reader(file1)
#         for row in reader:
#             if row and row[0] == str(key):
#                 row[1] = str(value)
#             temp_data.append(row)

#     with open(os.path.join(file_path, file_name), 'w', newline='') as file1:
#         writer = csv.writer(file1)
#         writer.writerows(temp_data)


def update_csv_list(file_name, keys, value, items):
    with open(file_path + file_name, 'r') as file1:
        reader = csv.reader(file1)
        data = list(reader)
    file1.close()

    with open(file_path + file_name, 'w') as file1:
        writer = csv.writer(file1)
        for i in range(items):
            if i in keys:
                row = [i, value]
            else:
                row = [i, data[i][1]]
            writer.writerow(row)
    file1.close()


def read_csv(file_name, items):
    device_data = []
    for i in range(items):
        device_data.append(0)

    with open(file_path + file_name, 'r') as file1:
        reader = csv.reader(file1)
        data = list(reader)
        print(data)
        for i in range(items):
            device_data[int(data[i][0])] = float(data[i][1])
    file1.close()
    return device_data


def create_device_load_csv():
    print("Creating device load csv")
    create_csv("device_load.csv", ip.nDevices)


def update_device_load_csv(fno, th):
    update_csv("device_load.csv", fno, th, ip.nDevices)


def read_device_load_csv():
    return read_csv("device_load.csv", ip.nDevices)


def create_fog_load_csv():
    create_csv("fog_load.csv", ip.nFog + 1)


def update_fog_load_csv(fno, th):
    update_csv("fog_load.csv", fno, th, ip.nFog + 1)


def read_fog_load_csv():
    return read_csv("fog_load.csv", ip.nFog + 1)


def create_device_delay_csv():
    print("Creating device delay csv")
    create_csv("device_delay.csv", ip.nDevices)


def read_device_delay_csv():
    print("Reading device delay csv")
    return read_csv("device_delay.csv", ip.nDevices)


def update_devices_delay_csv(devices, delay):
    print("Updating device delay csv")
    update_csv_list("device_delay.csv", devices, delay, ip.nDevices)


def update_device_delay_csv(device_no, delay):
    update_csv("device_delay.csv", device_no, delay, ip.nDevices)


# category 1 = sensitive, 0 = tolerant
def save_device_category_and_threshold(device_delay_threshold, delay_threshold_pre_calc):
    device_category = []
    with open("core_files/device_category.txt", 'w') as file1:
        for item in range(ip.nDevices):
            if device_delay_threshold[item] <= delay_threshold_pre_calc[1]:
                file1.write(str(item) + " 1\n")
                device_category.append(True)
            else:
                file1.write(str(item) + " 0\n")
                device_category.append(False)
    
    # copy device category to experiment folder
    shutil.copy("core_files/device_category.txt", "exp_results/" + ip.exp_id + "/device_category.txt")

    with open("core_files/delay_threshold_device.csv", 'w') as file1:
        for item in range(ip.nDevices):
            row = [item, device_delay_threshold[item]]
            writer = csv.writer(file1)
            writer.writerow(row)
    file1.close()

    # copy delay threshold to experiment folder
    shutil.copy("core_files/delay_threshold_device.csv", "exp_results/" + ip.exp_id + "/delay_threshold_device.csv")

    return device_category


def read_delay_threshold():
    return read_csv("delay_threshold_device.csv", ip.nDevices)


def save_fog_throughput(fog_throughput):
    with open("core_files/fog_throughput_" + ip.exp_id + ".txt", 'a') as file1:
        for i in range(len(fog_throughput)):
            if i % ip.nFog == 0:
                file1.write("\n")
            print(fog_throughput[i])
            file1.write(str(fog_throughput[i] / 1024) + "K\t")

    file1.close()


def save_fog_device_map(device_fog):
    with open("core_files/fog_device_map.txt", 'w') as file1:
        for item in range(ip.nDevices):
            file1.write(str(device_fog[item]) + "\n")
    file1.close()


def fog_device_map_read(device_fog):
    with open("core_files/fog_device_map.txt", 'r') as file1:
        for item in range(ip.nDevices):
            device_fog[item] = int(file1.readline())
    file1.close()


def save_delay_update_time_count_fog_id_delay(router_no, fog_no, delay, time_count):
    with open("core_files/delay_update_time_count_fog_id_delay.txt", 'a') as file1:
        file1.write(str(time_count) + "\t" + str(router_no) + "\t" + str(fog_no) + "\t" + str(delay) + "\n")
    file1.close()


def append_periodic_delay_update(file_name, received_timestamp):
    with open(file_name, 'a') as file1:
        for i in range(len(received_timestamp)):
            file1.write(str(received_timestamp[i]) + "\n")
    file1.close()


def delete_core_files():
    folder_path = "core_files"

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        try:
            # Iterate over each file in the folder
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"File '{file_path}' has been deleted.")
            
            print("All files in the folder have been deleted.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print(f"Folder '{folder_path}' does not exist.")


# write experiment configuration to file in exp_results/periodic_delay_update_<exp_id> directory
def write_exp_conf():
    # create directory if not exists
    if not os.path.exists("exp_results/" + ip.exp_id):
        os.makedirs("exp_results/" + ip.exp_id)
    with open("exp_results/" + ip.exp_id + "/exp_conf.txt", 'w') as file1:
        file1.write("Experiment ID: " + ip.exp_id + "\n")
        file1.write("algo: " + str(ip.algo) + "\n")
        file1.write("exp_category: " + str(ip.exp_category) + "\n")
        file1.write("Number of devices: " + str(ip.nDevices) + "\n")
        file1.write("Number of fog nodes: " + str(ip.nFog) + "\n")
        file1.write("Number of routers: " + str(ip.nRouters) + "\n")
        file1.write("fog_capacity_threshold: " + str(ip.fog_capacity_threshold) + "\n")
        file1.write("cloud_capacity_threshold: " + str(ip.cloud_capacity_threshold) + "\n")
        file1.write("iperf_interval: " + str(ip.iperf_interval) + "\n")
        file1.write("iperf_period: " + str(ip.iperf_period) + "\n")
        file1.write("load_balance_period: " + str(ip.load_balance_period) + "\n")
        file1.write("ratio_sensitive_tolerant: " + str(ip.ratio_sensitive_tolerant) + "\n")