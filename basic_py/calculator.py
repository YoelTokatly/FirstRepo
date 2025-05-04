import sys


def calculator(a, b ,operation):

# check if the input is a number or string 
    try:
        if '.' in a or '.' in b:
            a = float(a)
            b = float(b)
        else:   
            a = int(a)
            b = int(b)
    except ValueError:
        return "Invalid input, please enter numbers only"
#calc
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if operation == 'add':
            return a + b
        elif operation == 'subtract':
            return a - b
        elif operation == 'multiply':
            return a * b
        elif operation == 'divide':
            if b != 0:
                return a / b
            else:
                print("Cannot divide by zero")
        else:
            print("Invalid operation, choose from 'add', 'subtract', 'multiply', 'divide'")


def main ():
    print("Welcome to the calculator!")
    print ("0.",sys.argv[0])
    print("a=",sys.argv[1])
    print("B=",sys.argv[2])
    print("operator is:",sys.argv[3])
    if len(sys.argv) != 4:
        print("Usage: python calculator.py <number1> <number2> <operation>")
        return
    pass

    a = sys.argv[1]
    b = sys.argv[2]
    operation = sys.argv[3]
    
    
    result = calculator(a, b, operation)
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
        