# !/usr/bin/env python
# -*- coding: utf-8 -*-
from server import Serwer
from flask import Flask, render_template, request, redirect, Response, jsonify

#webserver to obsługa komunikacji naszego serwera z frontem (klientami)
#Flask na webserver nasłuchuje na akcje wysyłane przez klientów, wysyła odpowiednie polecenia na serwer i zwraca klientom odpowiedzi

app = Flask(__name__)
Server = Serwer()

print("Waiting for a connection, Server Started")

@app.route('/') # gdy nic nie zostało przyciśnięte
def output():
	# serve index template
	return render_template('index.html')
	
@app.route('/', methods = ['POST']) # gdy wybierzemy jakąś funkcjonalność 
def worker():	
	# read json + reply
	response = ''
	action = str(request.form.get('action'))
	
	if action == 'setConnection': # ustawienie połączenia
		UserName = str(request.form.get('nick'))
		
		ID = Server.connect(UserName)
		
		response = {'status': 'ok', 'GameId': ID[0], 'UserId': ID[1]}
		#response.headers.add('Access-Control-Allow-Origin', '*')
		
	elif action == 'getOponent': # zwracamy nazwę rywala z którym zaczynamy grę
		userId = int(request.form.get('UserId'))
		gameId = int(request.form.get('GameId'))
		
		nick = Server.playerName(userId, gameId)
		
		response = {'status': 'ok', 'username': nick}
		#response.headers.add('Access-Control-Allow-Origin', '*')
		
	elif action == 'chooseFigure': # czekam na obie strony, podejmuję odpowiednią decyzję
		myfigure = str(request.form.get('figure'))
		userId = int(request.form.get('UserId'))
		gameId = int(request.form.get('GameId'))
		
		ans = Server.battle(userId, gameId, myfigure)
		
		print('myScore ' + str(ans[0]))
		print('oponentScore ' + str(ans[1]))
		print('oponentFigure ' + str(ans[2]))
		response = {'status': 'ok', 'myScore': ans[0], 'oponentScore': ans[1], 'oponentFigure': ans[2]}
		#response.headers.add('Access-Control-Allow-Origin', '*')
	
	elif action == 'playerReady': # sprawdzenie czy przeciwnik jest już gotowy
		userId = int(request.form.get('UserId'))
		gameId = int(request.form.get('GameId'))
		
		if Server.ready(userId, gameId) == True:
			stat = 'ok'
		elif Server.ready(userId, gameId) == False:
			stat = 'fail'
		else:
			stat = 'wait'
		print("Wysłałem gotowość graczowi " + str(userId))
		response = {'status': stat}
		#response.headers.add('Access-Control-Allow-Origin', '*')

	return jsonify(response)

if __name__ == '__main__':
	app.run(host = '0.0.0.0',port=5000,debug=True)
	print("Application Started")
