
# // ---------------------------------------------------------------------
# // ------- [Quote Bot] On Message Event
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

from helpers import discord as discordHelpers
from helpers import general as helpers

from . import events

# // ---- Main
# // Chatbot Responses
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
    
    # // filtering
    # remove mentions from message content
    content = message.content

    for user in message.mentions:
        content = content.replace(discordHelpers.utils.mentionMember(user), "")

    # // save message
    recentMessageFromUsers[message.author.id] = message