import socket   # the import is required for the project 
import sys  # allows reading from stdin




ip = sys.argv[1] # get the manager ip
port=int(sys.argv[2]) # get the manager port
peer_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # create the socket


while True:
    message = input("Please enter with | as spaces")  # | so we dont have to replace spaces 
    peer_socket.sendto(message.encode(),(ip,port)) #sent the messages
    reply , addy =peer_socket.recvfrom(2048) #number comes from the sildes
    print(reply.decode())
