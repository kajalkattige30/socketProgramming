# This is a simple program to get basic understanding of sockets and how they work

# Sockets work on the client-server model.

import socket
import ssl
from datetime import datetime



HEADER = 64
# need to pick a port the server will be running on
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
# print(SERVER)
ADDR = (SERVER, PORT) # address needs to be a tuple containing first the server address and then the port which it is running off of
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "disconnect"
# Pick a socket to bind it to that address

# To create a new socket :
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# to bind the socket to an address
server.bind(ADDR) 




def start(): 
    server.listen()
    print(f"[LISTENING] server is listening on {SERVER}")
    connected = True
    while(connected):
        # It waits for a new connection to the server, when a new connection occurs, it will store the address of the connection (IP and port address it came from) and also store a connection object(conn) that is going to send information back to the connection 
        conn, addr = server.accept() 
        # Make the socket connection to the client secure through SSLSocket
        secure_client_socket = ssl.wrap_socket(conn, server_side=True,ca_certs="./certifile.pem", certfile="./certifile.pem", keyfile="./mykey.pem",cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_TLSv1)
        print(f"[NEW CONNECTION] {addr} connected.")
        secure_client_socket.send("Type 1 to ask Server for current time \nType 2 to ask Server for IP of local host\nType 'disconnect' to quit".encode(FORMAT))
         # Get certificate from the client
        client_cert = secure_client_socket.getpeercert()
        # print(client_cert)
        clt_subject    = dict(item[0] for item in client_cert['subject'])
        clt_organization = clt_subject['organizationName']

        # Check the client certificate bears the expected name as per server's policy
        if not client_cert:
            raise Exception("Unable to get the certificate from the client")
        if clt_organization != 'ISU':
            raise Exception("Incorrect organization in client certificate")
        msg_length = secure_client_socket.recv(HEADER).decode(FORMAT)
        if(msg_length):
            msg_length = int(msg_length)
            msg = secure_client_socket.recv(msg_length).decode(FORMAT)
            if(msg == DISCONNECT_MESSAGE):
                connected = False
            elif(msg == "1"):
                now = datetime.now()
                current_time = now.strftime("%Y/%m/%d, %H:%M:%S")
                secure_client_socket.send(current_time.encode(FORMAT))
            elif(msg == "2"):
                secure_client_socket.send(SERVER.encode(FORMAT))
            else:
                secure_client_socket.send("Wrong input!".encode(FORMAT))
                connected = False
        secure_client_socket.close()

print("[STARTING] server is starting...")
start()