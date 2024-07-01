import socket
import os
from comp import comp_action

def count_files_in_directory(directory):
    # List all files in the directory
    files = os.listdir(directory)
    # Count the number of files
    return len(files)

def receive_file(conn):
	try:
		while True:
			numb = count_files_in_directory("/home/christopherjoseph/Downloads/alpha_version/server_stor/created")
			
			if current_count >= 11:
			 	break
			else:
				file_name_size = conn.recv(8)
				if not file_name_size:
					return False
				file_name_size = int.from_bytes(file_name_size, byteorder='big')
				file_name = conn.recv(file_name_size).decode('utf-8')
				file_size = int.from_bytes(conn.recv(8), byteorder='big')
				received_data = b''
				while len(received_data) < file_size:
					part = conn.recv(1024)
					if not part:
						break
					received_data += part
			
				save_path = f'/home/christopherjoseph/Downloads/alpha_version/server_stor/created/{file_name}'
				with open(save_path, 'wb') as f:
					f.write(received_data)
				print(f"Received {file_name}")
				return True
	except Exception as e:
			print(f"Error receiving file: {e}")
			return False
        
        
def send_file(sock,file_path):
	with open(file_path, 'rb') as f:
		data = f.read()
		file_name = os.path.basename(file_path)
		file_name_size = len(file_name).to_bytes(8, byteorder='big')
		sock.sendall(file_name_size)  # send file name size
		sock.sendall(file_name.encode('utf-8'))  # send file name
		sock.sendall(len(data).to_bytes(8, byteorder='big'))  # send file size
		sock.sendall(data)  # send file data
		print(f"Sent {file_name}")
		

	
def main_action():
	
	print("\n-----Program Start-----\n")
	
	host = '127.0.0.1'
	port = 8086

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((host, port))
	sock.listen()

	print("\nInitiating Client\n")
	sock.accept()
	print('Connected with client.')
	
	while True:
		response = receive_file(sock)
		if not response:
			break
		
	
	datafolder = "/home/christopherjoseph/Downloads/alpha_version/server_stor/created"
	div_avg = comp_action(datafolder)
	
	folder_path = "/home/christopherjoseph/Downloads/alpha_version/server_stor/computed"
	
	for file_name in os.listdir(folder_path2):
		file_path = os.path.join(folder_path, file_name)
		if os.path.isfile(file_path) and file_path.endswith('.txt'):  # ensure it's a .txt file
			send_file(sock, file_path)
	
	raw_data = sock.recv(1024)
	
	decod_data = raw_data.decode('utf8')
	
	avg = int(decod_data)
	
	avg = avg*div_avg
	
	print(f"The average user response is {avg}.")
	
if __name__ == "__main__":
	main_action()
		

