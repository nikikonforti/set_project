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
      print("user exists.") #TODO: not urgent, but when you dont quit Chrome the cookies stay and gives non-incognito window same uuid.
   else:
      id = uuid.uuid1()
      session["user"] = id.int
      print("session user")
      print(session["user"])
      print("first 15")
      print(int(str(session["user"])[:15]))
      shortenedID = str(session["user"])[:15]
      playerIDs.append(shortenedID)
      playerID = shortenedID
   print("playerIDs: ")
   print(playerIDs)
   return render_template('playerload.html', playerID=playerID)

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
   # When play button is clicked, there is one game object created with the playerIDs to the respective tabs
   global thisGame 
   global playerIDs
   global gameHand
   thisGame = game.createGame(playerIDs)
   gameHand = thisGame.dealInitial()
   emit('update screen', message, broadcast=True)

@app.route('/play/<id>', methods=['GET', 'POST'])
def startGame(id=None):
   # data = request.get_json()
   # playerID = data["playerID"]
   print("startGame")
   # print("playerID")
   # print(playerID)
   global thisGame
   return render_template('main.html', gameHand=gameHand, deckSize=thisGame.getRemainingDeck(), playerPoints=thisGame.getAllPlayerPoints())

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
   playerID = data["playerID"]
   global thisGame
   isSet = thisGame.isSet(possibleSet)
   if isSet:
      oldPoints = thisGame.getPoints(playerID)
      thisGame.setPoints(playerID, int(oldPoints) + 1) 
      #TODO: fix these to give points to the specific player in question.
      print("player " + playerID + " gets point!")
   else:
      thisGame.setPoints(playerID, thisGame.getPoints(playerID) - 1)
      print("player " + playerID + " does not win point.")
   return jsonify(isSet=isSet, playerPoints=thisGame.getAllPlayerPoints())

@app.route('/checkSetInHand', methods=['GET', 'POST'])
def checkSetInHand():
   data = request.get_json()
   gameHand = data["gameHand"]
   playerID = data["playerID"]
   global thisGame
   isSet = thisGame.isSetInHand(gameHand)
   if isSet:
      thisGame.setPoints(playerID, thisGame.getPoints(playerID) -1) #TODO: same as above.
      print("player gets a point removed.")
   return jsonify(isSet = isSet, playerPoints=thisGame.getAllPlayerPoints())


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
# app.config["SECRET_KEY"] 

for key in session.keys():
     session.pop(key)
