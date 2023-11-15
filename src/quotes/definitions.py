# // ---------------------------------------------------------------------
# // ------- [Quote Bot] Quotes Data
# // ---------------------------------------------------------------------

# // ---- Classes
# // Quote
class quote:
    def __init__(self, id: int, user_id: int, guild_id: int, quote: str, data: dict, timestamp: float):
        self.__id = id
        self.__user_id = user_id
        self.__guild_id = guild_id
        self.__text = quote
        self.__data = data
        self.__timestamp = timestamp
        
    def getID(self):
        return self.__id
        
    def getUserID(self):
        return self.__user_id
    
    def getGuildID(self):
        return self.__guild_id

    def getText(self):
        return self.__text
    
    def getData(self):
        return self.__data
    
    def getTimestamp(self):
        return self.__timestamp