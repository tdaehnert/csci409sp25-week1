"""
    Program 5: Classes Review
    Student Name: Timothy Daehnert
    Course: CSCI 409 D1
"""

# 1. Create a class named Rectangle
#    1pt
class Rectangle:
    # 2. Create 2 class variables called length and width
    #    2pts
    length = 0
    width = 0

    # 3. Create an init function
    def ___init___(self, length, width):
        self.length = length
        self.width = width

    # 4. Create a function called area
    def area(self):
        return self.length * self.width

# 5. Create a new instance of the rectangle class
#    with a length of 10 and a width of 8
#    assign the class to the variable r1
r1 = Rectangle()
r1.length = 10
r1.width = 8

# 6. Print the length of the rectangle previously created
print(r1.length)

# 7. Print the area of the rectangle previous created
print(r1.area())