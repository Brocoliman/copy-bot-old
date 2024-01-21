import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def dice(self,ctx):
        await ctx.send(":game_die: | " + str(random.randint(1, 7)))

    @commands.command()
    async def randnum(self, ctx, start, end):
        if start >= end:
            await ctx.send(":1234: | That is not a valid input")
        else:
            await ctx.send(":1234: | " + str(random.randrange(int(start), int(end) + 1)))

    @commands.command()
    async def repeat_channel(self, ctx, channel: discord.TextChannel, *args):
        output = ''
        for word in args:
            output += str(word)
            output += " "
        await channel.send(output)

    @commands.command()
    async def repeat(self,ctx, *args):
        output = ''
        for word in args:
            output += str(word)
            output += " "
        await ctx.send(output)


def setup(client):
    client.add_cog(Fun(client))