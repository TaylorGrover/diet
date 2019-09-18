#! /data/data/com.termux/files/usr/bin/python3

### This file contains a couple of input verification functions

from database import Database
import os
from serving import Serving
import sys
import time

def cls():
    os.system("clear")

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
            return_value = input(msg)
            if "/" in return_value:
                return_value = float(return_value.split("/")[0])/float(return_value.split("/")[1])
            return_value = num_type(return_value)
        except:
            print("\0")
            if return_value == 'q':
                sys.exit(0)
            print("Input requires a " + str(num_type) + ". Enter q to exit.")
        else:
            break
    return return_value

def add_meal(msg,db):
    list_items(db)
    meal_index = get_number(msg,int)
    while meal_index > len(db) or meal_index < 0:
        meal_index = get_number(msg)
    servings = get_number("Enter the number of servings: ",float)
    return db[meal_index],servings

def list_items(db):
    for i, item in enumerate(db):
        print(str(i) + ". " + repr(item))
    print()

def create_new_food_item(db):
    list_items(db)
    macros = [0,0,0]
    macros_dict = {0:"Carbs: ",1:"Fats: ",2: "Protein: "}

    food_name = get_string("Enter the name of the food: ")
    print("Enter the carbs, fats, and protein in grams per serving")
    
    for i in range(3):
        macros[i] = get_number(macros_dict[i],float)
        if not isinstance(macros[i],float):
            print("Unable to parse macros.")
            sys.exit(0)
    serving_description = get_string("Enter a serving description: (i.e. macros PER WHAT): ")
    new_serving = Serving(food_name,macros,serving_description)
    db.add(new_serving)

def path_exists(log_path):
    exists = False
    file_name = log_path.split("/")[-1]
    dir_name = log_path[:-len(file_name)]
    if os.path.exists(dir_name):
        if os.path.isfile(log_path):
            exists = True
    else:
        # In addition to checking whether the file exists, if the directory does not exist then it is created here
        os.mkdir(dir_name)
    return exists

def get_current_log(log_path):
    lines = []
    quantities = []
    current_log = ""
    is_path = path_exists(log_path)
    if is_path:
        with open(log_path,"r") as f:
            for line in f:
                lines.append(line.split("\t")[1].strip())
                quantities.append(line.split("\t")[0].strip())
            f.seek(0)
            current_log = f.read()
    return [current_log,lines,quantities]

# This will be used to write a meal entry to the file which reads the data from the log in the path provided
def add_to_log(serving,servings,log_path):
    current_log,lines,quantities = get_current_log(log_path)
    if current_log == "":
        with open(log_path,"w") as f:
            print("Writing in empty log")
            f.write(str(servings)+"\t" + repr(serving) + "\n")
            f.write(str(format(servings*(serving.carbs*4 + serving.fats*9 + serving.protein*4),".2f")) + "\t" + str(servings*serving.carbs) + "," + str(servings*serving.fats) + "," + str(servings*serving.protein))
    else:
        calories = float(quantities.pop(-1).strip())
        macros = lines.pop(-1).strip()

        carbs,fats,protein = macros.split(",")
        carbs = float(carbs) + servings*serving.carbs
        fats = float(fats) + servings*serving.fats
        protein = float(protein) + servings*serving.protein

        if repr(serving) in lines:
            index = lines.index(repr(serving))
            quantities[index] = float(quantities[index]) + servings
        else:
            for i in range(len(lines)):
                if serving.name <= lines[i]:
                    lines.insert(i,repr(serving))
                    quantities.insert(i,servings)
                    break
                elif i == len(lines)-1:
                    lines.append(repr(serving))
                    quantities.append(servings)

        calories = carbs*4 + fats*9 + protein*4

        quantities.append(calories)
        lines.append(str(format(carbs,".2f")) + "," + str(format(fats,".2f")) + "," + str(format(protein,".2f")))

        with open(log_path,"w") as f:
            for i in range(len(lines)):
                f.write(str(quantities[i]) + "\t" + lines[i] + "\n")

def show_meals(log_path):
    current_log,lines,quantities = get_current_log(log_path)
    calories = quantities.pop(-1)
    carbs,fats,protein = lines.pop(-1).split(",")
    for quantity,line in zip(quantities,lines):
        print(str(quantity) + "\t" + str(line))
    print("\nTotal Calories: %.2f\nCarbs: %.2f\nFats: %.2f g\nProtein: %.2f g" % (float(calories),float(carbs),float(fats),float(protein)))
    

# This very simple program will execute sequentially, and will exit if anything goes wrong.
# There are only two main options: 1. Meal entries, or 2. Create new food items for the database

# Directory strings (need to be changed depending on platform)
database_dir = "/data/data/com.termux/files/home/.food/"
log_dir = "/data/data/com.termux/files/home/food_logs/"

# First thing to do is get the database
database = Database(dirpath=database_dir,filename="foods.dat",fieldname="name")

# Strings
start_msg = "\nEnter <q> to exit.\n\n1. Enter new meal\n2. Add a food item to the database\n3. View Catalog\n4. Show Current Log\n: "
add_meal_msg = "Add an item from the list: "

# The directory name for the log file. Will use the same file for a 24 hour period because the name
# will only change once a day has passed.
log_path = "%s%d_%.2d_%.2d_%s" % (log_dir,time.localtime()[0],time.localtime()[1],time.localtime()[2],time.ctime().split(" ")[0] + "_food_log.txt")

# Get the first input from the user
user_input_1 = get_number(start_msg,int)

# Clear the terminal
cls()

## 1 for meal entry and 2 for adding new food to database for future retreival
while user_input_1 != 'q':
    if user_input_1 == 1:
        meal_entry,servings = add_meal(add_meal_msg,database)
        add_to_log(meal_entry,servings,log_path)
    elif user_input_1 == 2:
        create_new_food_item(database)
    elif user_input_1 == 3:
        list_items(database)
    elif user_input_1 == 4:
        show_meals(log_path)
    user_input_1 = get_number(start_msg,int)
    cls()
