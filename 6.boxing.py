import random
"""
1 = The Jab
2 = The Cross
3 = The Lead Hook
4 = The Rear Hook
5 = The Lead Uppercut
6 = The Rear Uppercut

"""
punches= {
    1: ['Jab','Cross'],
    2: ['Cross','Lead Hook'],
    3: ['Lead Hook','Rear Hook'],
    4: ['Rear Hook','Lead Uppercut'],
    5: ['Lead Uppercut','Rear Uppercut'],
    6: ['Rear Uppercut','Jab']
}
counter = 0
while counter != 1:

    user_punch= int(input("Enter a number between 1 and 6: "))
    user_punch= punches[user_punch]

    pc_punch = punches[random.randint(1, 6)]
    print(f"you choose {user_punch[0]}  and i choose {pc_punch[0]}")

    if user_punch[0] == pc_punch[1]:
        print("you win!")
        counter += 1
    elif user_punch[1] ==  user_punch[0]:
        print("you lose!")
        counter += 1
    else:
        print("Draw!")
        print(f"User Punch: {user_punch[0]}")