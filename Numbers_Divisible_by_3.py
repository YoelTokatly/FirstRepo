#Numbers Divisible by 3

#for loop
start = int(input("Enter a starting number: "))
end = int(input("Enter an ending number: "))
divider = int(input("Enter a divider: "))

my_list = list(range(start, end + 1))
div_list = []

for number in my_list:
    if number % divider == 0:
        div_list.append(number)
        print(number)
print(f"Numbers divisible by {divider} between {start} and {end}: {div_list}")        


#while loop
start = int(input("Enter a starting number: "))
end = int(input("Enter an ending number: "))    
divider = int(input("Enter a divider: "))
div_list = []

counter = start
while counter <= end:
    if counter % divider == 0:
        print(counter)
        div_list.append(counter)
    counter += 1
    

