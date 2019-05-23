# !/usr/bin/env python
# -*- coding: utf-8 -*-
import queue
import threading

#game to informacje o każdej z gier (dla każdej gry oddzielne game na oddzielnym wątku)
#tutaj są wszystkie funkcje zmieniające te informacje i zwracające je na serwer

class Game(threading.Thread):
	def __init__(self, ansq, q=None, loop_time=1.0/60, done=None): 
	# wstępne informacje o grze, gra startuje i gracze jeszcze nic nie wybrali, mają po 0 punktów
		self.p1Went = False
		self.p2Went = False
		self.ready = False
		self.id = id
		self.moves = [None, None]
		self.wins = [0,0]
		self.ties = 0
		self.p1Nick = ''
		self.p2Nick = ''
		self.p1Id = 0
		self.p2Id = 0
		self.q = q
		self.timeout = loop_time
		self.done = done
		self.ansq = ansq
		super(Game, self).__init__()
		if not q:
			self.q = queue.Queue()

	def onThread(self, function, *args, **kwargs):
		self.q.put((function, args, kwargs))

	def run(self):
		while True:
			try:
				function, args, kwargs = self.q.get(timeout=self.timeout)
				function(*args, **kwargs)
			except queue.Empty:
				self.idle()

	def idle(self):
		# put the code you would have put in the `run` loop here 
		pass

	def set_done(self, done):
		self.done = done

	def set_game_Id(self, id):
		self.id = id

	def get_player1_nick(self):
		self.ansq.put(self.p1Nick)
		self.done.set()
	
	def returnQ(self, value):
		self.ansq.put(value)
		
	def set_player1_nick(self, nick):
		self.p1Nick = nick
	
	def get_player1_Id(self):
		self.ansq.put(self.p1Id)
		self.done.set()

	def set_player1_Id(self, id):
		self.p1Id = id
		
	def get_player2_nick(self):
		self.ansq.put(self.p2Nick)
		self.done.set()
		
	def set_player2_nick(self, nick):
		self.p2Nick = nick
		
	def get_player2_Id(self):
		self.ansq.put(self.p2Id)
		self.done.set()

	def set_player2_Id(self, id):
		self.p2Id = id

	def get_player_move(self, p):
	# funkcja do sprawdzenia jakiego wyboru dokonuje gracz 
		"""
		:param p: [0,1]
		:return: Move
		"""
		self.ansq.put(self.moves[p])
		self.done.set()
		
	def set_player_move(self, p, move):
		self.moves[p] = move

	def set_ties(self):
		self.ties += 1

	def set_wins(self, p):
		self.wins[p] += 1

	def get_wins(self, p):
		self.ansq.put(self.wins[p])
		self.done.set()

	def player(self, player, move):
	# gracz dokonuje wyboru
		self.moves[player] = move
		if player == 0:
			self.p1Went = True
		else:
			self.p2Went = True
			
	def connected(self):
	#informacja czy jest 2 graczy połączonych z serwerem
		self.ansq.put(self.ready)
		self.done.set()
		
	def set_player1_Went(self):
		self.p1Went = True

	def set_player2_Went(self):
		self.p2Went = True

	def set_game_ready(self):
		self.ready = True

	def bothWent(self):
	# sprawdzenie czy obaj gracze dokonali wyboru
		self.ansq.put(self.p1Went and self.p2Went)
		self.done.set()

	def bothFree(self):
	# sprawdzenie czy obaj gracze są po dokonaniu wboru
		if self.p1Went == False and self.p2Went == False:
			self.ansq.put(True)
		else:
			self.ansq.put(False)
		self.done.set()

	def winner(self):
	# sprawdzenie wszystkich kombinacji i wyłonienie zwycięzcy
		p1 = str(self.moves[0]).upper()
		p2 = str(self.moves[1]).upper()
		
		# P paper
		# R rock
		# S scissors
		# L lizard
		# K spock
		# kamień > nożyce > papier > kamień > jaszczurka > Spock > nożyce > jaszczurka > papier > Spock > kamień
		
		winner = -1
		# R>S
		if p1 == "R" and p2 == "S":
			winner = 0
		elif p1 == "S" and p2 == "R":
			winner = 1
		# S>P
		elif p1 == "S" and p2 == "P":
			winner = 0
		elif p1 == "P" and p2 == "S":
			winner = 1
		# P>R
		elif p1 == "P" and p2 == "R":
			winner = 0
		elif p1 == "R" and p2 == "P":
			winner = 1
		# R>L
		elif p1 == "R" and p2 == "L":
			winner = 0
		elif p1 == "L" and p2 == "R":
			winner = 1
		# L>K
		elif p1 == "L" and p2 == "K":
			winner = 0
		elif p1 == "K" and p2 == "L":
			winner = 1
		# K>S
		elif p1 == "K" and p2 == "S":
			winner = 0
		elif p1 == "S" and p2 == "K":
			winner = 1
		# S>L
		elif p1 == "S" and p2 == "L":
			winner = 0
		elif p1 == "L" and p2 == "S":
			winner = 1
		# L>P
		elif p1 == "L" and p2 == "P":
			winner = 0
		elif p1 == "P" and p2 == "L":
			winner = 1
		# P>K
		elif p1 == "P" and p2 == "K":
			winner = 0
		elif p1 == "K" and p2 == "P":
			winner = 1
		# K>R
		elif p1 == "K" and p2 == "R":
			winner = 0
		elif p1 == "R" and p2 == "K":
			winner = 1
		
		self.ansq.put(winner)
		self.done.set()
		
	def resetWent(self):
	# przy każdej turze musimy wyzerować wybór, by ponownie sprawdzić
		self.p1Went = False
		self.p2Went = False