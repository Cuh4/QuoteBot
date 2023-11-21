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
from . import classes

# // ---- Classes
class quotes:
    def __init__(self, databaseName: str = "quotes", databasePath: str = ""):
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
    
    def __searchReady(self, text: str):
        return text.lower().replace(" ", "")
    
    def __quoteDataToQuote(self, data: list):
        return classes.quote(self, data[0], data[1], data[2], data[3], data[4], data[5], data[6], json.loads(data[7]), data[8])

    # // methods
    def createDatabaseSchema(self):
        cursor = self.__getCursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS Quotes (
            id INTEGER PRIMARY KEY NOT NULL,
            creator_user_id INTEGER,
            user_id INTEGER,
            guild_id INTEGER,
            channel_id INTEGER,
            message_id INTEGER,
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
    
    def getAllQuotes(self):
        cursor = self.__getCursor()
        allData = cursor.execute("SELECT * FROM Quotes").fetchall()
        
        return [self.__quoteDataToQuote(data) for data in allData]
    
    def getQuoteByContentSearch(self, query: str):
        query = self.__searchReady(query)
        allQuotes = self.getAllQuotes()
        
        for quote in allQuotes:
            if self.__searchReady(quote.getText()).find(query):
                return quote
        
    def saveQuote(self, creator: discord.User, user: discord.User, guild: discord.Guild, message: discord.Message, data: dict):
        cursor = self.__getCursor()
        cursor.execute("INSERT OR IGNORE INTO Quotes (creator_user_id, user_id, guild_id, channel_id, message_id, quote, data, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", [creator.id, user.id, guild.id, message.channel.id, message.id, message.content[:5000], json.dumps(data), time.time()])

        self.__commit()

    def removeQuote(self, id: int):
        self.__getCursor().execute("DELETE FROM Quotes WHERE id = ?", [id])
        self.__commit()