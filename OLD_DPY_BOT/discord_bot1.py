# Broc-Bot
import discord
from discord.ext import commands, tasks
from itertools import cycle
import random
import os

prefix = "b-"

client = commands.Bot(command_prefix=prefix)
status = cycle(['Algodoo', 'Discord', 'Google Chrome'])
client.remove_command("help")

@client.event
async def on_ready():
    status_update.start()
    print("Broc-Bot is ready!")

@client.event
async def on_member_join(member):
    print(f'{member} has joined the server. Greetings, {member}!')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')

@tasks.loop(seconds=900)
async def status_update():
    await client.change_presence(activity=discord.Game(next(status)))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(":exclamation: | Command Not Found")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(":exclamation: | Missing Parameters: Please pass in all required arguments. For more help for a command, say **.help [command]**")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.TooManyArguments):
        await ctx.send(":interrobang: | Too many arguments. Please give the specified amount of arguments.")

@client.command()
async def invite(ctx):
    await ctx.send("Here is the link to invite me to your server: https://discord.com/api/oauth2/authorize?client_id=694205764813979749&permissions=8&scope=bot")


@client.command(pass_context=True)
async def help(ctx,member=discord.Member):
    author = ctx.message.author
    embed = discord.Embed(color=discord.Color(3447003))

    embed.set_author(name="Help")

    if discord.permissions.manage_messages:
        embed.add_field(name=prefix + 'Fun', value="", inline=True)
        embed.add_field(name=prefix + 'copy', value="repeats user input",inline=False)
        embed.add_field(name=prefix + 'replace', value="replaces user input with bot message", inline=False)
        embed.add_field(name=prefix + 'rev', value="repeats a reversed user message", inline=False)
        embed.add_field(name=prefix + 'upper', value="repeats a capitalized user input", inline=False)
        embed.add_field(name=prefix + 'lower', value="repeats a lowercase user input", inline=False)
        embed.add_field(name=prefix + 'angry', value="repeats user input in aNgRy FoRmAt", inline=False)

    await ctx.send(embed=embed)


#This command is only to test security
"""
@client.command()
async def test(ctx):
    await ctx.send("Test!")
"""


"""
@client.command()
async def load(ctx, extension):
    client.load_extension()

@client.command()
async def unload(ctx, extension):
    client.unload_extension()
"""
for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')






client.run("Njk0MjA1NzY0ODEzOTc5NzQ5.XtWRNg.ywP0riySka_cRy3IKvQZ7t4EaII")
