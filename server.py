from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
import game
app = Flask(__name__)

thisGame = None
gameHand = None

@app.route('/')
def home():
   global thisGame 
   global gameHand
   thisGame = game.createGame()
   gameHand = thisGame.dealInitial()
   return render_template('main.html', gameHand=gameHand, deckSize=thisGame.getRemainingDeck())  #feed list to html

@app.route('/3more', methods=['GET', 'POST'])
def deal3More():
   global gameHand
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
   app.run(debug = True)