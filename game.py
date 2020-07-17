import random 
from itertools import combinations

class Game:
	def __init__(self, cards, playerIDs):
		self.numPlayers = len(playerIDs)
		self.cards = cards
		self.gameHand = []
		self.playerPoints = {}
		print(playerIDs)
		for p in playerIDs:
			self.playerPoints[p] = 0
		print("playerPoints!!")
		print(self.playerPoints)

	def dealInitial(self):
		random.shuffle(self.cards)
		print(len(self.cards))
		for x in range(9):
			self.gameHand.append(self.cards.pop(0))
		print(len(self.cards))
		return self.gameHand
			
	def clickDeal(self):	
		for x in range(3):
			self.gameHand.append(self.cards.pop(0))
		print(len(self.cards))	
		return self.gameHand

	def isSet(self, possible_set):
		p_one = possible_set[0].split('_')
		p_two = possible_set[1].split('_')
		p_three = possible_set[2].split('_')

		arr_num = [p_one[0], p_two[0], p_three[0]]
		arr_color = [p_one[1], p_two[1], p_three[1]]
		arr_shape = [p_one[2], p_two[2], p_three[2]]
		arr_solid = [p_one[3], p_two[3], p_three[3]]

		#return self.check_feature(arr_num) and self.check_feature(arr_color) and self.check_feature(arr_shape) and self.check_feature(arr_solid)
		return True

	def isSetInHand(self, gameHand):
		for s in self.rSubset(gameHand, 3):
			p_one = s[0].split('_')
			p_two = s[1].split('_')
			p_three = s[2].split('_')
			
			arr_num = [p_one[0], p_two[0], p_three[0]]
			arr_color = [p_one[1], p_two[1], p_three[1]]
			arr_shape = [p_one[2], p_two[2], p_three[2]]
			arr_solid = [p_one[3], p_two[3], p_three[3]]

			if self.check_feature(arr_num) and self.check_feature(arr_color) and self.check_feature(arr_shape) and self.check_feature(arr_solid):
				return True
		return False
		
	def rSubset(self, arr, r):
		return list(combinations(arr, r)) 

	def check_feature(self, arr):
		if arr[0] == arr[1]:
			return arr[1] == arr[2]
		else:
			return arr[0] != arr[2] and arr[1] != arr[2]

	def removeSet(self, possibleSet):
		print("possisble set in game.py")
		print(possibleSet)
		print("gamehand in game.py")
		print(self.gameHand)
		for p in possibleSet:
			pFixed = p.split(".")[0]
			for g in self.gameHand:
				if pFixed == g:
					self.gameHand.remove(g)
		return self.gameHand

	def getPoints(self, playerID):
		print(self.playerPoints)
		return self.playerPoints[str(playerID)]

	def setPoints(self, playerID, newPoints):
		self.playerPoints[playerID] = newPoints

	def getAllPlayerPoints(self):
		return self.playerPoints

	def getRemainingDeckSize(self): # NAZLI: when i saw the call this method in app.py i was confused because i thought you were getting a list of cards
		# people should be able to tell what the function does from the name, like you can also make it getDeckSize or anything else you want 
		# but make sure the name implies you are getting size
		return len(self.cards)


def playGames():
	numPlayers = 4 #TODO: dont hard code num players
	
	deck = createDeck()
	game = Game(deck, numPlayers)

def createDeck():
    number = ["one", "two", "three"]
    color = ["purple", "red", "green"]
    shape = ["diamond", "oval", "squiggle"]
    fill = ["shaded", "solid", "empty"]

    deck = []

    for n in number:
        for c in color:
            for s in shape:
                for f in fill:
                    deck.append(n + "_" + c + "_" + s + "_" + f)

    return deck

def createGame(playerIDs):
	deck = createDeck()
	game = Game(deck, playerIDs)
	return game

# def main():
# 	playGames()

# if __name__ == "__main__":
# 	main()