# // ---------------------------------------------------------------------
# // ------- [Quote Bot] Main
# // ---------------------------------------------------------------------

# // ---- Imports
import discord
import time
import random

import config
import quotes
import slashCommands
from events import events
from helpers import discord as discordHelpers
from helpers import general as helpers

# // ---- Variables
# // Discord
# intents
intents = discord.Intents.default()
intents.message_content = True

# client
client = discord.Client(
    intents = intents,
    
    status = discord.Status.do_not_disturb,
    activity = discord.Activity(
        type = discord.ActivityType.watching,
        name = config.activityText
    )
)

tree = discord.app_commands.CommandTree(client)

# // ---- Main
# // Register Globals
# bot
helpers.globals.save("client", client)
helpers.globals.save("commandTree", tree)
helpers.globals.save("startupTimestamp", time.time())

# quotes
helpers.globals.save("recentMessageFromUsers", {})
helpers.globals.save("quotes", quotes.quotes())

# // Register Commands
slashCommands.start()

# // Discord Events
# On Ready
@client.event
async def on_ready():
    await events.on_ready.asyncFire()

# On Message
@client.event
async def on_message(message: discord.Message):
    await events.on_message.asyncFire(
        message = message
    )
    
# // Start Bot
client.run(config.botToken, log_handler = None)