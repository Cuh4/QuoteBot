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
# Format Quote Event
formatQuoteEvent = helpers.events.event("formatQuote").save()

@formatQuoteEvent.attach
async def formatQuote(quote: quotes.definitions.quote):
    # // setup variables
    # quote related
    quoteText = helpers.misc.truncateIfTooLong(quote.getText(), config.maxQuoteLength) # enforce character limit
    quoteText = discordHelpers.utils.stripMarkdown(quoteText) # remove markdown

    # quote author related
    user = client.get_user(quote.getUserID()) or await client.fetch_user(quote.getUserID())
    name = "Anonymous"
    avatar_url = client.user.display_avatar.url

    if user is not None:
        name, avatar_url = f"{user.display_name} (@{user.name})", user.display_avatar.url # get user's name and avatar url
    
    # // main
    # create embed
    embed = discord.Embed(
        description = f">>> **{quoteText}**",
        colour = discord.Color.from_rgb(*[random.randint(50, 255) for i in range(3)])
    )
    
    embed.set_author(name = name, url = discordHelpers.utils.linkUser(user) if user else "", icon_url = avatar_url)
    
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
    await events.on_message.asyncFire(
        message = message
    )
    
# // Start Bot
client.run(config.botToken, log_handler = None)