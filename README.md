1. install mininet
    - (mininet/util/install.sh)
    - sudo pip3 install mininet

2. install floodlight

3. start floodlight
    - cd ~/floodlight
    - java -jar target/floodlight.jar

4. run topo.py
    - sudo python3 ./topo.py
    - (sudo mn -c) -> for clearing the topology data.

5. run load balancer
    - sudo python3 ./net_ctrl.py
