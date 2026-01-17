"""
    Program 1: List Review
    Student Name: Timothy Daehnert
    Course: CSCI 409 D1
"""

# 1. Create a list named my_list with 5 strings in it

# Use the following list to answer the questions 2 - 7
cars = ["ford", "dodge", "porsche", "toyota", "jeep", "chevy"]

# 2. Complete the code to print the third item in the list
print(cars[2])

# 3. Use negative indexing to print the last item in the list
print(cars[-1])

# 4. Use slicing to print the third, fourth, and fifth elements
x = slice(3,6)
print(cars[x])

# 5. Write the code to add the item fiat to the end of the list
cars.append("fiat")

# 6. Write the code to add the item pontiac as the third item in the list
cars.insert(2, "pontiac")

# 7. Write the code to print the number of items in the cars list
print(len(cars))