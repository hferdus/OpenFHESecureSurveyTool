# echo-server.py

import socket
import os 
import zipfile
from tfhe_decryptor_subscript import tfhe_decryptor_subscript

HOST = "127.0.0.1"  
PORT = 65459  
FORMAT = "utf-8"                                     
SIZE = 1024
BYTEORDER_LENGTH = 8

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.bind((HOST, PORT))
sock.listen(1)


while True:
    client = sock.accept()                                          
    print(f"\033[33m[*] Listening as {HOST}:{PORT}\033[m")                                                    
    print(f"\033[32m[!] Client connected {client[1]}\033[m")


    print(f"[RECV] Receiving the file size")
    file_size_in_bytes = client[0].recv(BYTEORDER_LENGTH)
    file_size= int.from_bytes(file_size_in_bytes, 'big')
    print("File size received:", file_size, " bytes")
    client[0].send("File size received.".encode(FORMAT))

    print(f"[RECV] Receiving the filename.")
    filename = client[0].recv(SIZE).decode(FORMAT)
    print(f"[RECV]Filename received:", filename)
    client[0].send("Filename received.".encode(FORMAT))

    print(f"[RECV] Receiving the file data.")
    # Until we've received the expected amount of data, keep receiving
    packet = b""  # Use bytes, not str, to accumulate
    while len(packet) < file_size:
        if(file_size - len(packet)) > SIZE:  # if remaining bytes are more than the defined chunk size
            buffer = client[0].recv(SIZE)  # read SIZE bytes
        else:
            buffer = client[0].recv(file_size - len(packet))  # read remaining number of bytes

        if not buffer:
            raise Exception("Incomplete file received")
        packet += buffer
    with open('/home/christopherjoseph/Downloads/epsilon_version/serv_stor/'+filename, 'wb') as f:
        f.write(packet)
        
    print(f"[RECV] File data received.")
    client[0].send("File data received".encode(FORMAT))
    client[0].close()
    
    archive = zipfile.ZipFile('/home/christopherjoseph/Downloads/epsilon_version/serv_stor/zip_content.zip')

    for file in archive.namelist():
      archive.extract(file, '/home/christopherjoseph/Downloads/epsilon_version/serv_stor/')
      
    tfhe_decryptor_subscript()
      
    
	
		




	

