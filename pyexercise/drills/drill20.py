from sys import argv

script, input_file = argv

def print_all(f):
    print(f.read()) #

def rewind(f):
    f.seek(0)
    # seek() moving to the start of the file(0 bytes), it deal with bytes

def print_a_line(line_count, f):
    print(line_count, f.readline(), end = "")
    # end = "" avoid readline() returning \n
    # readline() scans each byte of the file until it finds
    # a \n character, then stops reading the file to return what it found so far.
    #

current_file = open(input_file)

print("First let's print the whole file:\n")

print_all(current_file)

print("Now let's rewind, kind of like a tape.")

rewind(current_file)

print("Let's print three lines:")

current_line = 1
print_a_line(current_line, current_file)

current_line = current_line + 1 # the same as current_line += 1
print_a_line(current_line, current_file)

current_line = current_line + 1
print_a_line(current_line, current_file)
