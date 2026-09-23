import socket   # the import is required for the project 

peers= {} # stores all the info on each peer


def register_peer(command): # give in the form of register ⟨peer-name⟩ ⟨IPv4-address⟩ ⟨m-port⟩ ⟨p-port⟩
    fields=command.split("|")
    peer_name = fields[1]
    Ipv4 = fields[2]
    mport = fields[3]
    pport = fields [4]

    if peer_name in peers:
       return "FAILURE|names must be unique "
    for people in peers.values():
       used=(people[mport], people[pport])
       if mport in used or pport in used:
          return "FAILURE| ports must be unique"
       

    peers[peer_name]= {"ipv4":Ipv4, "m_port":mport, "p_port":pport, "state":"free"}

 
    return  "SUCCESS"





def setup_dht(command):
 fields=command.split("|")


 return "SUCCESS now listing  n peers that together will construct the DHT. "

