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
        
        # // get variables
        # foundation variables
        client: discord.Client = helpers.globals.get("client")

        # quote related variables
        messageExists = False
        channel = client.get_channel(quote.getChannelID())
        
        if channel:
            message = channel.get_partial_message(quote.getMessageID())
            messageExists = message is not None

        # // jump to quote button
        # create button
        self.jumpToQuote = discord.ui.Button(
            label = "Jump To Quote",
            url = message.jump_url if messageExists else None,
            disabled = not messageExists,
            style = discord.ButtonStyle.red # defaults to link style if url is set, but the url is only set if the message exists, hence why this is red and not a success color like green
        )
        
        # add
        self.add_item(self.jumpToQuote)

        # // discord invite button
        # create button
        self.inviteButton = discord.ui.Button(
            label = "Support Server",
            url = "https://discord.gg/2HR2awsdSt",
            emoji = "😎"
        )
        
        # add
        self.add_item(self.inviteButton)