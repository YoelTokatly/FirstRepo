#Movie‑Night Ticket Calculator
import sys
age= int(input("Age?"))
if age < 0:
    print("Invalid age")
    sys.exit()
    
day= input("select 'd' for weekday/ 'w' weekend)?").lower()
if day not in ["d", "w"]:
    print("Invalid day")
    sys.exit(1)
loyalty= input("Loyalty member (y/n)?").lower()
if loyalty != "y":
    loyalty = "n"
    

#calculating the price
base= 20

if age < 13:
    base *= 0.5
elif age > 60:
    base *= 0.7

if day == "w":
    base += 5

if loyalty == "y":
    base -= 2
    
print(f"Your ticket price is: {base:.2f}")
    

