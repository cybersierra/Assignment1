#PURPOSE: server-side implementation for client-server communication that can accept multiple connections

import socket
import threading
import base64 #for encoding and decoding data
from Crypto.Cipher import AES #we'll use AES for encryption and decryption
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad #for padding the data to be encrypted

#=======================
#   Encryption stuff    
#=======================

key = b"0123456789012345" #key ofr encryption and decryption

#=======================
#   Decryption stuff
#=======================

def decrypt(encryptedMessage, key):
    encryptedBytes = base64.b64decode(encryptedMessage) #decode the base64 encoded message
    iv = encryptedBytes[:16] #get the iv from the first 16 bytes
    encryptedData = encryptedBytes[16:] #get the encrypted data from the rest of the bytes
    cipher = AES.new(key, AES.MODE_CBC, iv) #create a new AES cipher object in cipher block chaining mode
    decrypted = cipher.decrypt(encryptedData) #decrypt the data
    return unpad(decrypted, AES.block_size).decode() #decrypt the data, unpad it, and decode it

def handleClient(clientSocket):
    while True:
        try:
            data = clientSocket.recv(1024).decode()
            if not data:
                break
            decryptedMessage = decrypt(data, key)
            print("Client:", decryptedMessage)
            clientSocket.sendall("Message received".encode())
        except Exception as e:
            print("An error occurred: " + str(e))
            break
    clientSocket.close()

#=======================
#   Server setup stuff
#=======================

try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a socket object
        #socket.AF_INET is the address family for IPv4
        #socket.SOCK_STREAM is the socket type for TCP connection
    serverSocket.bind(("127.0.0.1", 5000)) #bind the socket to the localhost and port 5000
    serverSocket.listen(5) #listen for incoming connections, with a maximum of 1 connections
    print("Socket created successfully")
except socket.error as err:
    print("Socket creation failed with error: " + str(err))

print("Waiting for connection...")

while True:
    client, address = serverSocket.accept() #accept the client's connection request
    threading.Thread(target=handleClient, args=(client,)).start()
    print("Connection established with: " + str(address)) #print the client's address