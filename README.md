# Rochambeau Multithread Game
Rochambeau Multithread Game is a multiplayer game based on Flask server with Python backend and jQuery frontend.

## Specification
Main assumption of a project was to create an application which will create saparate threads for each game (in this case for a pair of clients). It was made as an evaluation of a collage core subject called `Distributed Systems`.
We made web front-end to make our app widely-available.

## Installation
To install Rochambeau Multithread Game you have to install `Python` in version 3.6 or above and `pip` package manager.
Then you have to install some extra packages:
```
pip install Flask
pip install pygame
pip install queuelib
```

Then just clone this repo with command
```
git clone https://github.com/gincio/rochambeau.git
```

## Run application
To run game webserver type
```
cd rochambeau
python webserver.py
```
Server will start with your machine IP on port 5000, so if you want to run a game on this machine type in your browser address bar. <YOUR_SERVER_IP_HERE> is your machine running server IP, you can connect to a game from different devices inside your network
```
http://<YOUR_SERVER_IP_HERE>:5000
```
