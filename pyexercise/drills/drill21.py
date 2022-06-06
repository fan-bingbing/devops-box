def add(a, b):
    print(f"ADDING {a} + {b}")
    return a + b

def subtract(a, b):
    print(f"SUBTRACTING {a} - {b}")
    return a - b

def multiply(a, b):
    print(f"MULTIPLING {a} * {b}")
    return a * b

def divide(a, b):
    print(f"DIVIDING {a} / {b}")
    return a / b


print("Let's do some math with just functions!")

age = add(30, 5)
height = subtract(78, 4)
weight = multiply(90, 2)
iq = divide(100, 2)

print(f"Age: {age}, Height：{height}, Weight：{weight}, IQ：{iq}")


# A puzzle for the extra credit, type it in anyway.
print("Here's a puzzle.")

what = add(age, subtract(height, multiply(weight, divide(iq, 2))))
# creating a formula using functions

print("That becomes:", what, "Can you do it by hand?")

# focus on a goal and know the purpose of all your efforts!
