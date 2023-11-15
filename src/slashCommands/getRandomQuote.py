# // ---------------------------------------------------------------------
# // ------- [Quote Bot] Get Random Quote Slash Command
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

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
        name = "random_quote",
        description = "Sends a random quote created by a random person."
    )
    async def command(interaction: discord.Interaction):
        # // get vars
        # get random quote
        quote = quotes.getRandomQuote()
        
        # // checks
        # setup
        checks = helpers.misc.failChecks()
        
        # quick check
        if quote is None:
            checks.fail("No quotes have been made. Get started by using </quote:1174424282772807761>.")
            
        # failure message if failed
        failed, failureMessage = checks.result()
        
        if failed:
            return await interaction.response.send_message(
                embed = discordHelpers.embeds.failure(failureMessage)
            )
            
        # // main
        # reply with quote
        quoteView = ui.views.quote(quote)

        response = await interaction.response.send_message(
            embed = await helpers.events.getSavedEvent("formatQuote").asyncFire(quote),
            view = quoteView
        )
        
        quoteView.setViewMessage(response)

# // start command
command()