######## OVERALL TODO: #########
# make multiplayer 
# make gui
################################
import random 

class Game:
	gameHand = []
	numPlayers = 0
	player1Points = 0 #TODO: dont hardcode just one player; make it an array of players

	def __init__(self, cards, numPlayers):
		self.numPlayers = numPlayers
		self.play(cards)

	def dealInitial(self, cards):
		random.shuffle(cards)
		print(len(cards))
		for x in range(9):
			self.gameHand.append(cards.pop(0))
		print(len(cards))
	
	def 
		while(len(cards) > 0):
			print(gameHand)
			#take user input:
			choice = input("Press s to select a set OR press d to deal 3 more cards:\n")
			
			if choice == "d":
				for x in range(3):
					gameHand.append(cards.pop(0))
				print(len(cards))

			if choice == "s":
				self.chooseSet(gameHand, cards)
			
			if choice != "s" and choice != "d":
				print("Whoops! You didn't choose s or d.")

		if(len(cards) == 0 and len(gameHand) > 0):
			choice = input("Press s to select a set OR press d for done (if you think there are no more sets):\n")
			if choice == "d":
				print("Thanks for playing! Overall, you got " + str(self.player1Points) + " points.")

			if choice == "s":
				self.chooseSet(gameHand, cards)

			if choice != "s" and choice != "d":
				print("Whoops! You didn't choose s or d.")

	def chooseSet(self, gameHand, cards):
		selection = []
		print("Choose the three numbered cards that are your set:\n")

		for x in range(3):
			while True:
				try:
					sel = int(input("Card " + str(x+1) + ": "))-1 #minus 1 because user input wouldnt account for list starting at 0
					#sel = int(input("Card: "))-1
					if sel < len(gameHand):
						selection.append(sel)
						break
					print("You inputted a number out of range. Try again: ")
				except Exception as e:
					print(e)

		print("Your card selection: ")
		print(selection)

		users_set = [gameHand[selection[0]], gameHand[selection[1]], gameHand[selection[2]]]

		print("users set: ")
		print(users_set)
		print("remainder of gameHand: ")
		print(gameHand)
		#check if set is correct:
		if self.isSet(users_set):
			print("Good job! You got a set.")
			self.player1Points += 1
			print("You now have " + str(self.player1Points) + " points.")
			#remove those cards from gameHand:
			for u in users_set:
				for g in gameHand:
					if g == u:
						gameHand.remove(g)
			#add three more cards to gameHand:
			if len(cards) >= 3:
				for x in range(3):
					gameHand.append(cards.pop(0))
		else:
			print("Nope! That wasn't a set. Want to try again?")

	def isSet(self, possible_set):
		p_one = possible_set[0].split('_')
		p_two = possible_set[1].split('_')
		p_three = possible_set[2].split('_')

		arr_num = [p_one[0], p_two[0], p_three[0]]
		arr_color = [p_one[1], p_two[1], p_three[1]]
		arr_shape = [p_one[2], p_two[2], p_three[2]]
		arr_solid = [p_one[3], p_two[3], p_three[3]]

		return self.check_feature(arr_num) and self.check_feature(arr_color) and self.check_feature(arr_shape) and self.check_feature(arr_solid)

	def check_feature(self, arr):
		if arr[0] == arr[1]:
			return arr[1] == arr[2]
		else:
			return arr[0] != arr[2] and arr[1] != arr[2]



def playGames():
	numPlayers = 4 #TODO: dont hard code num players
	
	deck = createDeck()
	game = Game(deck, numPlayers)

	################# DUMMY GAME TESTER #################
	f = "one_purple_oval_empty"
	s = "two_red_oval_empty"
	t = "three_green_oval_empty"
	dum_arr = [f, s, t]
	print ("THIS IS OUR RESULT: " )
	print(game.isSet(dum_arr))
	#####################################################

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

def createGame():
	numPlayers = 4 #TODO: dont hard code num players
	deck = createDeck()
	game = Game(deck, numPlayers)
	return game

# def main():
# 	playGames()

# if __name__ == "__main__":
# 	main()