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
        messageExists = client.get_partial_messageable(quote.getMessageID(), guild_id = quote.getGuildID()) is not None
        
        # // jump to quote button
        # create button
        self.jumpToQuote = discord.ui.Button(
            style = discord.ButtonStyle.blurple,
            label = "Jump To Quote",
            url = f"https://discord.com/channels/{quote.getGuildID()}/{quote.getChannelID()}/{quote.getMessageID()}" if messageExists else "", # partial messagable jump_url is incorrect as it misses the channel id or something, hence why we are doing it here manually
            disabled = messageExists
        )
        
        # add
        self.add_item(self.jumpToQuote)

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