import sqlite3
import random

class numberGame:
    def __init__(self, playerList):
        self.playerList = playerList
        
        self.minNum = None
        self.maxNum = None
        self.ranNum = None

        self.setSettings()
        self.connectToDB()
        self.showHighscore()
        self.guessNumber(int(input(f"Please guess a number, {self.playerList[0].name}: ")))

    def guessNumber(self, guessInt):
        self.playerList[0].guesses += 1
        if guessInt == self.ranNum:
            print(f"Congratulations {playerList[0].name}! Your guess was correct!")

            winner = self.playerList[0]
            self.saveScore(winner)
        elif guessInt < self.ranNum:
            print("Too low!")

            guessInt = int(input(f"Please guess a number, {self.playerList[0].name}: "))
            self.guessNumber(guessInt)
        elif guessInt > self.ranNum:
            print("Too high!")
            
            guessInt = int(input(f"Please guess a number, {self.playerList[0].name}: "))
            self.guessNumber(guessInt)

    def connectToDB(self):
        conn = sqlite3.connect("guessNumber.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS
        numberGame(gameID INTEGER PRIMARY KEY AUTOINCREMENT, 
                    playername TEXT NOT NULL, 
                    guesses INT NOT NULL);""")
        conn.commit()
        conn.close()

    def saveScore(self, winner):
        conn = sqlite3.connect("guessNumber.db")
        c = conn.cursor()
        c.execute("INSERT INTO numberGame (playername, guesses) VALUES (?, ?)", (winner.name, winner.guesses))
        conn.commit()
        conn.close()

        self.showHighscore()        

    def showHighscore(self):
        conn = sqlite3.connect("guessNumber.db")
        c = conn.cursor()
        c.execute("""SELECT playername, guesses FROM numberGame ORDER BY guesses ASC;""")

        print("HIGHSCORE")
        for playername, guesses in c:
            print(f"{playername} | {guesses}")

        conn.commit()
        conn.close()

    def setSettings(self):
        num1 = input("Please enter the first number of the guess-range: ")
        num2 = input("Please enter the second number of the guess-range: ")

        self.minNum = int(min(num1, num2))
        self.maxNum = int(max(num1, num2))

        #Determine random number to guess
        self.ranNum = random.randint(self.minNum, self.maxNum)


class player:
    def __init__(self, name):
        self.name = name
        self.guesses = 0


if __name__ == "__main__":
    playerList = []
    playerList.append(player(input("Please enter your name: ")))

    numberGame(playerList)