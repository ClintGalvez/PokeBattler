# import helper
#
# name = "Clint"
# score = 56
#
# # Leaderboard Section
# filename = "LeaderboardTest.txt"
#
# # Add the player's score into the leaderboard file
# fileOut = open(filename, "a")
# fileOut.write(name + "|" + str(score) + "|\n")
# fileOut.close()
#
# # Read the leaderboard
# fileIn = open(filename, "r")
# contents = fileIn.read()
# fileIn.close()
#
# contents = contents.split("\n")
# rows = len(contents)-1
# columns = 2
# nameIndex = 0
# scoreIndex = 1
# scoreTable = helper.CreateTable(rows, columns)
# for row in range(rows):
#     scoreInfo = contents[row].split("|")
#     scoreTable[row][nameIndex] = scoreInfo[nameIndex]
#     scoreTable[row][scoreIndex] = int(scoreInfo[scoreIndex])
#
# # Sort the leaderboard
# for i in range(rows-1):
#     for j in range(rows-1-i):
#         # Check if the current index is greater than the next one,
#         # if so they switch values
#         if scoreTable[j][scoreIndex] < scoreTable[j+1][scoreIndex]:
#             temp = scoreTable[j]
#             scoreTable[j] = scoreTable[j+1]
#             scoreTable[j+1] = temp
#
# # Display the leaderboard
# print("THANKS FOR PLAYING!")
# print("NAME: " + name)
# print("SCORE: " + str(score))
# print("\nSCOREBOARD:")
# for row in range(rows):
#     print(scoreTable[row][nameIndex] + ": " + str(scoreTable[row][scoreIndex]) + " points")
#
# outputString = helper.OutString(scoreTable)
#
# # Save the leaderboard
# fileOut = open(filename, "w")
# fileOut.write(outputString)
# fileOut.close()

import colorama
from colorama import Fore, Back

colorama.init(autoreset=True)

# Automatically adds a Style.RESET_ALL after each print statement
print(Fore.RED + 'Red foreground text')
print(Back.RED + 'Red background text')
print("Some plain text")