import datetime
import os
import sys
import time

def cls():
    os.system("clear")

def list_items(db):
    for i, item in enumerate(db):
        print(str(i) + ". " + repr(item))
    print()

# Get a string from the user
def get_string(msg):
    user_input = input(msg)
    if user_input == "q":
        print("Exiting.")
        sys.exit(0)
    return user_input

# Pass a message and a numerical type to get user input.
def get_number(msg,num_type):
    return_value = 0
    while True or not isinstance(return_value, num_type):
        try:
            # Get the string first then try to evaluate it separately
            return_value = input(msg)
            return_value = eval(return_value)
            '''if "/" in return_value:
                return_value = float(return_value.split("/")[0])/float(return_value.split("/")[1])'''
            return_value = num_type(return_value)
        except:
            print("\0")
            if return_value == 'q':
                sys.exit(0)
            print("Input requires a " + str(num_type) + ". Enter q to exit.")
        else:
            break
    return return_value

def path_exists(log_path):
    exists = False
    file_name = log_path.split("/")[-1]
    dir_name = log_path[:-len(file_name)]
    if os.path.exists(dir_name):
        if os.path.isfile(log_path):
            exists = True
    else:
        # In addition to checking whether the file exists, if the directory does not exist when it is created here, then it will be added
        os.mkdir(dir_name)
    return exists

def remove_database_item(db):
    list_items(db)
    index = get_number("Enter index of database item to remove: ",int)
    y_or_n = ""
    while (y_or_n != "y") and (y_or_n != "n"):
        y_or_n = input("Are you sure you want to remove " + str(db[index]) + "? (Y/n)").lower()
    if y_or_n == "y":
        db.pop(index)
    else:
        return 

# convert a list of items into the same type
def convert(array,object_type):
    new_array = []
    for item in array:
        new_array.append(object_type(item))
    return new_array

def get_log():
    year = get_number("Year: ", int)
    month = get_number("Month: ", int)
    day = get_number("Day: ", int)
    day_name = datetime.date(year,month,day).strftime("%a")
    string = "%.4d_%.2d_%.2d_%s_food_log.txt" % (year,month,day,day_name)
    return string

def find(pattern, arr, caseInsensitive=True):
    if caseInsensitive:
        pattern = pattern.lower()
    matchArr = []
    currentIndex = 0
    prevIndex = 0
    for arrIndex, string in enumerate(arr):
        originalString=str(string)
        if caseInsensitive:
            string = str(string).lower()
        for charIndex, char in enumerate(string):
            if char == pattern[currentIndex]:
                currentIndex += 1
                prevIndex = charIndex
            if charIndex-prevIndex > 1:
                #print(str(charIndex-prevIndex) + ":\tWord: " + string)
                currentIndex=0
            if currentIndex == len(pattern):
                matchArr.append((arrIndex,originalString))
                currentIndex=0
                break
    return matchArr
