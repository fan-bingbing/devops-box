from sys import argv
# argv is a module
# read the WYSS section for how to run This
# argv is the "argument varible", this varibale holds arguments you pass to script.
script, first, second, third = argv
# unpack argv, assign to four varibles in order that you can work with.
# command line arguments come in as strings.

print("The script is called:", script)
print("Your first variable is:", first)
print("Your second variable is:", second)
print("Your third variable is:", third)
# how to run this file? for example: python drill13.py first second third (4 argvs)
# first second third, they are three command line arguments
