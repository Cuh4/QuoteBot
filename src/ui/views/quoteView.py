# // ---------------------------------------------------------------------
# // ------- [Quote Bot] Quote View UI
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

import ui
from ui.views import template

# // ---- Main
# // UI
class view(template):
    # // Main UI
    def __init__(self):
        # // setup
        super().setup()

        # // discord invite button
        # create button
        self.inviteButton = discord.ui.Button(
            style = discord.ButtonStyle.link,
            label = "Support Server",
            url = "https://discord.gg/2HR2awsdSt",
            emoji = "😎"
        )
        
        # add
        self.add_item(self.inviteButton)