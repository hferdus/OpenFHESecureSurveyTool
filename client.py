import socket
import os
from enc import enc_action
from enc import partial_dec
def receive_file(conn):
    try:
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
        save_path = f'/home/christopherjoseph/Downloads/alpha_version/client_stor/computed/{file_name}'
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
		
def start_connection():

	host = '127.0.0.1'
	port = 8086
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((host, port))
	
	return sock

def main_action():

	print("\n-----Program Start-----\n")
	
	
	num_people = int(input("How many people do you want to answer this survey?: "))
	num_questions = int(input("How many question do you want the simulated survey to have?: "))
	
	
	enc_action(num_people,num_questions)
	sock = start_connection()
	
	
	
	folder_path1 = '/home/christopherjoseph/Downloads/alpha_version/client_stor/initial/'
	
	for file_name in os.listdir(folder_path1):
		file_path = os.path.join(folder_path1, file_name)
		if os.path.isfile(file_path) and file_path.endswith('.txt'):  # ensure it's a .txt file
			send_file(sock, file_path)
	while True:
		response = receive_file(sock)
		if not response:
			break
	
	avg = partial_dec()
	
	sock.send(str(avg).encode('utf8'))
			
	sock.close()
	
	print("\n-----Program End-----\n")
if __name__ == "__main__":
	main_action()
