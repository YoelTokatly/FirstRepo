
def get_user_input():
    b = 0
    while b == 0:
        try:
                user_answer = input("Choose a number between 1 and 9: ")
                user_number = int(user_answer)
                test = user_number % 2
                if test == 0:
                    print("Even")
                else:
                    print("Odd")   
                b = 1
        except ValueError:
                print("Please enter a valid number.")
                b = 0

    
    





if __name__ == "__main__":
    get_user_input()
