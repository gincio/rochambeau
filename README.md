# Rochambeau Multithread Game
Rochambeau Multithread Game is a multiplayer game based on Flask server with Python backend and jQuery frontend.

## Specification
Main assumption of a project was to create an application which will create saparate threads for each game (in this case for a pair of clients). It was made as an evaluation of a collage core subject called `Distributed Systems`.
We made web front-end to make our app widely-available.

## Installation
To install Rochambeau Multithread Game you have to install `Python` in version 3.6 or above and `pip` package manager.
Then you have to install some extra packages for Flask webserver and pygame library
```
pip install Flask
pip install pygame
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
Server will start with your machine IP on port 5000, so if you want to run a game on this machine type in your browser address bar
```
http://127.0.0.1:5000
```
or
```
localhost:5000
```
If you want to run a game on other device type
```
http://<MACHINE_RUNNING_SERVER_IP>:5000
```
