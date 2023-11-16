# // ---------------------------------------------------------------------
# // ------- [Quote Bot] Remove Slash Command
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

import quotes as _quotes
from helpers import general as helpers
from helpers import discord as discordHelpers

# // ---- Main
# // create command
def command():
    # // get vars
    # discord related
    client: discord.Client = helpers.globals.get("client")
    tree: discord.app_commands.CommandTree = helpers.globals.get("commandTree")
    
    # quotes related
    quotes: _quotes.quotes = helpers.globals.get("quotes")
    
    # // main command
    # slash command
    @tree.command(
        name = "remove",
        description = "Removes a quote with the specified ID."
    )
    @discord.app_commands.describe(quote_id = "The ID of the quote to remove. The ID can be found at the bottom of a quote message.")
    async def command(interaction: discord.Interaction, quote_id: int):
        # // get vars
        # get quote
        quote = quotes.getQuote(quote_id)
        
        # // checks
        # setup
        checks = helpers.misc.failChecks()
        
        # make sure this isnt being used anywhere but in a text channel
        if interaction.channel.type != discord.ChannelType.text and not discordHelpers.utils.isCreator(client, interaction.user):
            checks.fail("This command must be used in a text channel, not a DM.")
        
        # make sure this user has valid permissions
        if not discordHelpers.utils.hasPermissions(client, interaction.user, ["manage_messages"]):
            checks.fail("You must have `manage_messages` permissions to use this command.")
            
        # make sure the quote exists
        if quote is None:
            checks.fail("No quote with the specified ID was found.")
            
        # make sure the quote belongs to this member's guild
        if quote.getGuildID() != interaction.guild.id and not discordHelpers.utils.isCreator(client, interaction.user):
            checks.fail("The specified quote does not belong to your server.")
        
        # failure message if failed
        failed, failureMessage = checks.result()
        
        if failed:
            return await interaction.response.send_message(
                embed = discordHelpers.embeds.failure(failureMessage)
            )
        
        # // main
        # remove the quote
        quote.remove()
        
        # reply
        await interaction.response.send_message(
            embed = discordHelpers.embeds.success(f"Successfully removed quote #{quote.getID()}.")
        )
        

# // start command
command()