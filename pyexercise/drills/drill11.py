print("How old are you?", end='')
# end='' tells print to not end the line with a newline character and go to the next line.

age = input()# take string input from user
print("How tall are you?", end='')
height = input()
print("How much do you weigh?", end='')
weight = input()

print(f"So, you're {age} old, {height} tall and {weight} heavy.")
