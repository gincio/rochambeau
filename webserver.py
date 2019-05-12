# !/usr/bin/env python
# -*- coding: utf-8 -*-
from server import Serwer
from flask import Flask, render_template, request, redirect, Response, jsonify

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
	result = ''
	action = str(request.form.get('action'))
	
	if action == 'setConnection': # ustawienie połączenia
		UserName = str(request.form.get('myUsername'))
		
		ID = Server.connect(UserName)
		
		response = jsonify({'status': 'ok', 'GameId': ID})
		response.headers.add('Access-Control-Allow-Origin', '*')
		
	elif action == 'getOpponent': # zwracamy nazwę rywala z którym zaczynamy grę
		userName = str(request.form.get('myUsername'))
		GameId == str(request.form.get('GameId'))
		
		nick = Server.playerName(userName, GameId)
		
		response = jsonify({'status': 'ok', 'username': nick})
		response.headers.add('Access-Control-Allow-Origin', '*')
		
	elif action == 'chooseFigure': # czekam na obie strony, podejmuję odpowiednią decyzję
		myfigure = str(request.form.get('figure'))
		userName = str(request.form.get('myUsername'))
		GameId == str(request.form.get('GameId'))
		
		ans = Server.battle(userName, GameId, myfigure)
		
		response = jsonify({'status': 'ok', 'myScore': ans[0], 'oponentScore': ans[1], 'oponentFigure': ans[2]})
		response.headers.add('Access-Control-Allow-Origin', '*')
	
	elif action == 'playerReady': # sprawdzenie czy przeciwnik jest już gotowy
		userName = str(request.form.get('myUsername'))
		GameId == str(request.form.get('GameId'))
		
		if Server.ready(userName, GameId) == True:
			stat = 'ok'
		else:
			stat = 'wait'
		
		response = jsonify({'status': stat})
		response.headers.add('Access-Control-Allow-Origin', '*')
		
	else: # error
		response = jsonify({'status': 'fail'})
		response.headers.add('Access-Control-Allow-Origin', '*')

	return response

if __name__ == '__main__':
	app.run(debug=True)
	print("Application Started")