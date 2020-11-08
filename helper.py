"""
    Name: Clint Galvez
    Date: 8 November 2020
    Assignment: 1405-Z Individual Course Project (Poke-Battler)
    Purpose: Helpful functions
"""
# Create a table
def CreateTable(rows, columns):
    table = []
    for i in range(rows):
        row = []
        for j in range(columns):
            column = None
            row.append(column)
        table.append(row)
    return table

# Split a string by capitals
def SplitCaps(str):
    import re
    return re.findall("[A-Z][^A-Z]*", str)

# Check if the string is a number
def IsNumber(str):
    try:
        # Check if the string can be converted into an integer
        str = int(str)
        return True
    except:
        return False

# Check if the string is a pokemon type
def IsType(str):
    types = {
        "NORMAL": True,
        "FIRE": True,
        "WATER": True,
        "ELECTRIC": True,
        "GRASS": True,
        "ICE": True,
        "FIGHTING": True,
        "POISON": True,
        "GROUND": True,
        "FLYING": True,
        "PSYCHIC": True,
        "BUG": True,
        "ROCK": True,
        "GHOST": True,
        "DRAGON": True,
        "DARK": True,
        "STEEL": True,
        "FAIRY": True,
    }
    return str.upper() in types

# Put the contents of a table into a single string variable to be written into a file
def OutString(table):
    rows = len(table)
    columns = len(table[0])
    outString = ""
    for row in range(rows):
        for column in range(columns):
            outString += str(table[row][column]) + "|"
        outString += "\n"
    return outString

def Types(str):
    types = str
    types = types.strip("[]").replace("'", "").replace(" ", "").split(",")
    return types

def ReadFile(filename):
    table = []
    # Open and read the file
    with open(filename, "r") as fileIn:
        # Loop through the file
        for line in fileIn:
            table.append(line.strip().split("|"))

        # 2 = last modified and spacing
        # 3 = last modified, spacing, and categories
        for line in range(3):
            # Remove date last modified and spacing lines in the file
            table.pop(0)
    # Close the file
    fileIn.close()

    # If the file is Pokemon.txt turn the types string into a list
    if filename == "Pokemon.txt":
        for pokemon in range(len(table)):
            typesIndex = 2
            table[pokemon][typesIndex] = Types(table[pokemon][typesIndex])

    return table

def Clear():
    import os
    os.system("cls")

if __name__ == "__main__":
    print("Main")
    print(SplitCaps("ChinaTownManGuy"))
    print(IsNumber("43"))
    print(IsType("fairy"))
    print(ReadFile("Pokemon.txt"))
    print(Types("['Grass', 'Poison']"))
    print(IsNumber(None))
