import socket   # the import is required for the project 
import sys  # allows reading from stdin
import select # the import allows us to use select()
peer_to_peer_socket_exist=False




ip = sys.argv[1] # get the manager ip
mport=int(sys.argv[2]) # get the manager port
peer_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # create the socket


while True:
    if peer_to_peer_socket_exist:
    select(sys.stdin) # to be able to read read the two inputs to watch
    else:
        select(sys.stdin)
message = input("Please enter with | as spaces")  # | so we dont have to replace spaces 
mess_fields=message.split("|")
peer_socket.sendto(message.encode(),(ip,mport)) #sent the messages
reply , addy =peer_socket.recvfrom(2048) #number comes from the sildes
reply_text=reply.decode()
reply_fields=reply_text.split("|")
    if mess_fields[0]=="register" and reply_fields[0]=="SUCCESS": # check if the register worked
        peer_to_peer_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # create the socket
        peer_to_peer_socket.bind(("",int(mess_fields[4])))
        peer_to_peer_socket_exist=True


