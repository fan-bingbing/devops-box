my_nums_1 = [x*x for x in [1,2,3,4,5]]

my_nums_2 = (x*x for x in [1,2,3,4,5])

print(my_nums_1)



for num in my_nums_2:
    print(num)
