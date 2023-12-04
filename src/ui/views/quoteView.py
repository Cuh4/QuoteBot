# // ---------------------------------------------------------------------
# // ------- [Quote Bot] Quote View UI
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

import ui
import quotes
import config
from ui.views import template
from helpers import general as helpers
from helpers import discord as discordHelpers

# // ---- Main
# // UI
class view(template):
    # // Main UI
    def __init__(self, quote: quotes.classes.quote):
        # // setup
        # setup template
        super().setup()
        
        # // get variables
        # foundation variables
        self.client: discord.Client = helpers.globals.get("client")

        # quote related variables
        self.quote = quote
        
        messageExists = False
        channel = self.client.get_channel(quote.getChannelID())
        
        if channel:
            message = channel.get_partial_message(quote.getMessageID())
            messageExists = message is not None
            
        # // report button
        # create button
        self.reportButton = discord.ui.Button(
            label = "Report Quote",
            style = discord.ButtonStyle.danger,
            emoji = "🤬"
        )
        
        # button callback
        self.reportButton.callback = self.reportButtonCallback
        
        # add
        self.add_item(self.reportButton)

        # // jump to quote button
        # create button
        self.jumpToQuote = discord.ui.Button(
            label = "Jump To Quote" if messageExists else "[Original Message Removed]",
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

    # // Button Callbacks
    async def reportButtonCallback(self, interaction: discord.Interaction):
        # get report channel
        reportChannel = self.client.get_channel(config.reportChannelID) or await self.client.fetch_channel(config.reportChannelID)
        
        if reportChannel is None:
            return await interaction.response.send_message(
                embed = discordHelpers.embeds.failure("Sorry, but your report failed to send. Please try again later."),
                ephemeral = True
            )
            
        # format report details
        content = "\n".join([
            "**Quote Creator ID**",
            f"`{self.quote.getUserID()}`\n",
            "**Quote ID**",
            f"`{self.quote.getID()}`\n",
            "**Quote Content**",
            f"```{discordHelpers.utils.stripHighlightMarkdown(self.quote.getText())}```\n",
            "**Quote Creation Time**",
            f"{discordHelpers.utils.formatTimestamp(self.quote.getTimestamp())}"
        ])
        
        # disable button
        self.reportButton.disabled = True

        await self.message.edit(
            view = self
        )
        
        # send report
        await reportChannel.send(
            embed = discordHelpers.embeds.info(
                f"**A quote was reported by @{interaction.user.name} `({interaction.user.id})`.**\n---\n{content}"
            )
        )
        
        # send success message
        await interaction.response.send_message(
            embed = discordHelpers.embeds.success("This quote has been successfully reported."),
            ephemeral = True
        )