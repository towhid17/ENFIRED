1. install mininet 
    a. (mininet/util/install.sh)
    b. sudo pip3 install mininet

2. install floodlight

Running the program:
1. start floodlight
    a. cd ~/floodlight
    b. java -jar target/floodlight.jar

2. run topo.py
    sudo python3 ./topo.py

    (sudo mn -c) -> for clearing the topology data.

3. run load balancer
    sudo python3 ./net_ctrl.py


