# !/usr/bin/env python
# -*- coding: utf-8 -*-
from threading import Thread, Event
import json 
import pygame
import pickle
import sys
from game import Game
import time
import queue

#serwer to serce wszystkich gier, przechowuje słownik gier (wątków), wykonuje wszystkie sprawdzenia i akcje, przekazuje do pozostałych plików informacje 

class Serwer:
	def __init__(self):
		self.games = {} # możemy (jako serwer) prowadzić wiele niezależnych gier, więc tworzymy ich słownik
		self.queues = {} #słownik kolejek którymi zwracamy informacje z wątku z grą na serwer
		self.idCount = 0 # zmienne do przechowywania ID gier i graczy
		self.lastGameId = 0
		self.lastPlayerId = 1 
		self.done = Event() #event do oczekiwania na wątek, aż wykona zadanie, żeby zawsze mieć dobrą informację

	def connect(self, userName):
		self.idCount += 1
		gameId = self.lastGameId
		print("Łączę z grą o id = " + str(gameId))
		ans = []
		ans.insert(0, gameId)
		if self.idCount % 2 == 1: #gdy wejdzie pierwszy gracz z nowej gry
			self.queues[gameId] = queue.Queue() #dodanie kolejki do słownika kolejek
			self.games[gameId] = Game(ansq=self.queues[gameId]) #dodanie gry do słownika wątków, przekazujemy kolejkę przypisaną do tej gry
			self.games[gameId].setName("Game " + str(gameId)) #nazywamy wątek dla wygody debugowania
			self.games[gameId].start()
			self.games[gameId].onThread(self.games[gameId].set_done, done=self.done) #przekazujemy event do oczekiwania na wątek
			self.games[gameId].onThread(self.games[gameId].set_game_Id, id=gameId) #przekazujemy id gry
			
			#print("Wysyłam nick gracza 1: " + str(userName)) #printy używane do debugowania w trakcie tworzenia gry
			self.games[gameId].onThread(self.games[gameId].set_player1_nick, nick=userName) #ustawiamy nick pierwszego gracza
			#print("Wysyłam id gracza 1: " + str(self.lastPlayerId))
			self.games[gameId].onThread(self.games[gameId].set_player1_Id, id=self.lastPlayerId) #i jego Id
			
			#self.games[gameId].onThread(self.games[gameId].get_player1_nick) #sprawdzenie zapisu danych w wątku, używane przy debugowaniu
			#pobranenicki = self.queues[gameId].get()
			#self.done.wait()
			#print("Player 1 nick: " + str(pobranenicki))
			
			#self.games[gameId].onThread(self.games[gameId].get_player1_Id)
			#pobraneidiki = self.queues[gameId].get()
			#self.done.wait()
			#print("Player 1 id: " + str(pobraneidiki))
			
			ans.insert(1, self.lastPlayerId)
			self.lastPlayerId += 1
			print("Creating a new game...")
		if self.idCount % 2 == 0: #gdy wejdzie drugi gracz z nowej gry dopisujemy jego dane do istniejącej gry z jednym graczem
			#print("Wysyłam nick gracza 2: " + str(userName))
			self.games[gameId].onThread(self.games[gameId].set_player2_nick, nick=userName)
			#print("Wysyłam id gracza 2: " + str(self.lastPlayerId))
			self.games[gameId].onThread(self.games[gameId].set_player2_Id, id=self.lastPlayerId)
			
			#self.games[gameId].onThread(self.games[gameId].get_player2_nick)
			#pobranenicki = self.queues[gameId].get()
			#self.done.wait()
			#print("Player 2 nick: " + str(pobranenicki))
			
			#self.games[gameId].onThread(self.games[gameId].get_player2_Id)
			#pobraneidiki = self.queues[gameId].get()
			#self.done.wait()
			#print("Player 2 id: " + str(pobraneidiki))
			
			self.games[gameId].onThread(self.games[gameId].set_game_ready) #przesyłamy informację że gra już ma obu graczy i może ruszyć
			ans.insert(1, self.lastPlayerId)
			self.lastPlayerId += 1
			self.lastGameId += 1
		return ans

	def playerName(self, userId, gameId): #klient pyta o nick gracza z którym będzie grać, więc po sprawdzeniu który z graczy pyta odsyłamy nick drugiego
		self.games[gameId].onThread(self.games[gameId].get_player1_Id)
		tmp = self.queues[gameId].get()
		self.done.wait()
		tmp2 = False
		tmp3 = ""
		while tmp2 == False: #dopiero gdy obaj gracze mają połączenie z serwerem można każdemu zwrócić nick drugiego
			self.games[gameId].onThread(self.games[gameId].connected)
			tmp2 = self.queues[gameId].get()
			self.done.wait()
		if tmp != userId:
			self.games[gameId].onThread(self.games[gameId].get_player1_nick)
			tmp3 = self.queues[gameId].get()
			self.done.wait()
		else:
			self.games[gameId].onThread(self.games[gameId].get_player2_nick)
			tmp3 = self.queues[gameId].get()
			self.done.wait()
		return tmp3

	def ready(self, userId, gameId): #klient pyta czy obaj gracze są gotowi na następną rundę (żeby zaczęli ją równocześnie i mieli równą ilość czasu)
		exist = False
		while exist == False:
			self.games[gameId].onThread(self.games[gameId].connected)
			exist = self.queues[gameId].get()
			self.done.wait()
		bfree = False
		while bfree == False:
			self.games[gameId].onThread(self.games[gameId].bothWent)
			bfree = self.queues[gameId].get()
			self.done.wait()
		return bfree

	def battle(self, userId, gameId, myfigure):
		self.games[gameId].onThread(self.games[gameId].get_player1_Id) #pobieramy Id pierwszego gracza
		p1id = self.queues[gameId].get()
		self.done.wait()
		self.games[gameId].onThread(self.games[gameId].get_player2_Id) #pobieramy Id drugiego gracza
		p2id = self.queues[gameId].get()
		self.done.wait()
		if p1id == userId: #ustawiamy ruch pierwszego gracza i informujemy że już wykonał ruch
			self.games[gameId].onThread(self.games[gameId].set_player_move, p=0, move=myfigure)
			self.games[gameId].onThread(self.games[gameId].set_player1_Went)
		if p2id == userId: #ustawiamy ruch drugiego gracza i informujemy że już wykonał ruch
			self.games[gameId].onThread(self.games[gameId].set_player_move, p=1, move=myfigure)
			self.games[gameId].onThread(self.games[gameId].set_player2_Went)

		bwent = False
		while bwent == False: #dopiero gdy obaj gracze wykonają ruch w danej rundzie możemy przejść dalej
			self.games[gameId].onThread(self.games[gameId].bothWent)
			bwent = self.queues[gameId].get()
			self.done.wait()
		
		self.games[gameId].onThread(self.games[gameId].winner) #sprawdzamy który gracz wygrał rundę
		winner = self.queues[gameId].get()
		self.done.wait()
		if winner == -1:
			self.games[gameId].onThread(self.games[gameId].set_ties) #w przypadku remisu dopisujemy każdemu po punkcie i zwiększamy liczbę remisów
			self.games[gameId].onThread(self.games[gameId].set_wins, 0)
			self.games[gameId].onThread(self.games[gameId].set_wins, 1)
		if winner == 0:
			self.games[gameId].onThread(self.games[gameId].set_wins, 0) #gdy wygra gracz 1 zwiększamy jego wynik
		if winner == 1:
			self.games[gameId].onThread(self.games[gameId].set_wins, 1) #gdy wygra gracz 2 zwiększamy jego wynik

		self.games[gameId].onThread(self.games[gameId].resetWent) #resetujemy informajcę o tym że obaj wykonali ruch

		ans = [] #przygotowanie zmiennej którą wysyłamy jako odpowiedź, pobieramy dane i w każdemu z graczy wysyłamy odpowiedni zestaw informacji
		self.games[gameId].onThread(self.games[gameId].get_wins, 0)
		score1 = self.queues[gameId].get()
		self.done.wait()
		self.games[gameId].onThread(self.games[gameId].get_wins, 1)
		score2 = self.queues[gameId].get()
		self.done.wait()
		self.games[gameId].onThread(self.games[gameId].get_player_move, 0)
		move1 = self.queues[gameId].get()
		self.done.wait()
		self.games[gameId].onThread(self.games[gameId].get_player_move, 1)
		move2 = self.queues[gameId].get()
		self.done.wait()
		if p1id == userId:
			ans.insert(0, score1) #myscore
			ans.insert(1, score2) #oponentscore
			ans.insert(2, move2) #oponentfigure
		if p2id == userId:
			ans.insert(0, score2) #myscore
			ans.insert(1, score1) #oponentscore
			ans.insert(2, move1) #oponentfigure
		return ans