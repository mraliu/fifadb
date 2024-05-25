import os

directory = os.fsencode("images")
    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    print(filename)