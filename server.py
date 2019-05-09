# !/usr/bin/env python
# -*- coding: utf-8 -*-
# import socket
from _thread import *
import json 
import pygame
from network import Network
import pickle
import sys
import random
from game import Game
from flask import Flask, render_template, request, redirect, Response, jsonify
app = Flask(__name__)

print("Waiting for a connection, Server Started")

@app.route('/') # gdy nic nie zostało przyciśnięte
def output():
	# serve index template
	return render_template('index.html')

def threaded_client(p, gameId):
	# global idCount # zmienna od ilości wszystkich id
	reply = ""
	while True:
		try:
			# sprawdzenie czy gra wciąż istnieje (gdy ktoś się rozłączy gra zniknie ze słownika)
			if gameId in games:
				game = games[gameId]
				
				if not data:
					break
				else:
					if data == "reset":
						game.resetWent() # reset gry
					elif data != "get":
						game.play(p, data) # jeśli nie reset i nie get, to znaczy że przesyłamy wybór
						
					reply = game
			else:
				break
		except:
			break
	# na wypadek gdy nic się nie stanie (tak być nie może) zamykamy grę
	print("Lost connection")
	try:
		del games[gameID]
		print("Closing Game", gameID)
	except:
		pass
	# idCount -= 1

@app.route('/', methods = ['POST']) # gdy wybierzemy jakąś funkcjonalność 
def worker():
	# możemy (jako serwer) prowadzić wiele niezależnych gier, więc tworzymy ich słownik
	games = {} # słownik ID gier jakie mamy
	idCount = 0 # zmienna do przechowywania ID następnej gry jaka powstanie
	
	# read json + reply
	result = ''
	action = str(request.form.get('action'))
	
	if action == 'setConnection': # ustawienie połączenia
		UserName = str(request.form.get('nick'))
		clock = pygame.time.Clock()
	
		idCount += 1
		p = 0
		gameId = (idCount - 1)/2
		if idCount % 2 == 1:
			games[gameId] = Game(gameId)
			Game(gameId).p1Nick = UserName
			response = jsonify({'connection': Game(gameId).p2Nick})
			print("Creating a new game...")
		else:
			games[gameId].ready = True
			p = 1
			Game(gameId).p2Nick = UserName
			response = jsonify({'connection': Game(gameId).p1Nick})
		start_new_thread(threaded_client, (p, gameId))

		response.headers.add('Access-Control-Allow-Origin', '*')
			
	elif action == 'getOpponent': # zwracamy nazwę rywala z którym zaczynamy grę
		clock.tick(60)
		try: # próba połączenia z grą
				game = n.send('get')
		except: # gdy coś nie zadziała obsługa:
				run = False
				result = False
		result = int(n.getP())
		response = jsonify({'oponent': result})
		response.headers.add('Access-Control-Allow-Origin', '*')

	elif action == 'chooseFigure': # czekam na obie strony, podejmuję odpowiednią decyzję
		n = Network()
		player = int(n.getP())	
		
		if game.bothWent(): # gdy obaj wybrali potrzebujemy sprawdzić który wygrał
			pygame.time.delay(500)
			try:
					game = n.send("reset") # kolejna runda
			except:
					run = False
					print("Couldn't get game")
					# break # za każdym razem ubezpieczenie gdyby coś przestało działać
			# sprawdzamy komu co napisać i wypisujemy podsumowanie poprzedniej rundy
			if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
					result = "You Won!"
			elif game.winner() == -1:
					result = "Tie Game!"
			else:
					result = "You Lost..."
		response = jsonify({'winner': result})
		response.headers.add('Access-Control-Allow-Origin', '*')
		
	else: # playerReady
		result = "False"
		response = jsonify({'ready': result})
		response.headers.add('Access-Control-Allow-Origin', '*')

	return response

if __name__ == '__main__':
	app.run(debug=True)
	print("Application Started")