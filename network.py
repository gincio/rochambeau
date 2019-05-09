# import socket
import pickle
from flask import Flask

class Network:
	def __init__(self):
	# informacje o połączeniu
		# self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client = Flask(__name__)
		self.server = "localhost"
		self.port = 5000
		self.addr = (self.server, self.port)
		self.p = self.connect()
		
	def getP(self):
		return self.p
		
	def connect(self):
	# połączenie z serwerem, od serwera dostajemy informację czy jesteśmy graczem 0 czy 1
		try:
			self.client.connect(self.addr)
			return self.client.recv(2048).decode()
		except:
			pass
			
	def send(self, data):
	# wysyłanie informacji na serwer (np o dokonanym wyborze)
		try:
			self.client.send(str.encode(data))
			return pickle.loads(self.client.recv(2048*2))
		except socket.error as e:
			print(e)