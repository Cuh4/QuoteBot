# // ---------------------------------------------------------------------
# // ------- [Quote Bot] Quotes Main
# // ---------------------------------------------------------------------

# // ---- Imports
import time
import os
import json
import sqlite3
import discord
import pathlib

from . import helpers
from . import definitions

# // ---- Classes
class quotes:
    def __init__(self, databaseName: str = "quotes", databasePath: str = "/"):
        # create path if doesnt exist
        pathlib.Path(databasePath).mkdir(parents = True, exist_ok = True)
        
        # properties
        self.databaseName = helpers.pathSafeName(databaseName) + ".db"
        self.databasePath = databasePath
        self.fullPath = os.path.abspath(os.path.join(self.databasePath, self.databaseName))

        # connect to db
        self.database = sqlite3.connect(self.fullPath)
        self.createDatabaseSchema()
        
    # // helpers
    def __getCursor(self):
        return self.database.cursor()
    
    def __commit(self):
        return self.database.commit()
    
    def __quoteDataToQuote(self, data: list):
        return definitions.quote(data[0], data[1], data[2], data[3], json.loads(data[4]), data[5])

    # // methods
    def createDatabaseSchema(self):
        cursor = self.__getCursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS Quotes (
            id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
            user_id INTEGER,
            guild_id INTEGER,
            quote TEXT,
            data TEXT,
            timestamp REAL
        )""") # responses is a json list, data is a json dict
        
        self.__commit()
        
    def getRandomQuote(self):
        cursor = self.__getCursor()
        data = cursor.execute("SELECT * FROM Quotes ORDER BY RANDOM() LIMIT 1").fetchone()
        
        return self.__quoteDataToQuote(data) if data is not None else None
        
    def getQuotesByUser(self, user: discord.User):
        cursor = self.__getCursor()
        allData = cursor.execute("SELECT * FROM Quotes WHERE user_id = ?", [user.id]).fetchall()
        
        return [self.__quoteDataToQuote(data) for data in allData]
    
    def getQuotesByGuild(self, guild: discord.Guild):
        cursor = self.__getCursor()
        allData = cursor.execute("SELECT * FROM Quotes WHERE guild_id = ?", [guild.id]).fetchall()
        
        return [self.__quoteDataToQuote(data) for data in allData]
        
    def getQuote(self, id: int):
        cursor = self.__getCursor()
        data = cursor.execute("SELECT * FROM Quotes WHERE id = ?", [id]).fetchone()
        
        return self.__quoteDataToQuote(data) if data is not None else None
        
    def saveQuote(self, user: discord.User, guild: discord.Guild, quote: str, data: dict):
        cursor = self.__getCursor()
        cursor.execute("INSERT OR IGNORE INTO Quotes VALUES (?, ?, ?, ?, ?)", [user.id, guild.id, quote, json.dumps(data), time.time()])

        self.__commit()

    def removeQuote(self, id: int):
        self.__getCursor().execute("DELETE FROM Quotes WHERE id = ?", [id])
        self.__commit()