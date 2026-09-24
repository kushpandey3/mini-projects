import random
def getValidInt(question, min = float("-inf"), max = float("inf"), disallowedInputs = []):
    while(True):
        try: 
            inp = int(input(question))
            if(inp < min or inp > max):
                print(f"The input should be between {min} and {max}. ")
            elif inp in disallowedInputs:
                print("There's no use in guessing a number again, you can have your turn back. ")
            else:
                return inp
        except:
            print("Please respond with an integer. ")

def getValidYN(question):
    while(True):
        try:
            inp = input(question)
            if(inp[0]=='y' or inp[0]=='Y'):
                return True
            elif(inp[0]=='n' or inp[0]=='N'):
                return False
            else:
                print("Please answer with a Y or a N")
        except:
            print("Please answer with a Y or a N")

def determineDifficulty():
    if(getValidYN("Would you like to play with a preset difficulty? (Y/N) (The alternative is a custom difficulty)")):
        diff = getValidInt("Would you like to play at a toughness of 1, 2, or 3? ", 1, 3)
        maxAttempts = 10 if diff == 1 else 7 if diff == 2 else 3
        maxNumber = 15 if diff == 1 else 30 if diff == 2 else 50
    else:
        maxAttempts = getValidInt("How many attempts would you like to have? ")
        maxNumber = getValidInt("How many numbers would you like to guess between? ")
    return [maxAttempts, maxNumber]

maxAttempts, maxNumber = determineDifficulty()
highScore, cont = 0, True
while(cont):
    rand = random.randint(0, maxNumber)
    currAttempts = maxAttempts 
    guesses = []
    while currAttempts > 0:
        print("\n")
        guess = getValidInt(f"Guess a number between 0 and {maxNumber}. ", 0, maxNumber, guesses)
        currAttempts -= 1
        guesses.append(guess)
        if(guess==rand):
            if(currAttempts > highScore):
                highScore = currAttempts
                print(f"Congrats! You have a new high score of {highScore}")
            if(currAttempts>maxAttempts/2):
                print("You got it, Genius! ")
            elif(currAttempts==0):
                print("Wow, you managed to get it in the nick of time. ")
            else:
                print("Good work, you got it. ")
            break
        elif currAttempts==0:
            print(f"Womp womp. The number was {rand}. ")
        else:
            print(f"You have {currAttempts} attempts left. You have guessed {guesses} so far. ")
        print("\n")
    cont = getValidYN("Would you like to play again? (Y/N) ")
    if cont and getValidYN("Would you like to change the difficulty? (Y/N)"):
       maxAttempts, maxNumber = determineDifficulty()
       highScore = 0
else:
    print("Thank you for playing. ")
