# bot.py
import discord
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix=".")

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run("TOKEN")
