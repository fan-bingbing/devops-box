# read file, open()function default to read as text file
# f = open("drill17_example.txt")
#
# print(f.read())
#
# print(f.readline())
# print(f.readline())
#
# for x in f:
#     print(x)
# f.close()

# write file, "a"will append to the end of file, "w" will overwrite file
# f = open("drill17_example.txt", "a")
# f.write("Now we have more content!")
# f.close
# f = open("drill17_example.txt", "r")
# print(f.read())

#create, delete file or folders in python
def myfunc(n):
    return lambda a : a**n

mydoubler = myfunc(2)
print(mydoubler(8))
