import socket   # the import is required for the project 

peers= {} # stores all the info on each peer


def register_peer(command): # give in the form of register ⟨peer-name⟩ ⟨IPv4-address⟩ ⟨m-port⟩ ⟨p-port⟩
    fields=command.split("|")
    peer_name = fields[1] # grab the name 
    Ipv4 = fields[2]   # grab the ip addy
    mport = int(fields[3])  # grab the mport
    pport = int(fields[4]) # grab the pport 

    if peer_name in peers: # check if names are unique 
       return "FAILURE|names must be unique "
    if mport==pport:
        return "FAILURE|WHY WOULD YOUR PORTS BE MATCHING"
    for people in peers.values():   #check if ports are not unqiue 
       used=(people["m_port"], people["p_port"])   
       if mport in used or pport in used:
          return "FAILURE| ports must be unique"

    peers[peer_name]= {"ipv4":Ipv4, "m_port":mport, "p_port":pport, "state":"Free"} 
    return  "SUCCESS"


