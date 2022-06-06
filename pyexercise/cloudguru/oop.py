

# instance variables, class varbiables
# class methods and static methods


class Employee:

    number_of_emps = 0
    raise_amount = 1.04

    def __init__(self, first, last, pay, hours_per_week=37.5):
        self.first = first
        self.last = last
        self.pay = pay
        self._hours_per_week = hours_per_week # hiding attribute using single and doublke underscore
        # single underscore attribute are not meant to accessible by user


        # self.email = first + '.' + last + '@company.com'
        Employee.number_of_emps += 1 # access class variable

    @property # this is default getter
    def hours_per_week(self):
        return self._hours_per_week

    @hours_per_week.setter # this is how setter works
    def hours_per_week(self, value):
        self._hours_per_week = value

    @property # allow us define a method and access it as if it was a attribute
    def email(self):
        return f"{self.first}.{self.last}@company.com"

    @property
    def fullname(self): # show how to define getter and setter to change instance attribute
        return f"{self.first},{self.last}"

    @fullname.setter # show how to define getter and setter
    def fullname(self, name):
        first, last, pay = name.split(' ')
        self.first = first
        self.last = last
        self.pay = pay



    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount) # access class variable using self.

    @classmethod
    def set_raise_amount(cls, amount): # this is class method
        cls.raise_amount = amount # perform operations on class varible

    @classmethod
    def from_string(cls, emp_str): # use class method acting as constructor
        first, last, pay = emp_str.split('-')
        return cls(first, last, pay) # instantiate from a certain format of string

    @staticmethod # it doese not depends on any class or instance varibles but logically related
    def is_workday(day): # this is static method
        return day.weekday() == 5 or day.weekday() == 6

    def __repr__(self): # meant to be seen by develpers for debug or logging
        return f"Employee('{self.first}', '{self.last}', '{self.pay}')"
        # return a string that can be used to instantiate a new object

    def __str__(self): # meant to be seen by end-users
        return f"{self.fullname()} - {self.email}"


    def __add__(self, other): # define how to add two objects, add salary together
        return self.pay + other.pay

    def __len__(self): # another example of Dunder method
        return len(self.fullname())











# import datetime
# my_date = datetime.date(2021, 6, 18)
# print(Employee.is_workday(my_date))




emp_1 = Employee('Corey', 'Schafer', 50000)
print(emp_1.first)
print(emp_1.email)
print(emp_1.pay)
print(emp_1.fullname)
print(emp_1.hours_per_week)

emp_1.fullname = 'Aaron FAN 1000'
emp_1.hours_per_week = 40
print(emp_1.first)
print(emp_1.email)
print(emp_1.pay)
print(emp_1.fullname)
print(emp_1.hours_per_week)


# emp_2 = Employee('Aaron', 'Fan', 60000)

# print(emp_1 + emp_2)

# print(len(emp_1))
# new_emp = Employee.from_string('John-Doe-70000')
#
# Employee.set_raise_amount(1.05) # call class method using class
# print(emp_1.raise_amount)
# print(emp_2.raise_amount)
# print(new_emp.email)
# print(new_emp.pay)
