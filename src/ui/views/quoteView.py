# // ---------------------------------------------------------------------
# // ------- [Quote Bot] Quote View UI
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

import ui
import quotes
from ui.views import template
from helpers import general as helpers
from helpers import discord as discordHelpers

# // ---- Main
# // UI
class view(template):
    # // Main UI
    def __init__(self, quote: quotes.definitions.quote):
        # // setup
        # setup template
        super().setup()
        
        # get vars
        client: discord.Client = helpers.globals.get("client")
        message: discord.PartialMessageable = client.get_partial_messageable(quote.getMessageID(), guild_id = quote.getGuildID())
        
        # // jump to message button
        # create button
        self.jumpToMessage = discord.ui.Button(
            style = discord.ButtonStyle.blurple,
            label = "Jump To Quote",
            url = message.jump_url if message else "",
            disabled = message is None
        )
        
        # add
        self.add_item(self.jumpToMessage)

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