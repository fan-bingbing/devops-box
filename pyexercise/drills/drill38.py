ten_things = "Apples Oranges Crows Telephone Light Sugar"

print("Wait there are not 10 things in that list. Let's fix that.")

stuff = ten_things.split(' ') # stuff becomes a list from a string by calling split(' ')
more_stuff = ["Day", "Night", "Song", "Frisbee", "Corn", "Banana", "Girl", "Boy"]


while len(stuff) != 10:
    next_one = more_stuff.pop() # pop() pops out the last element from a list
    print("Adding: ", next_one)
    stuff.append(next_one)
    print(f"There are {len(stuff)} items now.")

print("There we go: ", stuff)

print("Let's do some things with stuff.")

print(stuff[1]) # stuff[1] is the second element in the list
print(stuff[-1]) # stuff[-1] is the last element in the list
print(stuff.pop()) # pop() pops out the last element in the list
print(' '.join(stuff)) # stuff becomes a string from a list by calling join()
print('#'.join(stuff[3:5])) # in stuff list from element 3 to element 4, it does not include element 5
