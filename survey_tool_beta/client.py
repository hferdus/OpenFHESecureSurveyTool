import socket
import shutil
import os
from tfhe_encryptor_subscript import main_encryption
from tfhe_encryptor_subscript import partial_decrypt
import threading
import zipfile

HOST = "127.0.0.1"  # The server's hostname or IP address

FORMAT = "utf-8"                                     
SIZE = 1024
BYTEORDER_LENGTH = 8


def func_1():

	PORT = 65451  # The port used by the server
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	sock.connect((HOST, PORT))


	main_encryption()

	shutil.make_archive('zip_content_initial', 'zip','/home/christopherjoseph/Downloads/survey_tool_beta_version/client_stor/initial/' )
	 
	file_size = os.path.getsize('zip_content_initial.zip')
	print("File Size is :", file_size, "bytes")
	file_size_in_bytes = file_size.to_bytes(BYTEORDER_LENGTH, 'big')

	print("Sending the file size")
	sock.send(file_size_in_bytes)
	msg = sock.recv(SIZE).decode(FORMAT)                    
	print(f"[SERVER]: {msg}")

	print("Sending the file name")
	sock.send("zip_content_initial.zip".encode(FORMAT))           
	msg = sock.recv(SIZE).decode(FORMAT)                    
	print(f"[SERVER]: {msg}")  

	print("Sending the file data")    
	with open ('zip_content_initial.zip','rb') as f1:
		sock.send(f1.read())  
	msg = sock.recv(SIZE).decode(FORMAT)
	print(f"[SERVER]: {msg}")

	sock.close()
	
def func_2():

	PORT = 65459

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
		with open('/home/christopherjoseph/Downloads/survey_tool_beta_version/client_stor/zips/'+filename, 'wb') as f:
			f.write(packet)

		print(f"[RECV] File data received.")
		client[0].send("File data received".encode(FORMAT))
		client[0].close()

		archive = zipfile.ZipFile('/home/christopherjoseph/Downloads/survey_tool_beta_version/client_stor/zips/zip_content_computed.zip')

		for file in archive.namelist():
			archive.extract(file, '/home/christopherjoseph/Downloads/survey_tool_beta_version/client_stor/computed/')


		client.close()
		
		partial_decrypt()
		
def func_3():

	PORT = 65468
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	sock.connect((HOST, PORT))



	shutil.make_archive('zip_content_final', 'zip','/home/christopherjoseph/Downloads/survey_tool_beta_version/client_stor/final/' )
	 
	file_size = os.path.getsize('zip_content_final.zip')
	print("File Size is :", file_size, "bytes")
	file_size_in_bytes = file_size.to_bytes(BYTEORDER_LENGTH, 'big')

	print("Sending the file size")
	sock.send(file_size_in_bytes)
	msg = sock.recv(SIZE).decode(FORMAT)                    
	print(f"[SERVER]: {msg}")

	print("Sending the file name")
	sock.send("zip_content_final.zip".encode(FORMAT))           
	msg = sock.recv(SIZE).decode(FORMAT)                    
	print(f"[SERVER]: {msg}")  

	print("Sending the file data")    
	with open ('zip_content_final.zip','rb') as f1:
		sock.send(f1.read())  
	msg = sock.recv(SIZE).decode(FORMAT)
	print(f"[SERVER]: {msg}")

	sock.close()

if __name__ =="__main__":
    t1 = threading.Thread(target=func_1)
    t2 = threading.Thread(target=func_2)
    t3 = threading.Thread(target=func_3)

    t1.start()
    t1.join()
    
    t2.start()
    t2.join()
    
    t3.start()
    t3.join()
