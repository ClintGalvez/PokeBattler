"""
    Name: Clint Galvez
    Date: XX October 2020
    Assignment: 1405-Z Individual Course Project (Poke-Battler)
    Purpose: Scrape websites for specific info
"""
import helper
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def Pokemon(saveToFile = False):
    url = "https://pokemondb.net/pokedex/all"

    try:
        # Request, Read, and Decode the website
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req)
        html = page.read().decode("utf-8")

        # Parse the page (BeautifulSoup object)
        soup = BeautifulSoup(html, "html.parser")

        # Navigate the tree and finds the moves table and the date the website was last modified
        tableInfo = soup.table
        tableHead = tableInfo.thead
        tableBody = tableInfo.tbody

        # Organize the categories found in the table's head
        try:
            categories = tableHead.text.strip().split(" ")
            for i in range(len(categories)):
                if categories[i].upper() == "SP.":
                    categories[i] = categories[i] + " " + categories[i+1]
                    categories.pop(i+1)
        except:
            # In case the for loop goes out of the list's index
            pass

        # Organize the pokemon info found in the table's body
        pokedex = []
        for child in tableBody.children:
            try:
                pokemon = child.text.strip().split("\n")
                pokedex.append(pokemon)
            except:
                pass

        for i in range(len(pokedex)):
            try:
                pokedex[i][0] = pokedex[i][0].replace("\u2640", "") # Remove female sign (?)
                pokedex[i][0] = pokedex[i][0].replace("\u2642", "") # Remove male sign (?)
                pokedex[i][0] = pokedex[i][0].replace(" ", "")

                # Hold the index 0 of the pokemon i in a temporary string variable to be split and reorganized
                string = pokedex[i][0]
                pokedex[i].pop(0)

                # Pokemon number
                numbers = ""
                for num in range(len(string)):
                    if helper.IsNumber(string[num]):
                        numbers += string[num]
                pokedex[i].insert(0, str(int(numbers)))

                # Pokemon name and type(s)
                string = helper.SplitCaps(string)
                name = ""
                types = []
                for j in range(len(string)):
                    if helper.IsType(string[j]):
                        types.append(string[j])
                    else:
                        name += string[j] + " "
                pokedex[i].insert(1, name.strip())
                pokedex[i].insert(2, types)
            except:
                pass

        # Organize the data into a single table
        # Determine the amount of columns
        columns = len(categories)
        # Calculate the amount of rows
        rows = len(pokedex) + 1
        # Create table to hold organized data
        pokedexTable = helper.CreateTable(rows, columns)

        # Organize the data into a table
        for row in range(rows):
            for column in range(columns):
                try:
                    if row == 0:
                        pokedexTable[row][column] = categories[column]
                    else:
                        pokedexTable[row][column] = pokedex[row-1][column]
                except:
                    # In case an attribute has no value
                    pokedexTable[row][column] = "None"

        # Determine where to hold the data
        if saveToFile:
            # Hold the data in a file
            # Save the organized into a string that will be written to a file
            outString = helper.OutString(pokedexTable)

            # Save the data into a file
            filename = "Pokemon.txt"
            fileOut = open(filename, "w")
            fileOut.write("Last modified: UNKOWN" + "\n\n" + outString)
            fileOut.close()
        else:
            # Hold the data in a dictionary
            dict = {}

            # Save the data from the table into the dict
            header = 0
            for pokemon in range(rows):
                for trait in range(columns):
                    if pokemon == header:
                        pass
                        # if movesTable[move][trait].upper() == "NAME":
                        #     _name = trait
                        # elif movesTable[move][trait].upper() == "TYPE":
                        #     _type = trait
                        # elif movesTable[move][trait].upper() == "CATEGORY":
                        #     _category = trait
                        # elif movesTable[move][trait].upper() == "CONTEST":
                        #     _contest = trait
                        # elif movesTable[move][trait].upper() == "PP":
                        #     _quantity = trait
                        # elif movesTable[move][trait].upper() == "POWER":
                        #     _power = trait
                        # elif movesTable[move][trait].upper() == "ACCURACY":
                        #     _accuracy = trait
                        # elif movesTable[move][trait].upper() == "GEN":
                        #     _gen = trait
                    else:
                        pass
                        # # Check if quantity, power and accuracy are given
                        # if helper.IsNumber(movesTable[move][_quantity]):
                        #     quantity = int(movesTable[move][_quantity])
                        # else:
                        #     quantity = None
                        #
                        # if helper.IsNumber(movesTable[move][_power]):
                        #     power = int(movesTable[move][_power])
                        # else:
                        #     power = None
                        #
                        # if helper.IsNumber(movesTable[move][_accuracy].strip("%")):
                        #     accuracy = int(movesTable[move][_accuracy].strip("%"))
                        # else:
                        #     accuracy = None
                        #
                        # # Save the move into the dictionary
                        # dict[movesTable[move][_name]] = {
                        #     "type": movesTable[move][_type],
                        #     "category": movesTable[move][_category],
                        #     "contest": movesTable[move][_contest],
                        #     "quantity": quantity,
                        #     "power": power,
                        #     "accuracy": accuracy,
                        #     "gen": movesTable[move][_gen],
                        # }
            return dict

    except:
        print("ERROR: Unable to scrape the website (" + url + ") for moves!")

def Moves(saveToFile = False):
    url = "https://bulbapedia.bulbagarden.net/wiki/List_of_moves"

    try:
        # Request, Read, and Decode the website
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req)
        html = page.read().decode("utf-8")

        # Parse the page (BeautifulSoup object)
        soup = BeautifulSoup(html, "html.parser")

        # Navigate the tree and finds the moves table and the date the website was last modified
        tableInfo = soup.table.table
        lastMod = soup.find(id="lastmod").string.strip()

        # Collect data from the table
        tableRawList = tableInfo.text.split("\n")
        tableList = []
        for i in range(len(tableRawList)):
            if tableRawList[i] != "":
                tableList.append(tableRawList[i].strip().strip("*"))

        # Create a 2D list to hold the organized data
        # Determine the amount of columns
        columns = 0
        for i in range(len(tableList)):
            if tableList[i] == "1":
                break
            columns += 1
        # Calculate the amount of rows
        rows = int(len(tableList) / columns)
        movesTable = helper.CreateTable(rows, columns)

        # Organize the data into a table
        index = 0
        for row in range(rows):
            for column in range(columns):
                movesTable[row][column] = tableList[index]
                index += 1

        # Determine where to hold the data
        if saveToFile:
            # Hold the data in a file
            # Save the organized into a string that will be written to a file
            outString = helper.OutString(movesTable)

            # Save the data into a file
            filename = "Moves.txt"
            fileOut = open(filename, "w")
            fileOut.write(str(lastMod) + "\n\n" + outString)
            fileOut.close()
        else:
            # Hold the data in a dictionary
            dict = {}

            # Save the data from the table into the dict
            header = 0
            for move in range(rows):
                for trait in range(columns):
                    if move == header:
                        if movesTable[move][trait].upper() == "NAME":
                            _name = trait
                        elif movesTable[move][trait].upper() == "TYPE":
                            _type = trait
                        elif movesTable[move][trait].upper() == "CATEGORY":
                            _category = trait
                        elif movesTable[move][trait].upper() == "CONTEST":
                            _contest = trait
                        elif movesTable[move][trait].upper() == "PP":
                            _quantity = trait
                        elif movesTable[move][trait].upper() == "POWER":
                            _power = trait
                        elif movesTable[move][trait].upper() == "ACCURACY":
                            _accuracy = trait
                        elif movesTable[move][trait].upper() == "GEN":
                            _gen = trait
                    else:
                        # Check if quantity, power and accuracy are given
                        if helper.IsNumber(movesTable[move][_quantity]):
                            quantity = int(movesTable[move][_quantity])
                        else:
                            quantity = None

                        if helper.IsNumber(movesTable[move][_power]):
                            power = int(movesTable[move][_power])
                        else:
                            power = None

                        if helper.IsNumber(movesTable[move][_accuracy].strip("%")):
                            accuracy = int(movesTable[move][_accuracy].strip("%"))
                        else:
                            accuracy = None

                        # Save the move into the dictionary
                        dict[movesTable[move][_name]] = {
                            "type": movesTable[move][_type],
                            "category": movesTable[move][_category],
                            "contest": movesTable[move][_contest],
                            "quantity": quantity,
                            "power": power,
                            "accuracy": accuracy,
                            "gen": movesTable[move][_gen],
                        }
            return dict

    except:
        print("ERROR: Unable to scrape the website (" + url + ") for moves!")

def Types(saveToFile = False):
    url = "https://pokemondb.net/type"

    try:
        # Request, Read, and Decode the website
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req)
        html = page.read().decode("utf-8")

        # Parse the page (BeautifulSoup object)
        soup = BeautifulSoup(html, "html.parser")

        # Navigate the tree

        # Collect the data

        # Organize the data

        # Determine where to hold the data
        if saveToFile:
            # Hold the data in a file
            # Save the organized into a string that will be written to a file
            # outString = helper.OutString(movesTable)

            # Save the data into a file
            filename = "Types.txt"
            fileOut = open(filename, "w")
            # fileOut.write("Last modified: UNKOWN" + "\n\n" + outString)
            fileOut.close()
        else:
            # Hold the data in a dictionary
            dict = {}

            # Save the data from the table into the dict
            header = 0

            return dict

    except:
        print("ERROR: Unable to scrape the website (" + url + ") for moves!")

def Sprites(saveToFile = False):
    url = "https://pokemondb.net/sprites"

    try:
        # Request, Read, and Decode the website
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req)
        html = page.read().decode("utf-8")

        # Parse the page (BeautifulSoup object)
        soup = BeautifulSoup(html, "html.parser")

        # Navigate the tree

        # Collect the data

        # Organize the data

        # Determine where to hold the data
        if saveToFile:
            pass
        else:
            # Hold the data in a dictionary
            dict = {}

            # Save the data from the table into the dict
            header = 0

            return dict

    except:
        print("ERROR: Unable to scrape the website (" + url + ") for moves!")

if __name__ == "__main__":
    Pokemon(True)
    Moves(True)
    Sprites(True)
    Types(True)
    print("MAIN: DONE")