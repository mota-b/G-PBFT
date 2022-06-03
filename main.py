# Dependencies
from os import environ
from PBFT import *
from client import *

import threading
import time
import asyncio

# Time parameters
START_CLIENTS_TIMEOUT = 1 # Start clients 'x' seconds after the environment config
REQUEST_INTERVAL = 200 # Time the client will wait before resending the request. This time, it broadcasts the request to all nodes

VIEW_CHANGES_TIMEOUT = 1000 # There is no value proposed in the paper so let's fix it to 120s
CHECKPOINT_FREQUENCY = 1000 # 100 is the proposed value in the original article


# Nodes parameters
HONEST_NODES = 40

SLOW_NODES = 0
NONE_RESPONDING_NODES = 0

FAULTY_NODES = 0
FAULTY_PRIMARY_NODES = 0
FAULTY_REPLIES_NODES = 0


# Methodes
def startEnvironment():
    # Define the nodes we want in our network by type
    print("\n\n>> A] Environment setup ")
    print("\n\t> Nodes types config ")
    print("\t\t- honest_node %d"%(HONEST_NODES)
    +"\n\t\t- slow_nodes %d"%(SLOW_NODES)
    +"\n\t\t- non_responding_node %d"%(NONE_RESPONDING_NODES)
    +"\n\t\t- faulty_nodes %d"%(FAULTY_NODES)
    +"\n\t\t- faulty_primary_nodes %d"%(FAULTY_PRIMARY_NODES)
    +"\n\t\t- faulty_replies_node %d"%(FAULTY_REPLIES_NODES))

    starting_time = 0
    nodes_config={} # This is a dictionary of nodes we want in our network. Keys are the nodes types, and values are a list of tuples of starting time and number of nodes 
    nodes_config[starting_time]=[ #nodes[starting time] = [(type of nodes , number of nodes)]
        ("honest_node",HONEST_NODES),
        ("slow_nodes",SLOW_NODES),
        ("non_responding_node",NONE_RESPONDING_NODES),
        ("faulty_node",FAULTY_NODES),
        ("faulty_primary",FAULTY_PRIMARY_NODES),
        ("faulty_replies_node",FAULTY_REPLIES_NODES)
    ] # Nodes starting from the beginning
    
    # Runn APBFT protocol
    print("\n\n>> B] start PBFT ")
    asyncio.run(run_APBFT(nodes_config, VIEW_CHANGES_TIMEOUT, CHECKPOINT_FREQUENCY))
def startClient():
    print("\n\n>> C] start Client ")
    requests_number = 1  # The user chooses the number of requests he wants to execute simultaneously (They are all sent to the PBFT network at the same time) - Here each request will be sent by a different client

    # create clients
    print("\n\n\t> C.1) Clients creation")
    clients_list = []
    for i in range(requests_number):
        globals()["C%s" % str(i)] = Client(i, REQUEST_INTERVAL)
        clients_list.append(globals()["C%s" % str(i)])
        print("\t\tclients-%d, 'client_request_interval: %d, client_port: %d'"%(requests_number, REQUEST_INTERVAL, globals()["C%s" % str(i)].client_port))
    
    
    # trigger client request
    for i in range (requests_number):
        # nodes_ids_list = get_nodes_ids_list()
        consensus_nodes_ids_list = get_consensus_nodes_ids_list()
        primary_id = get_primary_id()
        permitted_faulty_nodes_number = get_faulty_nodes_number_permitted()
        
        threading.Thread(target=clients_list[i].send_to_primary,args=("I am the client "+str(i),primary_id,consensus_nodes_ids_list, permitted_faulty_nodes_number)).start()
        time.sleep(1) #Exécution plus rapide lorsqu'on attend un moment avant de lancer la requête suivante
def main():
    # start environment
    startEnvironment()

    # start clients:
    time.sleep(START_CLIENTS_TIMEOUT)  # Waiting for the network to start...
    startClient()


if __name__ == "__main__":
    main()