#! /data/data/com.termux/files/usr/bin/python3

### This file contains a couple of input verification functions

from database import Database
import os
from serving import Serving
import sys
import time
from utilities import *


def add_meal(msg,db):
    list_items(db)
    meal_index = get_number(msg,int)
    while meal_index > len(db) or meal_index < 0:
        meal_index = get_number(msg)
    servings = get_number("Enter the number of servings: ",float)
    return db[meal_index],servings

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

# Function to estimate the macronutrients of a food entry
def estimate_calories(log_path):
    print("Estimate entry calories called. (Functionality not yet added.)")
    current_log,lines,quantities = get_current_log(log_path)

## Delete entry from meal log (removal of calories and macros)
def delete_entry():
    print("Delete entry called. (Functionality not yet added.)")
    pass

# This very simple program will execute sequentially, and will exit if anything goes wrong.
# There are only two main options: 1. Meal entries, or 2. Create new food items for the database

# Directory strings (need to be changed depending on platform)
database_dir = "/data/data/com.termux/files/home/.food/"
log_dir = "/data/data/com.termux/files/home/food_logs/"

# First thing to do is get the database
database = Database(dirpath=database_dir,filename="foods.dat",fieldname="name")

# Strings
start_msg = "\nEnter <q> to exit.\n\n1. Enter new meal\n2. Add a food item to the database\n3. View Catalog\n4. Show Current Log\n5. Estimate calories (for meals too complex to calculate)\n6. Delete meal entry\n7. Remove database item\n: "
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
    elif user_input_1 == 5:
        estimate_calories(log_path)
    elif user_input_1 == 6:
        delete_entry()
    elif user_input_1 == 7:
        remove_database_item(database)
    user_input_1 = get_number(start_msg,int)
    cls()
