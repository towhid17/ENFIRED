nRouters = 2
device_per_router = 3
nDevices = nRouters * device_per_router
nApps = nDevices
nFog = 6
nSwitches = nRouters * 2 + nFog + 2
cluster_size = 2
cluster_overlap = 0

nearest_fog_link_delay = 10
link_delay_gap = 25

delay_pre_calc = [70, 250, 400, 700]
ratio_sensitive_tolerant = 0.5

fog_capacity_threshold = 9.5
cloud_capacity_threshold = 13.5

exp_id = "enfired_11.0.1"
exp_category = "delay"
algo = "enfired"

sim_time = 1500
avg_delay_between_req = 1
iperf_interval = 10
iperf_period = 15
background_load = 9.9

sample_size = 10
sample_period = 1

delay_update_period = 5

load_balance_period = 5

device_load = '0.5M'
