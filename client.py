import socket
import ssl

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
DISCONNECT_MESSAGE = "Disconnected"
ADDR = (SERVER, PORT)



# Create an SSL context
context                     = ssl.SSLContext()
context.verify_mode         = ssl.CERT_REQUIRED

# Load CA certificate with which the client will validate the server certificate
context.load_verify_locations("./certifile.pem")

# Load client certificate
context.load_cert_chain(certfile="./certifile.pem", keyfile="./mykey.pem")


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Make the client socket suitable for secure communication
secureClientSocket  = context.wrap_socket(client)
secureClientSocket.connect(ADDR)
# Obtain the certificate from the server
server_cert = secureClientSocket.getpeercert()
# print(server_cert)
# Validate whether the Certificate is indeed issued to the server
subject         = dict(item[0] for item in server_cert['subject'])
organization      = subject['organizationName']

if not server_cert:
    raise Exception("Unable to retrieve server certificate")
    
if organization != 'ISU':
    raise Exception("Incorrect organization in server certificate")
print(secureClientSocket.recv(2048).decode(FORMAT))

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    secureClientSocket.send(send_length)
    secureClientSocket.send(message)

    

x = input()
send(x)
print(secureClientSocket.recv(2048).decode(FORMAT))

