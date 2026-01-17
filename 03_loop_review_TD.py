"""
    Program 3: Loop Review
    Student Name: Timothy Daehnert
    Course: CSCI 409 D1
"""

# 1. Write a FOR loop to iterate over the airports list
airports = ["MYR", "MCO", "ATL", "LGA"]
for a in airports:
    print(a)

# 2. Use the range function to loop through the code 5 times
for x in range(5):
    for item in airports:
        print(item)