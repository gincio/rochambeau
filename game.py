class Game:
	def __init__(self, id): 
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
		
	def get_player1_nick(self):
		return self.p1Nick
		
	def get_player2_nick(self):
		return self.p2Nick
		
	def get_player_move(self, p):
	# funkcja do sprawdzenia jakiego wyboru dokonuje gracz 
		"""
		:param p: [0,1]
		:return: Move
		"""
		return self.moves[p]
		# return json.dumps(self.moves[p])
		
	def player(self, player, move):
	# gracz dokonuje wyboru
		self.moves[player] = move
		if player == 0:
			self.p1Went = True
		else:
			self.p2Went = True
			
	def connected(self):
	# połączenie z serwerem
		return self.ready
		
	def bothWent(self):
	# sprawdzenie czy obaj gracze dokonali wyboru
		return self.p1Went and self.p2Went
		
	def winner(self):
	# sprawdzenie wszystkich kombinacji i wyłonienie zwycięzcy
		p1 = self.moves[0].upper()[0]
		p2 = self.moves[1].upper()[0]
		
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
		
		return winner
		# return json.dumps(winner)
		
	def resetWent(self):
	# przy każdej turze musimy wyzerować wybór, by ponownie sprawdzić
		self.p1Went = False
		self.p2Went = False