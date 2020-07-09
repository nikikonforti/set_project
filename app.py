from flask import Flask, render_template, request, jsonify, make_response, json
from flask import Response, session
import uuid
import game

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


thisGame = None
gameHand = None
playerIDs = []

@app.route('/')
def home():
	global playerIDs
	print(session)
	if 'user' in session:
	    print("User exists: ")
	else:
		id = uuid.uuid1()
		session["user"] = id.int 
		print(session)
		playerIDs.append(session["user"])
	print("playerIDs:")
	print(playerIDs)
	return render_template('playerload.html')

@app.route('/play', methods=['GET', 'POST'])
def startGame():
	global thisGame 
	global gameHand
	global playerIDs
	thisGame = game.createGame(playerIDs)
	gameHand = thisGame.dealInitial()
	return render_template('main.html', gameHand=gameHand, deckSize=thisGame.getRemainingDeck())

@app.route('/3more', methods=['GET', 'POST'])
def deal3More():
   global gameHand
   print(session)
   gameHand = thisGame.clickDeal()
   return jsonify(gameHand=gameHand, deckSize=thisGame.getRemainingDeck())

@app.route('/checkSet', methods=['GET', 'POST'])
def checkSet():
   data = request.get_json()
   possibleSet = data["possibleSet"]
   global thisGame
   isSet = thisGame.isSet(possibleSet)
   if isSet:
      thisGame.setPoints(thisGame.getPoints() + 1)
   else:
      thisGame.setPoints(thisGame.getPoints() - 1)
   return jsonify(isSet=isSet, playerPoints=thisGame.getPoints())

@app.route('/checkSetInHand', methods=['GET', 'POST'])
def checkSetInHand():
   data = request.get_json()
   gameHand = data["gameHand"]
   global thisGame
   isSet = thisGame.isSetInHand(gameHand)
   if isSet:
      thisGame.setPoints(thisGame.getPoints() -1)
   return jsonify(isSet = isSet, playerPoints=thisGame.getPoints())


@app.route('/removeSet', methods=['GET', 'POST'])
def removeSet():
   global thisGame 
   data = request.get_json()
   possibleSet = data["possibleSet"]
   gameHand = thisGame.removeSet(possibleSet)
   # check if it needs three more cards
   if len(gameHand) < 9 and thisGame.getRemainingDeck() > 0:
      gameHand = thisGame.clickDeal()
   return jsonify(gameHand=gameHand, deckSize=thisGame.getRemainingDeck())



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

playerIDs = []