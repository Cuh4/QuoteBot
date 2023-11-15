# // ---------------------------------------------------------------------
# // ------- [Quote Bot] Get Random User Quote Slash Command
# // ---------------------------------------------------------------------

# // ---- Imports
import discord
import random

import ui
import quotes as _quotes
from helpers import general as helpers
from helpers import discord as discordHelpers

# // ---- Main
# // create command
def command():
    # // get vars
    # discord-related
    client: discord.Client = helpers.globals.get("client")
    tree: discord.app_commands.CommandTree = helpers.globals.get("commandTree")
    
    # quotes-related
    quotes: _quotes.quotes = helpers.globals.get("quotes")
    
    # // main command
    # slash command
    @tree.command(
        name = "random_user_quote",
        description = "Sends a random quote created by the specified member."
    )
    @discord.app_commands.describe(member = "The member to get a quote from.")
    async def command(interaction: discord.Interaction, member: discord.Member):
        # // get vars
        # get user's quotes
        userQuotes = quotes.getQuotesByUser(member)
        
        # // checks
        # setup
        checks = helpers.misc.failChecks()
        
        # check if the mentioned user is a bot
        if member.bot:
            checks.fail(f"{discordHelpers.utils.mentionUser(member)} is a bot.")
        
        # check if the mentioned user has quotes
        if userQuotes is None:
            checks.fail(f"{discordHelpers.utils.mentionUser(member)} hasn't been quoted before. Tell them to get started by using </quote:1174424282772807761>.")
            
        # failure message if failed
        failed, failureMessage = checks.result()
        
        if failed:
            return await interaction.response.send_message(
                embed = discordHelpers.embeds.failure(failureMessage)
            )
            
        # // main
        # get random quote from user
        chosenQuote = random.choice(userQuotes)
        
        # reply with quote
        quoteView = ui.views.quote(chosenQuote)

        response = await interaction.response.send_message(
            embed = await helpers.events.getSavedEvent("formatQuote").asyncFire(chosenQuote),
            view = quoteView
        )
        
        quoteView.setViewMessage(response)

# // start command
command()