import time
import numpy as np
import sys

def DelayPrint(stringValue):
    # Print 1 character at a time
    for char in stringValue:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)
    return

class Pokemon:
    def __init__(self, name, types, moves, EVs, health="==================="):
        # Save variables as attributes
        self.name = name
        self.types = types
        self.moves = moves
        self.attack = EVs["ATTACK"]
        self.defense = EVs["DEFENSE"]
        self.health = health
        self.bars = 20 # Amount of health bars

    def fight(self, enemy):
        # Allow 2 pokemon to fight each other

        # Print fight information
        print("-----POKEMON BATTLE-----")
        print(f"\n{self.name}")
        print("TYPE/", self.types)
        print("ATTACK/", self.attack)
        print("DEFENSE/", self.defense)
        print("LVL/", 3*(1+np.mean([self.attack,self.defense])))

        print("\nVS")

        print(f"\n{enemy.name}")
        print("TYPE/", enemy.types)
        print("ATTACK/", enemy.attack)
        print("DEFENSE/", enemy.defense)
        print("LVL/", 3*(1+np.mean([enemy.attack,enemy.defense])))

        time.sleep(2)

        # Consider type advantages
        version = ["Fire", "Water", "Grass"]
        for i,k in enumerate(version):
            if self.types == k:
                # Both pokemon are the same type
                if enemy.types == k:
                    string_self_attack = "\nIts not very effective..."
                    string_enemy_attack = "\nIts not very effective..."

                # Enemy is STRONG
                if enemy.types == version[(i+1)%3]:
                    self.attack *= 0.5
                    self.defense *= 0.5
                    enemy.attack *= 2
                    enemy.defense *= 2
                    string_self_attack = "\nIts not very effective..."
                    string_enemy_attack = "\nIts super effective..."

                # Enemy is WEAK
                if enemy.types == version[(i+2)%3]:
                    self.attack *= 2
                    self.defense *= 2
                    enemy.attack *= 0.5
                    enemy.defense *= 0.5
                    string_self_attack = "\nIts super effective..."
                    string_enemy_attack = "\nIts not very effective..."

        # Now for the actual fighting...
        # Continue while pokemon still have health
        while self.bars > 0 and enemy.bars > 0:
            # Print the health of each pokemon
            print(f"\n{self.name}\t\tHLTH\t{self.health}")
            print(f"{enemy.name}\t\tHLTH\t{enemy.health}\n")

            # Player's turn
            self.Turn(enemy, string_self_attack, True)

            if enemy.bars <= 0:
                break

            # Enemy's turn
            enemy.Turn(self, string_enemy_attack, False)

        money = np.random.choice(5000)
        if self.bars > 0:
            DelayPrint(f"\nOpponent paid you ${money}.")
        else:
            DelayPrint(f"\nYou lost ${money}.")

    def Turn(self, enemy, string_attack, player):
        if player:
            print(f"Go {self.name}!")
            for i,x in enumerate(self.moves):
                print(f"{i+1}.", x)
            index = int(input("Pick a move: "))
            DelayPrint(f"\n{self.name} used {self.moves[index-1]}!")
            time.sleep(1)
            DelayPrint(string_attack)
        else:
            index = np.random.choice(len(self.moves))
            DelayPrint(f"{self.name} used {self.moves[index-1]}!")
            time.sleep(1)
            DelayPrint(string_attack)

        # Determine Damage
        enemy.bars -= self.attack
        enemy.health = ""

        # Add back bars plus defense boost
        for j in range(int(enemy.bars+0.1*enemy.defense)):
            enemy.health += "="

        time.sleep(1)
        print(f"\n{self.name}\t\tHLTH\t{self.health}")
        print(f"{enemy.name}\t\tHLTH\t{enemy.health}\n")
        time.sleep(0.5)

        # Check to see if the enemy has fainted
        if enemy.bars <= 0:
            DelayPrint("\n..." + enemy.name + " fainted.")

if __name__ == "__main__":
    # Create pokemon
    charizard = Pokemon("Charizard", "Fire", ["Flamethrower", "Fly", "Blast Burn", "Fire Punch"], {"ATTACK": 12, "DEFENSE": 8})
    blastoise = Pokemon("Blastoise", "Water", ["Water Gun", "Bubblebeam", "Hydro Pump", "Surf"], {"ATTACK": 10, "DEFENSE": 10})
    venusaur = Pokemon("Venusaur", "Grass", ["Vine Whip", "Razor Leaf", "Earthquake", "Frenzy Plant"], {"ATTACK": 8, "DEFENSE": 12})

    charizard.fight(blastoise)