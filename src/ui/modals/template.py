# // ---------------------------------------------------------------------
# // ------- [Quote Bot] Template Modal UI
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

import config

# // ---- Main
# // UI
class modal(discord.ui.Modal):
    def setup(self):
        super().__init__(timeout = config.uiModalTimeout)