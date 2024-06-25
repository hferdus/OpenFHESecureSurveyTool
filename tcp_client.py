import socket 
import chardet
from enc import enc

def detect_encoding(file_path): 
    with open(file_path, 'rb') as file: 
        detector = chardet.universaldetector.UniversalDetector() 
        for line in file: 
            detector.feed(line) 
            if detector.done: 
                break
        detector.close() 
    return detector.result['encoding'] 
    
    
  

def main_action():

	# Creating Client Socket
	
	host = '127.0.0.1'
	port = 8085

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	
	# Connectng with server
	
	sock.connect((host, port)) 

	

	sam_num = int(input('Input the number you want to send: '))
	enc(sam_num)
	
	path = '/home/christopherjoseph/Downloads/test/client_stor/ciphertext.json'
	
	with open(path,'r') as f:
		data_1 = f.read()
	print(type(data_1))	
		
		
	sock.send(bytes(data_1,encoding="utf-8"))
	
	path = '/home/christopherjoseph/Downloads/test/client_stor/cc.json'
	
	with open(path,'r') as f:
		data_1 = f.read()
		
	print(type(data_1))	
		
	sock.send(bytes(data_1,encoding="utf-8"))
	
	path = '/home/christopherjoseph/Downloads/test/client_stor/sk1.json'
	
	with open(path,'r') as f:
		data_1 = f.read()
		
	print(type(data_1))	
		
	sock.send(bytes(data_1,encoding="utf-8"))
	
	path = '/home/christopherjoseph/Downloads/test/client_stor/sk2.json'
	
	with open(path,'r') as f:
		data_1 = f.read()
		
	print(type(data_1))	
		
	sock.send(bytes(data_1,encoding="utf-8"))
	
	
if __name__ == '__main__': 
	main_action()
