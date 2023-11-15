# // ---------------------------------------------------------------------
# // ------- [Quote Bot] Quotes Classes
# // ---------------------------------------------------------------------

# // Imports
from .quote import quotes

# // ---- Classes
# // Quote
class quote:
    def __init__(self, parent: quotes, id: int, user_id: int, guild_id: int, channel_id: int, message_id: int, quote: str, data: dict, timestamp: float):
        self.__parent = parent
        self.__id = id
        self.__user_id = user_id
        self.__guild_id = guild_id
        self.__channel_id = channel_id
        self.__message_id = message_id
        self.__text = quote
        self.__data = data
        self.__timestamp = timestamp
        
    def getParent(self):
        return self.__parent
        
    def getID(self):
        return self.__id
        
    def getUserID(self):
        return self.__user_id
    
    def getGuildID(self):
        return self.__guild_id
    
    def getChannelID(self):
        return self.__channel_id
    
    def getMessageID(self):
        return self.__message_id

    def getText(self):
        return self.__text
    
    def getData(self):
        return self.__data
    
    def getTimestamp(self):
        return self.__timestamp
    
    def remove(self):
        return self.getParent().removeQuote(self.getID())