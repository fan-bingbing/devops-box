from sys import argv
from os.path import exists # import exists function to check if a file exist

script, from_file, to_file = argv

print(f"Copy from {from_file} to {to_file}")

# We could do these on one line, how?
in_file = open(from_file)
in_data = in_file.read()

print(f"The input file is {len(in_data)} bytes long")

print(f"Does the output file exist? {exists(to_file)}")
print("Ready, hit RETURN to continue, CTRL-C to abort.")
input()

out_file = open(to_file, 'w')
out_file.write(in_data)

print("Alright, all done.")

out_file.close()
in_file.close()
