import asyncio
import os
import discord
from discord.ext import commands
from dropbase import *

from settings import *

# discord gateway intents
intents = discord.Intents.default()
allowed_mentions = discord.AllowedMentions(everyone=False,
                                           users=True,
                                           roles=False)

# bot instance
bot = discord.ext.commands.Bot(command_prefix=prefix,
                               intents=intents,
                               description=description,
                               case_insensitive=True,
                               allowed_mentions=allowed_mentions)


@bot.command()
async def graph(ctx):
    await ctx.send(f"Send a file to be a graphed. It must be a {', '.join(supported_file_types)}")

    def check(message):
        return message.author == ctx.author and len(message.attachments) == 1

    msg = discord.Message
    try:
        msg = await bot.wait_for('message', check=check, timeout=60)
    except asyncio.TimeoutError:
        await ctx.send('Timed out. Please try again')

    # check if file is supported
    # FIXME: check for all in the supported file types list, not just .csv
    if ".csv" not in msg.attachments[0].filename:
        await ctx.send(f"That's not a valid file type. It must be a {', '.join(supported_file_types)}")
    else:
        # saves with filename
        await msg.attachments[0].save("file.csv")


bot.run(os.getenv('BOT_TOKEN'))