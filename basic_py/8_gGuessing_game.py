
#Guessing Game
import random


the_number = random.randint(1, 5)


try:
    user_guess = int(input("Guess a number between 1 and 5: or 100 to exit: "))
    print(user_guess)
except ValueError:
    user_guess = int(input("Guess a number between 1 and 5: or 100 to exit:  "))
    exit()


counter = 0
while counter < 5 :
    if  user_guess == 100:
        counter = 5
    elif user_guess > the_number:
        print(f"You selected {user_guess} I selected {the_number}")
        print("Too high!")
        user_guess = int(input("Try again: "))
    elif user_guess < the_number:
        print(f"You selected {user_guess} I selected {the_number}")
        print("Too low!")
        user_guess = int(input("Try again: "))
    elif user_guess == the_number:
        print(f"You selected {user_guess} I selected {the_number}")
        print("Correct! You guessed it!")
        counter = 5

