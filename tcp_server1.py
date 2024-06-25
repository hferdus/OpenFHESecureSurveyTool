import socket
import json
import os

from enc import dec
def main_action():

	# Defining Socket
	host = '127.0.0.1'
	port = 8085
	client_num = int(input("Enter the number of clients: "))

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((host,port))
	sock.listen(client_num)

	# Estabilishing connections
	connections = []
	print("\n Initiating Clients \n")
	for i in range(client_num):

		conn = sock.accept()
		connections.append(conn)
		print('Connected with client',i+1)

	fileno = 0
	idx = 0
	for conn in connections:
	# Receiving file data
		idx += 1
		
		# Ciphertext
		data_1 = ""
		while True:
			part = conn[0].recv(4096)  # a smaller, more manageable buffer size
			if not part:
				break
			data_1 += part.decode("utf-8")
			
			
		data_1 = json.dumps(data_1)
		print(type(data_1))
		filename = '/home/christopherjoseph/Downloads/test/server_stor/ciphertext.json'

		fo = open(filename,"w")


		if not data_1:
				break
		else:
				fo.write(data_1)

		fo.close()
		
		
	dec()

	for conn in connections:
		conn[0].close()

if __name__ == '__main__':

	main_action()
