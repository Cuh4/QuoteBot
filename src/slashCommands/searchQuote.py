# // ---------------------------------------------------------------------
# // ------- [Quote Bot] Search Quote Slash Command
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
        name = "search_quote",
        description = "Search for a quote."
    )
    @discord.app_commands.describe(query = "The content to find in a quote.")
    async def command(interaction: discord.Interaction, query: str):
        # // get vars
        # search for quote
        quote = quotes.getQuoteByContentSearch(query, 0.7)
        
        # // checks
        # setup
        checks = helpers.misc.failChecks()
        
        # check if a quote was found
        if quote is None:
            checks.fail("A quote matching your query was not found.")
            
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
            embed = await ui.embeds.quote(quote),
            view = quoteView
        )
        
        quoteView.setViewMessage(response)

# // start command
command()