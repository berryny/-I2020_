import random

computer_choices = {
    0: 'rock',
    1: 'paper',
    2: 'scissors',
}
user_choices = {
    'R': (0, 'rock'),
    'P': (1, 'paper'),
    'S': (2, 'scissors')
}

class RockPaperScissors:
    def __init__(self, rps_computer_choices,rps_user_choices):
        self.rps_computer_choices = rps_computer_choices
        self.rps_user_choices = rps_user_choices
    # other methods below
    
    def rps_computers_turn(self):
        turn = random.randint(0,2)
        return (turn, self.rps_computer_choices[turn])    

    def rps_your_turn(self, selection):
        self.selection = selection
        user_correct_input = False
        while not user_correct_input:
            user_input = self.selection

            if user_input in ['R', 'P', 'S']:
                 user_correct_input = True
            else:
                print("Hey there, please put one of ['R', 'P', 'S'] to play the game.")
                user_input = input("Hey there, please choose from ['R', 'P', 'S'] to play this game.")

        return user_input, self.rps_user_choices[user_input]

    def compare_turns(self, computer_choice,user_choice):

        if (user_choice[0] - computer_choice[0]) % 3 == 0:
            return "Tied"

        elif (user_choice[0] - computer_choice[0]) % 3 == 1:
            return True

        elif (user_choice[0] - computer_choice[0]) % 3 == 2:
            return False
        else:
            return None
        
    def won_round(self,argvar):
        self.argvar = argvar
        computer_choice = self.rps_computers_turn()
        your_choice = self.rps_your_turn(self.argvar)
        user_choice = your_choice[1]
        compare_choices = self.compare_turns(computer_choice,user_choice)
        return compare_choices
    
    @staticmethod
    def game_round(arg):
        your_score = 0
        computer_score = 0

        play = RockPaperScissors(computer_choices,user_choices).won_round(arg)
        if play == True:
            your_score += 1
            print(f"User Wins.")
        elif play == False:
            computer_score += 1
            print(f"Computer Wins")
        elif play == "Tied":
            your_score += 1
            computer_score += 1
            print(f"Tied")
        else:
            print(f"Unexpected Result.")

        return f"Scores -> You: {your_score} and Computer: {computer_score}"


if __name__ == "__main__":
    import sys
    rps = RockPaperScissors(computer_choices,user_choices)
    print(rps.game_round(sys.argv[1]))
