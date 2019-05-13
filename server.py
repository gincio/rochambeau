from threading import Thread
import json 
import pygame
import pickle
import sys
from game import Game

class Serwer:
	def __init__(self):
		self.games = {} # możemy (jako serwer) prowadzić wiele niezależnych gier, więc tworzymy ich słownik
		self.idCount = 0 # zmienna do przechowywania ID następnej gry jaka powstanie
		self.lastGameId = 0
		self.lastPlayerId = 1

	def connect(self, userName):
		self.idCount += 1
		gameId = self.lastGameId + 1
		ans = []
		ans.append(gameId)
		self.lastGameId += 1
		if self.idCount % 2 == 1:
			self.games[gameId] = Thread(target = self.playGame, args = (self, gameId)) # w słowniku chcemy przechowywać wątki na których są kolejne gry
			self.games[gameId].start()
			self.games[gameId].game.p1Nick = userName # nie działa odwołanie przez wątek.gra.parametr lub .metoda
			self.games[gameId].game.p1Id = lastPlayerId
			ans [1] = lastPlayerId
			self.lastPlayerId += 1
			print("Creating a new game...")
		else:
			self.games[gameId].game.ready = True
			self.games[gameId].game.p2Nick = UserName
			self.games[gameId].game.p2Id = lastPlayerId
			ans [1] = lastPlayerId
			self.lastPlayerId += 1
		return ans

	def playGame(self, gameId):
		self.game = Game(gameId) # potrzebny while (gra istnieje): nasłuchuj, tylko nie umiemy napisać go tak żeby działał

	def playerName(self, userId, GameId):
		if games[gameId].game.p1Id != userId:
			return games[gameId].game.p1Nick
		else:
			return games[gameId].game.p2Nick

	def ready(self, userId, GameId):
		if games[gameId].game.p1Id == userId:
			games[gameId].game.p1Went = True
		if games[gameId].game.p2Id == userId:
			games[gameId].game.p2Went = True
		while games[gameId].game.bothWent() == False:
			print('Waiting for 2-nd player')
		return games[gameId].game.bothWent()

	def battle(self, userId, GameId, myfigure):
		if games[gameId].game.p1Id == userId:
			games[gameId].game.moves[0] = myfigure
		if games[gameId].game.p2Id == userId:
			games[gameId].game.moves[1] = myfigure
			
		winner = games[gameId].game.winner()
		if winner == -1:
			games[gameId].game.ties += 1
			games[gameId].game.wins[0] += 1
			games[gameId].game.wins[1] += 1
		if winner == 0:
			games[gameId].game.wins[0] += 1
		if winner == 1:
			games[gameId].game.wins[1] += 1
			
		ans = []
		if games[gameId].game.p1Id == userId:
			ans[0] = myscore = games[gameId].game.wins[0]
			ans[1] = oponentscore = games[gameId].game.wins[1]
			ans[2] = oponentfigure = games[gameId].game.moves[1]
		if games[gameId].game.p2Id == userId:
			ans[0] = myscore = games[gameId].game.wins[1]
			ans[1] = oponentscore = games[gameId].game.wins[0]
			ans[2] = oponentfigure = games[gameId].game.moves[0]
		return ans