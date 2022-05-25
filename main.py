from PBFT import *
from client import *

import threading
import time

# Parameters to be defined by the user

waiting_time_before_resending_request = 200 # Time the client will wait before resending the request. This time, it broadcasts the request to all nodes
timer_limit_before_view_change = 200 # There is no value proposed in the paper so let's fix it to 120s
checkpoint_frequency = 100 # 100 is the proposed value in the original article

# Define the proportion of nodes we want in the consensus set
p = 1

# Define the nodes we want in our network + their starting time + their type
print(">> 1) Environment nodes setup ")
nodes={} # This is a dictionary of nodes we want in our network. Keys are the nodes types, and values are a list of tuples of starting time and number of nodes 
#nodes[starting time] = [(type of nodes , number of nodes)]
faulty_primary = 0 
slow_nodes = 0
honest_node = 40
non_responding_node = 0
faulty_node = 0
faulty_replies_node = 0

nodes[0]=[("faulty_primary",faulty_primary),("slow_nodes",slow_nodes),("honest_node",honest_node),("non_responding_node",non_responding_node),("faulty_node",faulty_node),("faulty_replies_node",faulty_replies_node)] # Nodes starting from the beginning
print("  faulty_primary %d,  slow_nodes %d, honest_node %d \n  non_responding_node %d, faulty_node %d, faulty_replies_node %d"%(faulty_primary, slow_nodes, honest_node, non_responding_node, faulty_node, faulty_replies_node))
#nodes[1]=[("faulty_primary",0),("honest_node",1),("non_responding_node",0),("slow_nodes",1),("faulty_node",1),("faulty_replies_node",0)] # Nodes starting after 2 seconds
#nodes[2]=[("faulty_primary",0),("honest_node",0),("non_responding_node",0),("slow_nodes",2),("faulty_node",1),("faulty_replies_node",0)]

# Running APBFT protocol
run_APBFT(nodes=nodes,proportion=p,checkpoint_frequency0=checkpoint_frequency,clients_ports0=clients_ports,timer_limit_before_view_change0=timer_limit_before_view_change)

print("\n>> 2) Starting network...")
time.sleep(1)  # Waiting for the network to start...
print("Network online ")

# Run clients:
print("\n>> 3) Clients request")
requests_number = 1  # The user chooses the number of requests he wants to execute simultaneously (They are all sent to the PBFT network at the same time) - Here each request will be sent by a different client
print("  [clients_number: '%d', 'client_request_interval: '%d']"%(requests_number, waiting_time_before_resending_request))
clients_list = []
for i in range(requests_number):
    globals()["C%s" % str(i)] = Client(i, waiting_time_before_resending_request)
    clients_list.append(globals()["C%s" % str(i)])
for i in range (requests_number):
    threading.Thread(target=clients_list[i].send_to_primary,args=("I am the client "+str(i),get_primary_id(),get_nodes_ids_list(),get_f())).start()
    time.sleep(1) #Exécution plus rapide lorsqu'on attend un moment avant de lancer la requête suivante
