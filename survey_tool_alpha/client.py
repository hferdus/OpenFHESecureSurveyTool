import socket
import shutil
import os
from tfhe_encryptor_subscript import main_action

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65459  # The port used by the server
FORMAT = "utf-8"                                     
SIZE = 1024
BYTEORDER_LENGTH = 8

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.connect((HOST, PORT))


main_action()

shutil.make_archive('zip_content', 'zip','/home/christopherjoseph/Downloads/epsilon_version/gen_stor/' )
 
file_size = os.path.getsize('zip_content.zip')
print("File Size is :", file_size, "bytes")
file_size_in_bytes = file_size.to_bytes(BYTEORDER_LENGTH, 'big')

print("Sending the file size")
sock.send(file_size_in_bytes)
msg = sock.recv(SIZE).decode(FORMAT)                    
print(f"[SERVER]: {msg}")

print("Sending the file name")
sock.send("zip_content.zip".encode(FORMAT))           
msg = sock.recv(SIZE).decode(FORMAT)                    
print(f"[SERVER]: {msg}")  

print("Sending the file data")    
with open ('zip_content.zip','rb') as f1:
	sock.send(f1.read())  
msg = sock.recv(SIZE).decode(FORMAT)
print(f"[SERVER]: {msg}")

sock.close()
