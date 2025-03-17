#PURPOSE: client-side implementation for client-server communication.

# you need to install pycryptodome using 'pip install pycryptodome'

import socket

#=======================
#   Encryption stuff
#=======================
# comments for context are in server.py
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

key = b"0123456789012345"

def encrypt(message, key):
    cipher = AES.new(key, AES.MODE_CBC ) #create a new AES cipher object in cipher block chaining mode
    encryptedBytes = cipher.encrypt(pad(message.encode(), AES.block_size)) #encrypt the message and pad it to the block size
    return base64.b64encode(cipher.iv + encryptedBytes).decode() #encode the iv and encrypted bytes in base64 and return it as a string

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a socket object
clientSocket.connect(("127.0.0.1", 5000)) #connect to the server

while True:
    message = input("Your message: ")
    if message.lower() == "exit":
        break
    encryptedMessage = encrypt(message, key)
    clientSocket.sendall(encryptedMessage.encode())

    response = clientSocket.recv(1024).decode()
    print("Server:", response)

clientSocket.close()