from socket import *
import socket
import threading
import time
import sys
import json
import logging
from chat import Chat
from client import ChatClient


REALM_IP = '127.0.0.1'
REALM_PORT = 12377
chatserver = Chat(REALM_IP, REALM_PORT)

from file_protocol import FileProtocol
fp = FileProtocol()

class ProcessTheClient(threading.Thread):
	def __init__(self, connection, address):
		self.connection = connection
		self.address = address
		threading.Thread.__init__(self)

	def run(self):
		rcv=""
		while True:
			data = self.connection.recv(512)
			if data:
				d = data.decode()
				rcv=rcv+d
				if rcv[-2:]=='\r\n':
					#end of command, proses string
					logging.warning("data dari client: {}" . format(rcv))

					# if first word of rcv is data
					if rcv.split(" ")[0].lower() == "data" or rcv.split(" ")[0].lower() == "get":
						hasil = fp.proses_string(rcv)
					else:
						hasil = json.dumps(chatserver.proses(rcv))			
							
					
					hasil_dict = json.loads(hasil)
					
					if hasil_dict['status'] == 'NAV':
						server_as_client = ChatClient(hasil_dict['ip'], hasil_dict['port'], is_server=True, real_username=hasil_dict['username_fr'])
						real_username=hasil_dict['username_fr']
						print("server token id: ", server_as_client.tokenid)
						rcv = rcv.split(" ")
						rcv = self.construct_string(rcv[0], rcv[2:])

						print("SINI AFTER : ", rcv)
						resp = json.dumps(server_as_client.proses(rcv))
						resp = resp + "\r\n\r\n"
						self.connection.sendall(resp.encode())
						# print("hasil ",hasil)

						# if hasil['status'] == 'OK':
						# 	resp = {'status': 'OK', 'message': 'Okay'}
						# 	hasil = json.dumps(resp)

						# elif "error" in hasil.lower():
						# 	resp = {'status': 'ERROR', 'message': 'Error'}
						# 	hasil = json.dumps(resp)

						# close the connection
						server_as_client.sock.close()
						rcv = ""
						continue
					
					hasil = hasil + "\r\n\r\n"
					
					logging.warning("balas ke  client: {}" . format(hasil))
					self.connection.sendall(hasil.encode())

					rcv=""
			else:
				break
		self.connection.close()

	def construct_string(self, command, parts):
		# print all part

		command = command + " "
		for part in parts:
			command = command + part + " "

		command = command + "\r\n"
		
		return command
		
	

class Server(threading.Thread):
	def __init__(self):
		self.the_clients = []
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		threading.Thread.__init__(self)

	def run(self):
		self.my_socket.bind(('0.0.0.0',REALM_PORT))
		self.my_socket.listen(1)
		while True:
			self.connection, self.client_address = self.my_socket.accept()
			logging.warning("connection from {}" . format(self.client_address))
			
			clt = ProcessTheClient(self.connection, self.client_address)
			clt.start()
			self.the_clients.append(clt)
	

def main():
	svr = Server()
	svr.start()

if __name__=="__main__":
	main()