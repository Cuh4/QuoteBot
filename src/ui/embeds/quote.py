# // ---------------------------------------------------------------------
# // ------- [Quote Bot] Quote Embed UI
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

import config
import quotes
import random
from helpers import general as helpers
from helpers import discord as discordHelpers

# // ---- Main
# // UI
async def embed(quote: quotes.classes.quote):
    # // get variables
    # discord related
    client: discord.Client = helpers.globals.get("client")
    
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
        color = discord.Color.from_rgb(*[random.randint(50, 255) for i in range(3)])
    )
    
    embed.set_author(name = name, url = discordHelpers.utils.linkUser(user) if user else "", icon_url = avatar_url)
    embed.set_footer(text = f"Quote ID: {quote.getID()} | Channel ID: {quote.getChannelID()}")
    
    return embed