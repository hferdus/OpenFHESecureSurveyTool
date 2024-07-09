# multiconn-client.py

import sys
import socket
import selectors
import types

print("-----Program Start-----")
sel = selectors.DefaultSelector()
num_conns = int(input("Enter the number of clients: "))

messages = ["Message 1 from client.", "Message 2 from client."]

def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print(f"Starting connection {connid} to {server_addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(
            connid=connid,
            msg_total=2,
            recv_total=0,
            messages=messages.copy(),
            outb="",
        )
        sel.register(sock, events, data=data)

# ...

def service_connection(key, mask):
	sock = key.fileobj
	data = key.data
	if mask & selectors.EVENT_READ:
		recv_data = sock.recv(1024).decode()  # Should be ready to read
		if recv_data:
			print(f"Received {recv_data!r} from connection {data.connid}")
			data.recv_total += len(recv_data)
		
		if not recv_data or data.recv_total == data.msg_total:
			print(f"Closing connection {data.connid}")
			sel.unregister(sock)
			sock.close()

	if mask & selectors.EVENT_WRITE:
		if not data.outb and data.messages:
			data.outb = data.messages.pop(0)
		if data.outb:
			print(f"Sending {data.outb!r} to connection {data.connid}")
			sent = sock.send(bytes(data.outb,encoding="utf-8"))
			data.outb = data.outb[sent:]
		
start_connections("127.0.0.1",65429,num_conns)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()
