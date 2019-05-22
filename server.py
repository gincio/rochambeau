from threading import Thread, Event
import json 
import pygame
import pickle
import sys
from game import Game
import time
import queue

class Serwer:
	def __init__(self):
		self.games = {} # możemy (jako serwer) prowadzić wiele niezależnych gier, więc tworzymy ich słownik
		self.queues = {}
		self.idCount = 0 # zmienna do przechowywania ID następnej gry jaka powstanie
		self.lastGameId = 0
		self.lastPlayerId = 1

	def connect(self, userName):
		self.idCount += 1
		gameId = self.lastGameId + 1
		ans = []
		ans.insert(0, gameId)
		self.lastGameId += 1
		if self.idCount % 2 == 1:
			done = Event()
			self.queues[gameId] = queue.Queue()
			self.games[gameId] = Game(ansq=self.queues[gameId]) # w słowniku chcemy przechowywać wątki na których są kolejne gry
			self.games[gameId].setName("Game " + str(gameId))
			self.games[gameId].start()
			self.games[gameId].onThread(self.games[gameId].set_done, done=done)
			self.games[gameId].onThread(self.games[gameId].set_game_Id, id=gameId)
			
			print("Wysyłam nick: " + str(userName))
			self.games[gameId].onThread(self.games[gameId].set_player1_nick, nick=userName)
			#done.wait()
			#print("Player 1 nick: " + str(self.games[gameId].onThread(self.games[gameId].get_player1_nick)))
			self.games[gameId].onThread(self.games[gameId].set_player1_Id, id=self.lastPlayerId)
			#print("Player 1 id: " + str(self.games[gameId].onThread(self.games[gameId].get_player1_Id))
			#self.games[gameId].join()
			print(self.queues[gameId].empty())
			pobranenicki = self.queues[gameId].get() #str(self.games[gameId].onThread(self.games[gameId].get_player1_nick))
			#done.wait()
			print("cokolwiek")
			#time.sleep(3)
			print("Waiting for U're mom")
			#time.sleep(3)
			print("Player 1 nick: " + str(pobranenicki))
			
			ans.insert(1, self.lastPlayerId)
			self.lastPlayerId += 1
			print("Creating a new game...")
		if self.idCount % 2 == 0:
			self.games[gameId].onThread(self.games[gameId].set_player2_nick, nick=userName)
			#print("Player 2 nick: " + str(self.games[gameId].onThread(self.games[gameId].get_player2_nick)))
			self.games[gameId].onThread(self.games[gameId].set_player2_Id, id=lastPlayerId)
			#print("Player 2 id: " + str(self.games[gameId].onThread(self.games[gameId].get_player2_Id)))
			self.games[gameId].onThread(self.games[gameId].set_game_ready)
			ans.insert(1, lastPlayerId)
			self.lastPlayerId += 1
		print("Player 1 id: " + str(self.games[gameId].onThread(self.games[gameId].get_player1_Id)))
		return ans

	def playerName(self, userId, GameId):
		if games[gameId].onThread(self.games[gameId].get_player1_Id) != userId:
			return games[gameId].onThread(self.games[gameId].get_player1_nick)
		else:
			return games[gameId].onThread(self.games[gameId].get_player2_nick)

	def ready(self, userId, GameId):
		if games[gameId].onThread(self.games[gameId].get_player1_Id) == userId:
			games[gameId].onThread(self.games[gameId].set_player1_Went)
		if games[gameId].onThread(self.games[gameId].get_player2_Id) == userId:
			games[gameId].onThread(self.games[gameId].set_player2_Went)
		while games[gameId].onThread(self.games[gameId].bothWent) == False:
			print('Waiting for 2-nd player')
		return games[gameId].onThread(self.games[gameId].bothWent)

	def battle(self, userId, GameId, myfigure):
		if games[gameId].onThread(self.games[gameId].get_player1_Id) == userId:
			games[gameId].onThread(self.games[gameId].set_player_move, (0, myfigure))
		if games[gameId].onThread(self.games[gameId].get_player2_Id) == userId:
			games[gameId].onThread(self.games[gameId].set_player_move, (1, myfigure))
			
		winner = games[gameId].onThread(self.games[gameId].winner)
		if winner == -1:
			games[gameId].onThread(self.games[gameId].set_ties)
			games[gameId].onThread(self.games[gameId].set_wins, 0)
			games[gameId].onThread(self.games[gameId].set_wins, 1)
		if winner == 0:
			games[gameId].onThread(self.games[gameId].set_wins, 0)
		if winner == 1:
			games[gameId].onThread(self.games[gameId].set_wins, 1)
			
		ans = []
		if games[gameId].onThread(self.games[gameId].get_player1_Id) == userId:
			ans.insert(0, games[gameId].onThread(self.games[gameId].get_wins, 0)) #myscore
			ans.insert(1, games[gameId].onThread(self.games[gameId].get_wins, 1)) #oponentscore
			ans.insert(2, games[gameId].onThread(self.games[gameId].get_player_move, 1)) #oponentfigure
		if games[gameId].onThread(self.games[gameId].get_player2_Id) == userId:
			ans.insert(0, games[gameId].onThread(self.games[gameId].get_wins, 1)) #myscore
			ans.insert(1, games[gameId].onThread(self.games[gameId].get_wins, 0)) #oponentscore
			ans.insert(2, games[gameId].onThread(self.games[gameId].get_player_move, 0)) #oponentfigure
		return ans