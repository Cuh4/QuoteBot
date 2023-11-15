
# // ---------------------------------------------------------------------
# // ------- [Quote Bot] On Message Event
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

from helpers import discord as discordHelpers
from helpers import general as helpers

from . import events

# // ---- Main
# // Message History
@events.on_message.attach
async def callback(**data):
    # // get needed vars
    # get discord stuffs
    client: discord.Client = helpers.globals.get("client")
    message: discord.Message = data.get("message")
    
    # get recent messages
    recentMessageFromUsers: dict[int, discord.Message] = helpers.globals.get("recentMessageFromUsers")

    # // basic checks
    # ignore messages sent by bots
    if message.author.bot:
        return
    
    # send help message if the message mentions the bot
    if discordHelpers.utils.isMentioned(message.mentions, client.user):
        return await message.channel.send(
            embed = discordHelpers.embeds.info("To quote someone's message, use </quote:1174424282772807761>."),
            reference = message,
            mention_author = True
        )
    
    # // filtering
    # remove mentions from message content
    content = message.content

    for user in message.mentions:
        content = content.replace(discordHelpers.utils.mentionMember(user), "")

    # // save message
    recentMessageFromUsers[message.author.id] = message