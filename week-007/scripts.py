# Code Along:
# How can we make a Guessing Game module.
from random import randint

class GuessingGame:
    def __init__(self):
        self.max_guesses = 3
        self.guesses = 0
        self.random_number = randint(1,3)
        
    @staticmethod
    def welcome_message():
        print("Welcome to guessing game.")
        
    def start(self):
        print(self)
        GuessingGame.welcome_message()
        win = self.handle_guesses()
        if win:
            print("you have won")
        else: 
            print("you have lost")
            
    def handle_guesses(self):
        while self.guesses < self.max_guesses:
            guess = input("Enter a guess: ")
#             print(self.guesses)
            if int(guess) == self.random_number:
                return True
            self.guesses += 1
        print("game over")
        return False
if __name__ == "__main__":
    game = GuessingGame()
    game.start()