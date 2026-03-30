
# Problem 

# Fix this design: 

# class Bird: 
#    def fly(self): 
#        pass 
 
# class Penguin(Bird): 
#    def fly(self): 
#        raise Exception("Cannot fly") 
# Task 

# Redesign system so: 

# No subclass breaks behavior 

# LSP is followed 

class Bird:
    def eat(self):
        print("Eating...")


class FlyingBird(Bird):
    def fly(self):
        print("Flying...")


class Sparrow(FlyingBird):
    pass


class Penguin(Bird):
    def swim(self):
        print("Swimming...")





