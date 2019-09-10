### This file to contain a set of useful classes for the food entry program

## The Serving class encapsulates serving sizes of food items, used to easily 
# input multiples of servings. The 3 main attributes of a serving are the 3 
# primary macronutrients. In many cases, the Serving object will be a ratio of
# serving size in either grams or some volumetric quantity and the three macronutrients.
# Takes three items in the constructor: carbs, fats, protein
# The description is supposed to illustrate the size of a serving in some useful way (i.e.
# macros per gram or macros per unit)
class Serving:
    def __init__(self, name = "", macros = [], description = ""):
        if len(macros) is not 3:
            raise ValueError("Macros needs to be a list of [carbs,fats,protein] per serving")
        self.name = name
        self.macros = macros
        self.description = description

        self.carbs = macros[0]
        self.fats = macros[1]
        self.protein = macros[2]
    def __repr__(self):
        return self.name + ": (" + str(self.carbs) + " g carbs, " + str(self.fats) + " g fat, " + str(self.protein) + " g protein)"
