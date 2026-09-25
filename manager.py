#!/usr/bin/python3
import socket   # the import is required for the project 
import random 

peers= {} # stores all the info on each peer
members={} # stores members of the DHT


def register_peer(command): # given in the form of register|(peer-name)(IPv4-address)|(m-port)|(p-port)
    fields=command.split("|")
    peer_name = fields[1] # grab the name 
    Ipv4 = fields[2]   # grab the ip addy
    mport = int(fields[3])  # grab the mport
    pport = int(fields[4]) # grab the pport 

    if peer_name in peers: # check if names are unique 
       return "FAILURE|names must be unique"
    if mport==pport: # check if ports match
        return "FAILURE|Port can not be the same"
    for people in peers.values():   #check if ports are not unqiue 
       used=(people["m_port"], people["p_port"])   
       if mport in used or pport in used:
          return "FAILURE|ports must be unique"

    peers[peer_name]= {"ipv4":Ipv4, "m_port":mport, "p_port":pport, "state":"Free"} 
    return  "SUCCESS"

def setup_dht(command): # given in the form of setup-dht|(peer-name)|(n)|(YYYY)
   fields=command.split("|") # splits the string to get the imporent value 
   peer_name=fields[1]  # gets name
   number=int(fields[2]) # gets N
   year=int(fields[3]) #gets the year 
   if (not(peer_name in peers)):      # all of these handle falure conditions
      return "FAILURE|PEER NOT REGISTERED"
   if number<3:
      return "FAILURE|N MUST BE 3 OR GREATER"
   if len(peers)<number:
      return "FALURE|NOT ENOUGH MEMEBRS"
   if members:    # empty dictionary are false 
      return "FALURE|DHT SET UP BEFOREHAND"
   peers[peer_name]["state"]="Leader"

   members[peer_name]={"ipv4":peers[peer_name]["ipv4"],"p_port":peers[peer_name]["p_port"],"id":0} # will make the printing easier
   free_peers=[] # the list only needs to keep track of names
   for peer in peers: #get every free peer
      if peers[peer]["state"]=="Free":
         free_peers.append(peer) 
   chosen=random.sample(free_peers,number-1) # the python random libary coming in
   start_id=1
   for peer in chosen:
      members[peer]={"ipv4":peers[peer]["ipv4"],"p_port":peers[peer]["p_port"],"id":start_id} # add the peer to the members
      peers[peer]["state"]="InDHT"
      start_id+=1
   strings=[] #lets us use a return statment with all the strings
   for peer in members:
      strings.append(peer+","+str(members[peer]["ipv4"])+","+str(members[peer]["p_port"])) 
      #/ the str conver the ports and the ip to strings so they can be added/#
   return "SUCCESS|"+"|".join(strings)
   



   
   
