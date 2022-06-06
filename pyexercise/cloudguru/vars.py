class User:
    active_users = []

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def activate(self):
        if not self.is_activate():
            self.__class__.active_users.append(self)
    # how to use class level attributes
    # this way when class name Users change, code will still work

    def deactivate(self):
        if self.is_activate():
            self.__class__.active_users.remove(self)

    def is_activate(self):
        return self in self.__class__.active_users


# python -i vars.py  this gives python shell and have access to User class
# me.__dict__ this gives dictionary representation of data that me object is holding
# User.__dict__ this gives everything that User class has
# dir(me) this gives all functionality that me instances has
# help(User) this gives tree view of class User
# isinstance(me, User) shows if me is instance of class User
# customizing double underscore method (dunder methods)...






me = User("keith", "keith@example.com")
me.name = "Aaron FAN"

print(f"Active: {me.is_activate()} Active_users: {User.active_users}")
me.activate()
print(f"Active: {me.is_activate()} Active_users: {User.active_users}")
me.deactivate()
print(f"Active: {me.is_activate()} Active_users: {User.active_users}")
me.active_users = "just me"
print(f"Active: {me.active_users} Active_users: {User.active_users}")
