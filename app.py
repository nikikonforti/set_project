from flask import Flask, render_template, request, jsonify, make_response, json
from flask import Response, session
from flask_socketio import SocketIO, emit
import uuid
import game

app = Flask(__name__)
socketio = SocketIO(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


thisGame = None
gameHand = None
playerIDs = []

values = {
    'slider1': 25,
    'slider2': 0,
}

@app.route('/')
def home():
   global playerIDs
   print(session)
   if 'user' in session:
      print("user exists: ")
   else:
      id = uuid.uuid1()
      session["user"] = id.int
      print(session)
      playerIDs.append(session["user"])
   print("playerIDs: ")
   print(playerIDs)
   return render_template('playerload.html')

@socketio.on('connect')
def test_connect():
   emit('after connect',  {'data':'Lets dance'})

@socketio.on('Slider value changed')
def value_changed(message):
   print("in python value_changed")
   values[message['who']] = message['data']
   emit('update value', message, broadcast=True)

@socketio.on('Play button clicked')
def play_clicked(message):
   print("MESSAGE:")
   print(message)
   global thisGame 
   global playerIDs
   global gameHand
   thisGame = game.createGame(playerIDs)
   gameHand = thisGame.dealInitial()
   #startGame()
   emit('update screen', message, broadcast=True)
   #return render_template('main.html', gameHand=None, deckSize=1)

@app.route('/play', methods=['GET', 'POST'])
def startGame():
   print("startGame")
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
   print("data in check set:")
   print(data)
   possibleSet = data["possibleSet"]
   global thisGame
   isSet = thisGame.isSet(possibleSet)
   if isSet:
      #thisGame.setPoints(thisGame.getPoints() + 1) TODO: fix these to give points to the specific player in question.
      print("player gets point!")
   else:
      #thisGame.setPoints(thisGame.getPoints() - 1)
      print("player does not win point.")
   return jsonify(isSet=isSet, playerPoints=thisGame.getPoints())

@app.route('/checkSetInHand', methods=['GET', 'POST'])
def checkSetInHand():
   data = request.get_json()
   gameHand = data["gameHand"]
   global thisGame
   isSet = thisGame.isSetInHand(gameHand)
   if isSet:
      #thisGame.setPoints(thisGame.getPoints() -1) TODO: same as above.
      print("player gets a point removed.")
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
   #app.run(host='0.0.0.0', port=5000, debug=True)
   socketio.run(app, host='0.0.0.0')

playerIDs = []