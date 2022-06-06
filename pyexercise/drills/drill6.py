types_of_people = 10 # interger variable
x = f"There are {types_of_people} types of people." # format string variable

binary = "binary" # string variable
do_not = "don't" # string variable
y = f"Those who know {binary} and those who {do_not}." # format string variable

print(x)
print(y)

print(f"I said: {x}") # print a format string
print(f"I also said: '{y}'") # print a format string

hilarious = True
joke_evaluation = "Isn't that joke so funny?! {}"

print(joke_evaluation.format(hilarious))

w = "This is the left side of ..."
e = "a string with a right side."

print(w + e)
