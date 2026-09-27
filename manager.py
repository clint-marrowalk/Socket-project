#!/usr/bin/python3
import socket as s   # the import is required for the project 
import random   # to be ablue to select at random
import sys # to read from stdin

peers= {} # stores all the info on each peer
members={} # stores members of the DHT
block = False # to blocks until dht_complte

def register_peer(command): # given in the form of register|(peer-name)|(IPv4-address)|(m-port)|(p-port)
    fields=command.split("|")
    peer_name = fields[1] # grab the name 
    Ipv4 = fields[2]   # grab the ip addy
    mport = int(fields[3])  # grab the mport
    pport = int(fields[4]) # grab the pport 

    if not(peer_name.isalpha()) or len(peer_name)>=16:
      return "FAILURE|names must be aphabetic and at most 15 charaters long"
    elif peer_name in peers: # check if names are unique 
       return "FAILURE|names must be unique"
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
   if (not(peer_name in peers)):      # all of these handle failure conditions
      return "FAILURE|PEER NOT REGISTERED"
   elif number<3:
      return "FAILURE|N MUST BE 3 OR GREATER"
   elif len(peers)<number:
      return "FAILURE|NOT ENOUGH MEMEBRS"
   elif members:    # empty dictionary are false 
      return "FAILURE|DHT SET UP BEFOREHAND"
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
   global block
   block=True # can't take commands till dht complte   
   return "SUCCESS|"+"|".join(strings)

def dht_complete(command): # given in the form of dht-complete|(peer-name)
   fields=command.split("|")
   peer_name=fields[1]
   if not(peer_name in members):
      return "FAILURE|"+peer_name+"not in the DHT"
   elif not (members[peer_name]["id"]==0):
      return "FAILURE|setup with "+peer_name+" as leader"
   else:
      global block
      block=False # can now take commands 
      return "SUCCESS|now accpeting commands"


port = int(sys.argv[1]) #read the port from standerd input 
host_socket=s.socket(s.AF_INET,s.SOCK_DGRAM) # create the socket
host_socket.bind(("",port)) # bind the socket
while True:
   message,client_addy = host_socket.recvfrom(2048) #number comes from the sildes
   decoded_mess=message.decode()
   fields=decoded_mess.split("|") 

   if block and fields[0] != "dht-complete": # prevents from running till dht-complete
      reply="FAILURE|DHT under construcion"
   elif fields[0]=="register":    # checks for which commands to use
      reply=register_peer(decoded_mess)
   elif fields[0]=="setup-dht":
      reply=setup_dht(decoded_mess)
   elif fields[0]=="dht-complete":
      reply=dht_complete(decoded_mess)
   else:
      reply= "FAILURE|Command not recognized"
      
   host_socket.sendto(reply.encode(),client_addy) # format from the slides

