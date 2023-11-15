# // ---------------------------------------------------------------------
# // ------- [Quote Bot] Quote Slash Command
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

import config
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
    recentMessageFromUsers: dict[int, discord.Message] = helpers.globals.get("recentMessageFromUsers")
    quotes: _quotes.quotes = helpers.globals.get("quotes")
    
    # misc
    startupTime = helpers.globals.get("startupTimestamp")
    
    # // main command
    # slash command
    @tree.command(
        name = "quote",
        description = "Saves the most recent message from the specified member as a quote."
    )
    @discord.app_commands.describe(member = "The member to quote.")
    async def command(interaction: discord.Interaction, member: discord.Member):
        # // checks
        # setup
        checks = helpers.misc.failChecks()
        
        # quick check
        if member.bot:
            checks.fail(f"{discordHelpers.utils.mentionMember()} is a bot.")
        
        # find message
        message = recentMessageFromUsers.get(member.id, None)
        
        if message is None:
            checks.fail(f"{discordHelpers.utils.mentionMember()} hasn't sent a message since I was started {discordHelpers.utils.formatTimestamp(startupTime, 'R')}.")
            
        # failure message if failed
        failed, failureMessage = checks.result()
        
        if failed:
            return interaction.response.send_message(
                embed = discordHelpers.embeds.failure(failureMessage)
            )
            
        # // main
        # save as a quote
        quotes.saveQuote(member, member.guild, message.content[:6000], {}) # trim the quote to prevent people from somehow saving stuff that is wayyyy over the discord message character limit 
        
        # notify
        helpers.prettyprint.success(f"{discordHelpers.utils.formattedName(member)} saved a quote.")

# // start command
command()