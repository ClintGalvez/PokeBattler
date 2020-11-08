"""
    Name: Clint Galvez
    Date: 8 November 2020
    Assignment: 1405-Z Individual Course Project (Poke-Battler)
    Purpose: Arcade Pokemon Battle game where each win is worth a point
"""
# import pygame

# File
import constant
import helper

# Library
import numpy as np
import os
import random
import sys
import time

def DelayPrint(stringValue, newLine = True):
    if newLine:
        stringValue += "\n"

    # Print 1 character at a time
    for char in stringValue:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)
    return None

class Pokemon:
    def __init__(self, pokemon):
        # Assign stats approximate to the ones found in the pokedex
        self.name = pokemon
        self.types = constant.pokedex[pokemon]["types"]
        self.total = constant.pokedex[pokemon]["total"]
        self.maxHealth = constant.pokedex[pokemon]["health"]
        self.health = constant.pokedex[pokemon]["health"]
        self.attack = constant.pokedex[pokemon]["attack"]
        self.defense = constant.pokedex[pokemon]["defense"]
        self.specialAttack = constant.pokedex[pokemon]["specialAttack"]
        self.specialDefense = constant.pokedex[pokemon]["specialDefense"]
        self.speed = constant.pokedex[pokemon]["speed"]
        self.bars = 20 # Amount of health bars
        self.level = 1

        # Assign random moves appropriate to the pokemon's type(s)
        self.moves = []

        for i in range(constant.moveQuantity):
            randomMove = random.choice(list(constant.moves.keys()))
            while constant.moves[randomMove]["type"] not in self.types:
                randomMove = random.choice(list(constant.moves.keys()))
            self.moves.append({"name": constant.moves[randomMove]["name"],
                               "type": constant.moves[randomMove]["type"],
                               "category": constant.moves[randomMove]["category"],
                               "contest": constant.moves[randomMove]["contest"],
                               "maxQuantity": constant.moves[randomMove]["quantity"],
                               "quantity": constant.moves[randomMove]["quantity"],
                               "power": constant.moves[randomMove]["power"],
                               "accuracy": constant.moves[randomMove]["accuracy"],
                               "gen": constant.moves[randomMove]["gen"]
                               })

    def Attack(self, enemy, bot=False):
        if bot:
            # Generate random move to attack with
            moveIndex = random.randint(0, constant.moveQuantity-1)

            # Ensure the move can still be used
            while self.moves[moveIndex]["quantity"] <= 0:
                # Generate another random move to attack with
                moveIndex = random.randint(0, constant.moveQuantity-1)

            # Update the amount of times the move can be used
            self.moves[moveIndex]["quantity"] -= 1

            # Ensure the move quantity can never be less than 0
            if self.moves[moveIndex]["quantity"] <= 0:
                self.moves[moveIndex]["quantity"] = 0

            # Calculate the amount of damage done and reduce the enemy's health by that much
            damage = int(CalculateDamage(self, enemy, moveIndex, Modifier(enemy)))
            enemy.health -= damage

            # Display attack info
            print("\n" + self.name + " used " + self.moves[moveIndex]["name"])
            time.sleep(2)
            print(enemy.name + " lost " + str(damage) + " hp!\n")

            # Ensure enemy health never goes below 0
            if enemy.health <= 0:
                enemy.health = 0
        else:
            # Have the player choose the move
            print("\nChoose a move:")

            validMoveIndex = False

            # Ensure the move is valid
            while not validMoveIndex:
                # Display possible moves
                for i in range(len(self.moves)):
                    print(str(i+1) + ". " + self.moves[i]["name"] + ": PP = " + str(self.moves[i]["quantity"]) + " Type = " + self.moves[i]["type"])
                moveIndex = input("\nEnter a move: ")

                # Ensure the input is an integer
                if helper.IsNumber(moveIndex):
                    # Process the move index to allow it access the appropriate move in the moves list
                    moveIndex = int(moveIndex) - 1

                    # Ensure the integer is between 1 and the number of moves (inclusive)
                    if moveIndex >= 0 and moveIndex < constant.moveQuantity:
                        # Ensure the move can still be used
                        if self.moves[moveIndex]["quantity"] > 0:
                            validMoveIndex = True
                        else:
                            print("\nERROR: Invalid move!")
                    else:
                        print("\nERROR: Invalid move!")
                else:
                    print("\nERROR: Invalid move!")

            # Update the amount of times the move can be used
            self.moves[moveIndex]["quantity"] -= 1

            # Ensure the move quantity can never be less than 0
            if self.moves[moveIndex]["quantity"] <= 0:
                self.moves[moveIndex]["quantity"] = 0

            # Calculate the amount of damage done and reduce the enemy's health by that much
            damage = int(CalculateDamage(self, enemy, moveIndex, Modifier(enemy)))
            enemy.health -= damage

            # Display attack info
            print("\n" + self.name + " used " + self.moves[moveIndex]["name"])
            time.sleep(2)
            print(enemy.name + " lost " + str(damage) + " hp!\n")

            # Ensure enemy health never goes below 0
            if enemy.health <= 0:
                enemy.health = 0


class Trainer:
    def __init__(self, name="Clint", bot=False):
        self.name = name
        self.score = 0
        self.team = GenerateTeam()
        self.battler = self.team[0]
        self.availablePokemon = constant.teamSize
        self.items = {}
        self.canBattle = True

        if bot:
            self.bot = True
        else:
            self.bot = False

    def GenerateNewTeam(self):
        self.team = GenerateTeam()
        self.battler = self.team[0]
        self.availablePokemon = constant.teamSize
        self.items = {}
        self.canBattle = True

    def RecoverTeam(self):
        for pokemon in range(constant.teamSize):
            self.team[pokemon].health = self.team[pokemon].maxHealth
            for move in range(constant.moveQuantity):
                self.team[pokemon].moves[move]["quantity"] = self.team[pokemon].moves[move]["maxQuantity"]

    def DisplayTeam(self):
        for i in range(constant.teamSize):
            print(str(i+1) + ". " + self.team[i].name)
            line = "---"
            for char in self.team[i].name:
                line += "-"
            print(line)
            print("TYPE: " + str(self.team[i].types))
            print("HEALTH: " + str(self.team[i].health) + "/" + str(self.battler.maxHealth))
            print("ATTACK: " + str(self.team[i].attack))
            print("DEFENSE: " + str(self.team[i].defense))
            print("SP. ATK: " + str(self.team[i].specialAttack))
            print("SP. DEF: " + str(self.team[i].specialDefense))
            print("SPEED: " + str(self.team[i].speed) + "\n")

    def Displaybattler(self):
        print(str(self.battler.name))
        print("HEALTH: " + str(self.battler.health) + "/" + str(self.battler.maxHealth))
        print("TYPE: " + str(self.battler.types))
        print("ATTACK: " + str(self.battler.attack))
        print("DEFENSE: " + str(self.battler.defense))
        print("SPEED:" + str(self.battler.speed))
        print("LVL: " + str(self.battler.level))

    def Pokemon(self, bot=False):
        helper.Clear()

        if bot:
            # Generate random pokemon index
            pokemonIndex = random.randint(1, constant.teamSize-1)

            # Ensure that the pokemon can be swapped out to battle
            while self.team[pokemonIndex].health <= 0:
                # Generate another random pokemon index
                pokemonIndex = random.randint(1, constant.teamSize-1)

            # Swap the pokemon
            temp = self.battler
            self.battler = self.team[pokemonIndex]
            self.team[pokemonIndex] = temp

            # Announce swap
            print("\n" + self.team[pokemonIndex].name + " has been swapped out with " + self.battler.name + "!")
            time.sleep(3)
        else:
            # Display team
            print("YOUR POKEMON:")
            self.DisplayTeam()

            validPokemonIndex = False

            # Ensure that the pokemon can be swapped out to battle
            while not validPokemonIndex:
                pokemonIndex = input("Enter the number of the pokemon you want to swap out to battle: ")

                # Ensure the input is an integer
                if helper.IsNumber(pokemonIndex):
                    # Process the pokemon index to allow it access the appropriate pokemon in the team list
                    pokemonIndex = int(pokemonIndex) - 1

                    # Ensure the integer is between 1 and the number of pokemon in a team (inclusive)
                    if pokemonIndex > 0 and pokemonIndex < constant.teamSize:
                        # Ensure the pokemon can still battle
                        if self.team[pokemonIndex].health > 0:
                            validPokemonIndex = True
                        else:
                            print("\nERROR: Invalid pokemon!")
                    else:
                        print("\nERROR: Invalid pokemon!")
                else:
                    print("\nERROR: Invalid pokemon!")

            # Swap the pokemon
            temp = self.battler
            self.battler = self.team[pokemonIndex]
            self.team[pokemonIndex] = temp

            # Announce swap
            print("\n" + self.team[pokemonIndex].name + " has been swapped out with " + self.battler.name + "!\n")
            time.sleep(3)

    def Bag(self, bot=False):
        print("Sorry this function is a DLC.\nTo get the DLC follow the steps in this youtube video: https://www.youtube.com/watch?v=ub82Xb1C8os\n")
        time.sleep(3)

    def Trade(self, enemy):
        # Display your team
        print("YOUR POKEMON:")
        self.DisplayTeam()

        # Display the enemy's team
        print("\n\nENEMY POKEMON:")
        enemy.DisplayTeam()

        validEnemyPokemonIndex = False

        # Ensure that the pokemon can be swapped out to battle
        while not validEnemyPokemonIndex:
            enemyPokemonIndex = input("Enter the number of the pokemon from the enemy that you want: ")

            # Ensure the input is an integer
            if helper.IsNumber(enemyPokemonIndex):
                # Process the pokemon index to allow it access the appropriate pokemon in the team list
                enemyPokemonIndex = int(enemyPokemonIndex) - 1

                # Ensure the integer is between 1 and the number of pokemon in a team (inclusive)
                if enemyPokemonIndex > 0 and enemyPokemonIndex < constant.teamSize:
                    validEnemyPokemonIndex = True
                else:
                    print("\nERROR: Invalid pokemon!")
            else:
                print("\nERROR: Invalid pokemon!")

        temp = enemy.team[enemyPokemonIndex]

        validSelfPokemonIndex = False

        # Ensure that the pokemon can be swapped out to battle
        while not validSelfPokemonIndex:
            selfPokemonIndex = input("Enter the number of the pokemon from your lineup you want to trade off: ")

            # Ensure the input is an integer
            if helper.IsNumber(selfPokemonIndex):
                # Process the pokemon index to allow it access the appropriate pokemon in the team list
                selfPokemonIndex = int(selfPokemonIndex) - 1

                # Ensure the integer is between 1 and the number of pokemon in a team (inclusive)
                if selfPokemonIndex > 0 and selfPokemonIndex < constant.teamSize:
                    validSelfPokemonIndex = True
                else:
                    print("\nERROR: Invalid pokemon!")
            else:
                print("\nERROR: Invalid pokemon!")

        # Trade the pokemon
        enemy.team[enemyPokemonIndex] = self.team[selfPokemonIndex]
        self.team[selfPokemonIndex] = temp

        # Announce trade
        print("\n" + self.team[selfPokemonIndex].name + " has been successfully traded for " + enemy.team[enemyPokemonIndex].name + "!\n")
        time.sleep(3)


def GenerateTeam():
    team = []
    for i in range(constant.teamSize):
        randomPokemon = random.choice(list(constant.pokedex.keys()))
        while constant.pokedex[randomPokemon]["total"] == None:
            randomPokemon = random.choice(list(constant.pokedex.keys()))
        team.append(Pokemon(randomPokemon))
        # print(team[i].name + ":\n" + str(team[i].moves))
    return team

def CalculateDamage(self, enemy, moveIndex, modifier):
    level = self.level
    power = self.moves[moveIndex]["power"]
    attack = self.attack
    defense = enemy.defense

    damage = ((((2 * level) / 5 + 2) * power * (attack / defense)) * 0.5 + 2) * modifier
    return damage

def Modifier(pokemon):
    modifier = 1
    return modifier

if __name__ == "__main__":
    playerTeam = []
    enemyTeam = []
    quitGame = False
    gameOver = False

    name = input("Enter your name: ")

    # Generate the player's team
    player = Trainer(name)

    # Generate the enemy's team
    enemy = Trainer("Clint", True)

    # # Display the player's team
    # print("=====PLAYER TEAM=====")
    # player.DisplayTeam()
    #
    # print("Please wait as we find an opponent for you.\nAs we do, feel free to go over your team.")
    # time.sleep(10)
    #
    # print("\n\nAn opponent has been selected for you.")
    # time.sleep(2)
    #
    # print("May your battle be glorious! Now onward you go!")
    # time.sleep(2)

    while not quitGame:
        while not gameOver:
            helper.Clear()

            # Print Attack information
            print("-----POKEMON BATTLE-----")
            player.Displaybattler()
            print("\nVS\n")
            enemy.Displaybattler()

            # Display possible options
            option = input("\nChoose an option:\n1. Attack\n2. BAG\n3. POKEMON\n4. RUN\n\nEnter an option: ")

            possibleOptions = {"1": True, "2": True, "3": True, "4": True}

            # Ensure option is valid
            while option not in possibleOptions:
                option = input("\nERROR: Invalid option!\nChoose an option:\n1. Attack\n2. BAG\n3. POKEMON\n4. RUN\n\nEnter an option: ")

            # Attack
            if option == "1":
                # Determine who attacks first based on which pokemon has a greater speed
                if player.battler.speed >= enemy.battler.speed:
                    player.battler.Attack(enemy.battler)
                    # Ensure that the pokemon can still fight
                    if enemy.battler.health > 0:
                        enemy.battler.Attack(player.battler, True)
                else:
                    enemy.battler.Attack(player.battler, True)
                    # Ensure that the pokemon can still fight
                    if player.battler.health > 0:
                        player.battler.Attack(enemy.battler)
            # Bag
            elif option == "2":
                # Go through the player's bag
                player.Bag()

                # Counts as a move, meaning that the enemy gets to launch an attack
                enemy.battler.Attack(player.battler, True)
            # Pokemon
            elif option == "3":
                player.Pokemon()

                # Counts as a move, meaning that the enemy gets to launch an attack
                enemy.battler.Attack(player.battler, True)
            # Run
            else:
                # Running means quitting the battle and ending the game
                break

            time.sleep(4)

            # Check if both pokemon can continue to battle
            if player.battler.health <= 0:
                # Increase the enemy's battler's level
                enemy.battler.level += 0.5

                # Update the number of pokemon available to battle
                player.availablePokemon -= 1

                # Update whether or not the player can still battle
                if player.availablePokemon <= 0:
                    player.canBattle = False

                time.sleep(2)

                print(player.battler.name + " has fainted...")
                if player.canBattle:
                    print("Please choose another pokemon to battle.")
                    time.sleep(2)
                    player.Pokemon()
                else:
                    gameOver = True

            elif enemy.battler.health <= 0:
                # Increase the player's battler's level
                player.battler.level += 0.5

                print(enemy.battler.name + " has fainted...")

                # Update the number of pokemon available to battle
                enemy.availablePokemon -= 1

                # Update whether or not the enemy can still battle
                if enemy.availablePokemon <= 0:
                    enemy.canBattle = False

                time.sleep(2)

                # Swap to the next pokemon if the enemy can still battle
                if enemy.canBattle:
                    enemy.Pokemon(True)
                else:
                    # Player has won
                    print("\nCongratulations! You have won the battle")

                    # Rewards
                    player.score += 1
                    # give player items
                    # increase overall team level

                    # Ask if the player wants to continue battling
                    continueBattling = input("Do you wish to continue battling?\nEnter \"Y\" to continue: ")

                    if continueBattling.upper() == "Y":
                        # Check if the player wants to swap one of their pokemon with the opponent's
                        trade = input("\nDo you want to swap one of your pokemon with your opponent's?\nEnter \"Y\" to trade: ")
                        if trade.upper() == "Y":
                            # Trade pokemon with the enemy
                            player.Trade(enemy)

                        # Fully heal the player's team
                        player.RecoverTeam()

                        # Generate a new team to battle
                        enemy.GenerateNewTeam()
                    else:
                        gameOver = True

        helper.Clear()
        print("=====GAME OVER!=====")
        time.sleep(1)
        playAgain = input("\nDo you wish to wish to play again?\nEnter \"Y\" to play again: ")
        if playAgain.upper() == "Y":
            gameOver = False
        else:
            quitGame = True

    # Leaderboard Section
    filename = "Leaderboard.txt"
    nameIndex = 0
    scoreIndex = 1

    # Add the player's score into the leaderboard file
    fileOut = open(filename, "a")
    fileOut.write(name + "|" + str(player.score) + "|\n")
    fileOut.close()

    # Read the leaderboard
    fileIn = open(filename, "r")
    contents = fileIn.read()
    fileIn.close()

    # Organize the scores into a table
    contents = contents.split("\n")
    rows = len(contents)-1
    scoreTable = helper.CreateTable(rows, 2)
    for row in range(rows):
        scoreInfo = contents[row].split("|")
        scoreTable[row][nameIndex] = scoreInfo[nameIndex]
        scoreTable[row][scoreIndex] = int(scoreInfo[scoreIndex])

    # Sort the scores
    for i in range(rows-1):
        for j in range(rows-1-i):
            # Check if the current index is greater than the next one,
            # if so they switch values
            if scoreTable[j][scoreIndex] < scoreTable[j+1][scoreIndex]:
                temp = scoreTable[j]
                scoreTable[j] = scoreTable[j+1]
                scoreTable[j+1] = temp

    # Display the leaderboard
    helper.Clear()
    print("THANKS FOR PLAYING!")
    print("NAME: " + player.name)
    print("SCORE: " + str(player.score))
    print("\nSCOREBOARD:")
    for row in range(rows):
        print(scoreTable[row][nameIndex] + ": " + str(scoreTable[row][scoreIndex]) + " points")

    # Save the leaderboard
    outputString = helper.OutString(scoreTable)
    fileOut = open(filename, "w")
    fileOut.write(outputString)
    fileOut.close()
