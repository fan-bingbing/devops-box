from sys import argv

script, filename = argv

text = open(filename)
# a new command named open, it just open file,  but doesn't get actual content
# command also known as function and method


print(f"Here's your file {filename}:")
print(text.read())
# in variable text, it's a file, call a function named read
text.close()
# close file in the end

print("Type the filename again:")
file_again = input("> ")

text_again = open(file_again)

print(text_again.read())
text_again.close()
#close file in the end
