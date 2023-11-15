# // ---------------------------------------------------------------------
# // ------- [Quote Bot] Template Modal UI
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

import config

# // ---- Main
# // UI
class modal(discord.ui.Modal):
    message: discord.Message = None
    
    def setup(self):
        super().__init__(timeout = config.uiModalTimeout)
        
    def setViewMessage(self, message: discord.Message):
        self.message = message