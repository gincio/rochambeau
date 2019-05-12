from _thread import *
import json 
import pygame
import pickle
import sys
from game import Game

class Serwer:
	def __init__(self):
		self.games = {} # możemy (jako serwer) prowadzić wiele niezależnych gier, więc tworzymy ich słownik
		self.idCount = 0 # zmienna do przechowywania ID następnej gry jaka powstanie

	def connect(self, userName):
		self.idCount += 1
		gameId = (self.idCount - 1)/2
		p = 0
		if self.idCount % 2 == 1:
			self.games[gameId] = Game(gameId)
			self.games[gameId].p1Nick = userName
			print("Creating a new game...")
		else:
			self.games[gameId].ready = True
			p = 1
			self.games[gameId].p2Nick = UserName
		start_new_thread(Game(gameId), ()) # jakie argumenty tutaj podać żeby tworzył się prawidłowo następny wątek? pierwszy argument musi dać się wywołać, bo to on jest właśnie funkcją którą obsłuży nowy wątek
		return "ok"

	def playerName(self, userName, GameId):
		if games[gameId].p1Nick != userName:
			return games[gameId].p1Nick
		else:
			return games[gameId].p2Nick

	def ready(self, userName, GameId):
		if games[gameId].p1Nick == userName:
			games[gameId].p1Went = True
		if games[gameId].p2Nick == userName:
			games[gameId].p2Went = True
		return games[gameId].bothWent()

	def battle(self, userName, GameId, myfigure):
		if games[gameId].p1Nick == userName:
			games[gameId].moves[0] = myfigure
		if games[gameId].p2Nick == userName:
			games[gameId].moves[1] = myfigure
			
		winner = games[gameId].winner()
		if winner == -1:
			games[gameId].ties += 1
			games[gameId].wins[0] += 1
			games[gameId].wins[1] += 1
		if winner == 0:
			games[gameId].wins[0] += 1
		if winner == 1:
			games[gameId].wins[1] += 1
			
		ans
		if games[gameId].p1Nick == userName:
			ans[0] = myscore = games[gameId].wins[0]
			ans[1] = oponentscore = games[gameId].wins[1]
			ans[2] = oponentfigure = games[gameId].moves[1]
		if games[gameId].p2Nick == userName:
			ans[0] = myscore = games[gameId].wins[1]
			ans[1] = oponentscore = games[gameId].wins[0]
			ans[2] = oponentfigure = games[gameId].moves[0]
		return ans