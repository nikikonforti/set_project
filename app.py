from flask import Flask, render_template, request, jsonify, make_response, json
from flask import Response, session
from flask_socketio import SocketIO, emit
import shortuuid
import game

app = Flask(__name__)
socketio = SocketIO(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


thisGame = None
gameHand = None
playerIDs = []

@app.route('/')
def home():
   global playerIDs
   print(session) 
   if 'user' in session:
      print("user exists.") #TODO: not urgent, but when you dont quit Chrome the cookies stay and gives non-incognito window same uuid.
      playerID = session['user'] 
      if playerID not in playerIDs:
         playerIDs.append(playerID) # when you restart python (because you fix a small bug for example) playerIDs get cleared 
         # however chrome still stores the session data in cookies so this if statement gets executed
         # so you need to make sure that playerIDs are restored after python refresh using session data
   else:
      id = shortuuid.uuid()[:8]
      session["user"] = id
      print("session user")
      print(session["user"])
      playerIDs.append(id)
      playerID = id
   print("playerIDs: ")
   print(playerIDs)
   return render_template('playerload.html', playerID=playerID) #TODO: this is a problem. You can only render normal window then incog window not the other way around. I have NO idea. cookies? the devil???

@socketio.on('connect')
def test_connect():
   emit('after connect',  {'data':'Lets dance'})

@socketio.on('play') 
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

@socketio.on('refresh')
def refresh_cards(message):
   print("refresh message:")
   print(message)
   global gameHand
   print("game hand on refresh")
   print(gameHand)
   emit('update screen', message, broadcast=True)

@app.route('/play/', methods=['GET', 'POST'])
def startGame():
   global thisGame
   print("startGame")
   print(thisGame.getRemainingDeckSize())
   print("gameHand in play")
   print(gameHand)
   return render_template('main.html', gameHand=gameHand, deckSize=thisGame.getRemainingDeckSize(), playerPoints=thisGame.getAllPlayerPoints())

@app.route('/3more', methods=['GET', 'POST'])
def deal3More():
   global gameHand
   print(session)
   gameHand = thisGame.clickDeal()
   return jsonify(gameHand=gameHand, deckSize=thisGame.getRemainingDeckSize())

@app.route('/checkSet', methods=['GET', 'POST'])
def checkSet():
   data = request.get_json()
   print("data in checkSet:")
   print(data)
   possibleSet = data["possibleSet"]
   playerID = session['user']
   print('playerID')
   print(playerID)
   global thisGame
   isSet = thisGame.isSet(possibleSet)
   if isSet:
      oldPoints = thisGame.getPoints(playerID)
      thisGame.setPoints(playerID, int(oldPoints) + 1) 
      print("player " + playerID + " gets point!")
   else:
      thisGame.setPoints(playerID, thisGame.getPoints(playerID) - 1)
      print("player " + playerID + " does not win point.")
   return jsonify(isSet=isSet, playerPoints=thisGame.getPoints(playerID))

@app.route('/checkSetInHand', methods=['GET', 'POST'])
def checkSetInHand():
   data = request.get_json()
   print(data)
   gameHand = data["gameHand"]
   playerID = session["user"]
   global thisGame
   isSet = thisGame.isSetInHand(gameHand)
   if isSet:
      thisGame.setPoints(playerID, thisGame.getPoints(playerID) -1) 
      print("player gets a point removed.")
   return jsonify(isSet = isSet, playerPoints=thisGame.getPoints(playerID))


@app.route('/removeSet', methods=['GET', 'POST'])
def removeSet():
   global thisGame 
   data = request.get_json()
   possibleSet = data["possibleSet"]
   gameHand = thisGame.removeSet(possibleSet)
   # check if it needs three more cards
   if len(gameHand) < 9 and thisGame.getRemainingDeckSize() > 0:
      gameHand = thisGame.clickDeal()
   return jsonify(gameHand=gameHand, deckSize=thisGame.getRemainingDeckSize())



if __name__ == '__main__':
   #app.run(host='0.0.0.0', port=5000, debug=True)
   socketio.run(app, host='0.0.0.0')

playerIDs = []
# app.config["SECRET_KEY"] 

for key in session.keys():
     session.pop(key)
