people = 20
cats = 30
dogs = 15

# if this boolean expression is True, then run the code under it, otherwise skip it.
# A colon at the end of a line is telling python you are going to create a new "block"
# and then indenting four spaces tells python what lines of code are in that block.
if people < cats:
    print("Too many cats! The world is doomed!")

if people > cats:
    print("Not many cats! The world is saved!")

if people < dogs:
    print("The world is drooled on!")

if people > dogs:
    print("The world is dry!")


dogs += 5

if people >= dogs:
    print("People are greater than or equal to dogs.")

if people <= dogs:
    print("People are less than or equal to dogs.")

if people == dogs:
    print("People are dogs.")
