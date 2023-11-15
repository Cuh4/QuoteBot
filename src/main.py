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
helpers.globals.save("client", client)
helpers.globals.save("commandTree", tree)
helpers.globals.save("recentMessageFromUsers", {})
helpers.globals.save("quotes", quotes.quotes())
helpers.globals.save("startupTimestamp", time.time())

# // Register Events
formatQuoteEvent = helpers.events.event("formatQuote").save()
@formatQuoteEvent.attach
def formatQuote(quote: quotes.definitions.quote):
    # setup embed
    quoteText = helpers.misc.truncateIfTooLong(quote.getText(), config.maxQuoteLength)
    
    embed = discord.Embed(
        description = f"\"**{quoteText}**\"",
        colour = discord.Color.from_rgb(*[random.randint(200, 255) for i in range(3)])
    )
    
    # setup embed footer
    user = client.get_user(quote.getUserID())
    name, avatar_url = "Anonymous", None
    
    if user is not None:
        name, avatar_url = f"{user.display_name} (@{user.name})", user.display_avatar.url
    
    embed.set_footer(
        text = f"- {name}",
        icon_url = avatar_url if avatar_url is not None else client.user.display_avatar.url
    )
    
    # return
    return embed

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
    # fire event
    await events.on_message.asyncFire(
        message = message
    )
    
# // Start Bot
client.run(config.botToken)