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
			
			print("Wysyłam nick gracza 1: " + str(userName))
			self.games[gameId].onThread(self.games[gameId].set_player1_nick, nick=userName)
			print("Wysyłam id gracza 1: " + str(self.lastPlayerId))
			self.games[gameId].onThread(self.games[gameId].set_player1_Id, id=self.lastPlayerId)
			
			self.games[gameId].onThread(self.games[gameId].get_player1_nick)
			pobranenicki = self.queues[gameId].get()
			done.wait()
			print("Player 1 nick: " + str(pobranenicki))
			
			self.games[gameId].onThread(self.games[gameId].get_player1_Id)
			pobraneidiki = self.queues[gameId].get()
			done.wait()
			print("Player 1 id: " + str(pobraneidiki))
			
			ans.insert(1, self.lastPlayerId)
			self.lastPlayerId += 1
			print("Creating a new game...")
			time.sleep(10)
		if self.idCount % 2 == 0:
			print("Wysyłam nick gracza 2: " + str(userName))
			self.games[gameId].onThread(self.games[gameId].set_player2_nick, nick=userName)
			print("Wysyłam id gracza 2: " + str(self.lastPlayerId))
			self.games[gameId].onThread(self.games[gameId].set_player2_Id, id=self.lastPlayerId)
			
			self.games[gameId].onThread(self.games[gameId].get_player2_nick)
			pobranenicki = self.queues[gameId].get()
			done.wait()
			print("Player 2 nick: " + str(pobranenicki))
			
			self.games[gameId].onThread(self.games[gameId].get_player2_Id)
			pobraneidiki = self.queues[gameId].get()
			done.wait()
			print("Player 2 id: " + str(pobraneidiki))
			
			self.games[gameId].onThread(self.games[gameId].set_game_ready)
			ans.insert(1, self.lastPlayerId)
			self.lastPlayerId += 1
		return ans

	def playerName(self, userId, GameId):
		self.games[gameId].onThread(self.games[gameId].get_player1_Id)
		tmp = self.queues[gameId].get()
		done.wait()
		if tmp != userId:
			self.games[gameId].onThread(self.games[gameId].get_player1_nick)
			tmp2 = self.queues[gameId].get()
			done.wait()
			return tmp2
		else:
			self.games[gameId].onThread(self.games[gameId].get_player2_nick)
			tmp2 = self.queues[gameId].get()
			done.wait()
			return tmp2

	def ready(self, userId, GameId):
		self.games[gameId].onThread(self.games[gameId].get_player1_Id)
		tmp = self.queues[gameId].get()
		done.wait()
		if tmp == userId:
			self.games[gameId].onThread(self.games[gameId].set_player1_Went)
		self.games[gameId].onThread(self.games[gameId].get_player2_Id)
		tmp = self.queues[gameId].get()
		done.wait()
		if tmp == userId:
			self.games[gameId].onThread(self.games[gameId].set_player2_Went)
		self.games[gameId].onThread(self.games[gameId].bothWent)
		tmp2 = self.queues[gameId].get()
		done.wait()
		while tmp2 == False:
			print('Waiting for 2-nd player')
			self.games[gameId].onThread(self.games[gameId].bothWent)
			tmp2 = self.queues[gameId].get()
			done.wait()
		return tmp2

	def battle(self, userId, GameId, myfigure):
		self.games[gameId].onThread(self.games[gameId].get_player1_Id)
		p1id = self.queues[gameId].get()
		done.wait()
		self.games[gameId].onThread(self.games[gameId].get_player2_Id)
		p2id = self.queues[gameId].get()
		done.wait()
		if p1id == userId:
			self.games[gameId].onThread(self.games[gameId].set_player_move, (0, myfigure))
		if p2id == userId:
			games[gameId].onThread(self.games[gameId].set_player_move, (1, myfigure))

		self.games[gameId].onThread(self.games[gameId].winner)
		winner = self.queues[gameId].get()
		done.wait()
		if winner == -1:
			self.games[gameId].onThread(self.games[gameId].set_ties)
			self.games[gameId].onThread(self.games[gameId].set_wins, 0)
			self.games[gameId].onThread(self.games[gameId].set_wins, 1)
		if winner == 0:
			self.games[gameId].onThread(self.games[gameId].set_wins, 0)
		if winner == 1:
			self.games[gameId].onThread(self.games[gameId].set_wins, 1)

		ans = []
		self.games[gameId].onThread(self.games[gameId].get_wins, 0)
		score1 = self.queues[gameId].get()
		done.wait()
		self.games[gameId].onThread(self.games[gameId].get_wins, 1)
		score2 = self.queues[gameId].get()
		done.wait()
		self.games[gameId].onThread(self.games[gameId].get_player_move, 0)
		move1 = self.queues[gameId].get()
		done.wait()
		self.games[gameId].onThread(self.games[gameId].get_player_move, 1)
		move2 = self.queues[gameId].get()
		done.wait()
		if p1id == userId:
			ans.insert(0, score1) #myscore
			ans.insert(1, score2) #oponentscore
			ans.insert(2, move2) #oponentfigure
		if p2id == userId:
			ans.insert(0, score2) #myscore
			ans.insert(1, score1) #oponentscore
			ans.insert(2, move1) #oponentfigure
		return ans