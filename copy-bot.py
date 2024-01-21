# Copy-bot.py
q = lambda a, b, c: ((-b+(b**2-4*a*c)**(1/2))/(2*a), (-b-(b**2-4*a*c)**(1/2))/(2*a))


# Setup
import discord
from discord.ext import commands

import json  # data keeping
import os  # easy access for files
import datetime  # discord embed time
from discord_bots.cogs.calc import *  # calculator

prefix = "="
DISCORD_LINK = "https://discord.gg/K9cKGGY"

os.chdir(r'...')

intents = discord.Intents.all()  # Enable all intents

client = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=intents)
client.remove_command('help')

# Not used yet
emoji_letter = ":regional_indicator_a: :regional_indicator_b: :regional_indicator_c: :regional_indicator_d: :regional_indicator_e: :regional_indicator_f: :regional_indicator_g: :regional_indicator_h: :regional_indicator_i: :regional_indicator_j: :regional_ind" \
               "icator_k: :regional_indicator_l: :regional_indicator_m: :regional_indicator_n: :regional_indicator_o: :regional_indicator_p: :regional_indicator_q: :regional_indicator_r: :regional_indicator_s: :regional_ind" \
               "icator_t: :regional_indicator_u: :regional_indicator_v: :regional_indicator_w: :regional_indicator_x: :regional_indicator_y: :regional_indicator_z: "

with open('activity.txt', 'r') as status:
    gameActivity = status.read()

TOKEN = "..."

cmd = {
    "copy": {"desc": "repeats user input", "category": "lvl1", "arguments": "[*words]"},
    "replace": {"desc": "replaces user input with bot message", "category": "lvl1", "arguments": "[*words]"},
    "upper": {"desc": "repeats a capitalized user input", "category": "lvl1", "arguments": "[*words]"},
    "lower": {"desc": "repeats a lowercase user input", "category": "lvl1", "arguments": "[*words]"},
    "reverse": {"desc": "repeats a reversed user message", "category": "lvl2", "arguments": "[*words]"},
    "angry": {"desc": "repeats user input in aNgRy FoRmAt", "category": "lvl2", "arguments": "[*words]"},
    # "translate": {"desc": "translates the user message (please use `auto` for 1st argument and `en` for 2nd argument as default usage)", "category": "lvl2",
    #           "arguments": " [source=auto] [destination=en] [*words]"},
    "shuffle": {"desc": "shuffles the message", "category": "lvl2", "arguments": "[*words]"},
    "binary": {"desc": "converts string into binary", "category": "lvl2", "arguments": "[*words]"},
    "hexadecimal": {"desc": "converts string into hex", "category": "lvl2", "arguments": "[*words]"},
    "calculate": {"desc": "calculates an arithmetic expression", "category": "lvl2", "arguments": "[expression]"},
    "format": {"desc": "formats the message in a user specified way", "category": "lvl2",
               "arguments": "[format: i-italic, b-bold, s-spoiler, `-code, ~-strikethrough, u-underline] [*words]"},
    "markdown": {"desc": "markdowns the message", "category": "lvl2",
                 "arguments": "[markdown: py-python, js-javascript, .etc] [*words]"},
    "embed": {"desc": "repeats user input in an embed", "category": "lvl5",
              "arguments": "[*words] [attach: image=None]"},
    "encrypt": {"desc": "encrypts user input with a numeric shift key", "category": "lvl5",
                "arguments": "[key: integer] [*words]"},
    "poll": {"desc": "makes a poll with reactions", "category": "lvl5",
             "arguments": "[reactions: ab-A and B; abc-A, B, and C;\n abcd-A, B, C, and D; abcde-A, B, C, D, and E;\n"
                          " updown-UP and DOWN; updownmid-UP, SHRUG, and DOWN;\n check-CHECK MARK; yn-CHECK, CROSS] [*words]"},
    "webhook": {
        "desc": "makes a webhook with the user's given message and optional avatar. You can ensure that this command "
                "is safe because the user that invokes this command will appear in the audit that shows Copy Bot creating this webhook",
        "category": "lvl5",
        "arguments": "[name: string] [*words] [attach: avatar=None]"},
    "clear": {"desc": "clears/purges a certain amount of message in the current channel", "category": "mod",
              "arguments": "[AMOUNT]"},
    "kick": {"desc": "kicks a member", "category": "mod", "arguments": "discord.Member: [MEMBER] [REASON]"},
    "ban": {"desc": "bans a member", "category": "mod", "arguments": "discord.Member: [MEMBER] [REASON]"},
    "unban": {"desc": "unbans a member", "category": "mod", "arguments": "USER: [USER_USERNAME#USER_DISCRIM]"},
    "slowmode": {"desc": "sets a slowmode for the current channel", "category": "mod",
                 "arguments": "[SLOWMODE_LENGTH]"},
    "help": {"desc": "shows this message", "category": "misc", "arguments": "NONE or COMMAND"},
    "invite": {"desc": "shows the invite link", "category": "misc", "arguments": "NONE"},
    "level": {"desc": "shows your level(gain exp using my commands)", "category": "misc", "arguments": "NONE"},
    "leaderboard": {"desc": "shows the top 10 users", "category": "", "arguments": "NONE"},
    "info": {"desc": "info about the bot", "category": "misc", "arguments": "NONE, 'levels', or 'mod'"},
}

# ============================================================================================================
# Predefined Functions
# ============================================================================================================

"""
def level_req(req):
    async def dec_func(func):
        async def res_func(ctx, *args):
            with open('users.json') as u:
                f = json.load(u)
                if str(ctx.message.author.id) in f:
                    if f[str(ctx.message.author.id)]['level'] < req:
                        await ctx.send(f":no_entry_sign:  | Make sure to get to level {req} before using this command!")
                        return
                else:
                    await ctx.send(f":no_entry_sign:  | Make sure to get to level {req} before using this command!")
                    return

            await func(ctx, *args)

        return res_func

    return dec_func"""


async def update_data(users, user):
    if not str(user.id) in users:
        users[str(user.id)] = {}
        users[str(user.id)]['experience'] = 0
        users[str(user.id)]['level'] = 1


async def add_experience(users, user, exp):
    users[str(user.id)]['experience'] += exp


async def level_up(users, user, channel):
    experience = users[str(user.id)]['experience']
    lvl_start = users[str(user.id)]['level']
    lvl_end = int(experience ** (1 / 4))

    if lvl_start < lvl_end:
        await channel.send('{} has leveled up to level {}!'.format(user.mention, lvl_end))
        users[str(user.id)]['level'] = lvl_end


# ============================================================================================================
# Events
# ============================================================================================================

# Ready
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Activity(type=discord.ActivityType.watching, name="for =help")
                                 )
    print("Ready!")


# User Join
@client.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)


@client.event
async def on_command(ctx, exp_gain=5):
    with open('users.json', 'r') as f:
        users = json.load(f)

    id = ctx.message.author.id

    if str(id) not in users:
        await update_data(users, ctx.message.author)

    if ctx.command.name in cmd:
        if not (cmd[ctx.command.name]['category'] == 'mod') and not (cmd[ctx.command.name]['category'] == 'misc'):
            if users[str(id)]['level'] >= int(cmd[ctx.command.name]['category'][3]):
                await update_data(users, ctx.message.author)
                await add_experience(users, ctx.message.author, exp_gain)
                await level_up(users, ctx.message.author, ctx.message.channel)

    try:
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)
    except:
        pass


@client.event
@commands.has_permissions(send_messages=True)
async def on_guild_join(guild):
    if guild.system_channel:
        embed = discord.Embed(
            color=discord.Color(3447003),
            title='Copy-Bot Invited!',
            description="Thanks for inviting me to your server!",
            timestamp=datetime.datetime.now()
        )

        embed.set_author(name="Copy-Bot")
        embed.set_thumbnail(url="https://github.com/Brocoliman/TheBrocolimanDing/blob/master/copy-bot.png?raw=true")
        await guild.system_channel.send(embed=embed)


@client.event
async def on_message(message):
    m = message.content

    if message.author.bot:
        await client.process_commands(message)
        return
    if m.lower() == 'ew':
        if random.random() < 0.2:
            with open('typos.txt') as typos:
                await message.channel.send(
                    f"**{random.choice(typos.read().splitlines())}** "
                    f"{'j' if random.random()<0.3 else 'i'}nde{'w' if random.random()<0.3 else 'e'}d.{',' if random.random()<0.3 else '.'}."
                )
        else:
            await message.channel.send("**EW** indeed...")

    await client.process_commands(message)


@client.event
async def on_message_delete(message):
    if message.mentions_everyone and not message.author == message.guild.owner:
        embed = discord.Embed(
            color=discord.Color(3447003),
            title='Copy-Bot Ghost Ping Detector',
            description=f"{message.author.name} pinged @everyone",
            timestamp=message.created_at
        )
        embed.set_author(name="Copy-Bot")
        embed.set_thumbnail(url=message.author.avatar_url)

        await message.channel.send(embed=embed)

    if len(message.mentions) > 0 or len(message.role_mentions) > 0:
        if message.author.bot:
            return

        ping_flag = False
        for recip in message.mentions:
            if not recip.bot and not recip == message.author:
                ping_flag = True
        if not ping_flag:
            return

        mention = []
        if len(message.mentions) > 0 and len(message.role_mentions) > 0:
            mention = [i.mention for i in message.mentions + message.role_mentions]
        elif len(message.mentions) > 0:
            mention = [member.mention for member in message.mentions]
        elif len(message.role_mentions) > 0:
            mention = [role.mention for role in message.role_mentions]

        str_mentions = ""
        for i in mention:
            str_mentions += i + ', '
        str_mentions = str_mentions[:-2]

        embed = discord.Embed(
            color=discord.Color(3447003),
            title='Copy-Bot Ghost Ping Detector',
            description=f"{message.author.name} pinged {str_mentions}",
            timestamp=message.created_at
        )
        embed.set_author(name="Copy-Bot")
        embed.set_thumbnail(url=message.author.avatar_url)

        await message.channel.send(embed=embed)


@client.event
async def on_message_edit(message, after):
    if message.mention_everyone and not after.mention_everyone:
        embed = discord.Embed(
            color=discord.Color(3447003),
            title='Copy-Bot Ghost Ping Detector',
            description=f"{message.author.name} pinged @everyone",
            timestamp=message.created_at
        )
        embed.set_author(name="Copy-Bot")
        embed.set_thumbnail(url=message.author.avatar_url)

        await message.channel.send(embed=embed)

    if len(message.mentions) > 0 or len(message.role_mentions) > 0:
        if message.author.bot:
            return

        if not (len(after.role_mentions + after.mentions) < len(message.role_mentions + message.mentions)):
            return

        ping_flag = False
        for recip in message.mentions:
            if not recip.bot and not recip == message.author:
                ping_flag = True
        if not ping_flag:
            return

        mention = []
        if len(message.mentions) > 0 and len(message.role_mentions) > 0:
            mention = [i.mention for i in message.mentions + message.role_mentions]
        elif len(message.mentions) > 0:
            mention = [member.mention for member in message.mentions]
        elif len(message.role_mentions) > 0:
            mention = [role.mention for role in message.role_mentions]

        str_mentions = ""
        for i in mention:
            str_mentions += i + ', '
        str_mentions = str_mentions[:-2]

        embed = discord.Embed(
            color=discord.Color(3447003),
            title='Copy-Bot Ghost Ping Detector',
            description=f"{message.author.name} pinged {str_mentions}",
            timestamp=message.created_at
        )
        embed.set_author(name="Copy-Bot")
        embed.set_thumbnail(url=message.author.avatar_url)

        await message.channel.send(embed=embed)


# ============================================================================================================
# Commands
# ============================================================================================================


# Basic copy command - repeats user input
@client.command(aliases=['c'])
async def copy(ctx, *args):
    output = ''
    for word in args:
        output += str(word)
        output += " "

    image = None
    for i in ctx.message.attachments:
        image = await i.to_file()
        break

    if image:
        await ctx.send(output, file=image)
    else:
        await ctx.send(output)


# Replace - replaces user input with message copy
@client.command(aliases=['rep'])
async def replace(ctx, *args):
    await ctx.message.delete()
    output = ''
    for word in args:
        output += str(word)
        output += " "

    image = None
    for i in ctx.message.attachments:
        image = await i.to_file()
        break

    if image:
        await ctx.send(output, file=image)
    else:
        await ctx.send(output)


# Upper - capitalizes user input
@client.command(aliases=['up'])
async def upper(ctx, *args):
    holder = ''
    for word in args:
        holder += word
        holder += " "

    output = holder.upper()

    image = None
    for i in ctx.message.attachments:
        image = await i.to_file()
        break

    if image:
        await ctx.send(output, file=image)
    else:
        await ctx.send(output)


# Lower - lowercases user input
@client.command(aliases=['low'])
async def lower(ctx, *args):
    holder = ''
    for word in args:
        holder += word
        holder += " "

    output = holder.lower()

    image = None
    for i in ctx.message.attachments:
        image = await i.to_file()
        break

    if image:
        await ctx.send(output, file=image)
    else:
        await ctx.send(output)


# Reverse - reverses user input
@client.command(aliases=['rev'])
async def reverse(ctx, *args):
    with open('users.json') as u:
        f = json.load(u)
        if str(ctx.message.author.id) in f:
            if f[str(ctx.message.author.id)]['level'] < 2:
                await ctx.send(":no_entry_sign:  | Make sure to get to level 2 before using this command!")
                return
        else:
            await ctx.send(":no_entry_sign:  | Make sure to get to level 2 before using this command!")
            return

    holder = ''
    for i in range(len(args)):
        holder += args[i]
        holder += " "

    output = holder[::-1]

    image = None
    for i in ctx.message.attachments:
        image = await i.to_file()
        break

    if image:
        await ctx.send(output, file=image)
    else:
        await ctx.send(output)


# angry - returns user input in angry format
@client.command(aliases=['ang'])
async def angry(ctx, *args):
    with open('users.json') as u:
        f = json.load(u)
        if str(ctx.message.author.id) in f:
            if f[str(ctx.message.author.id)]['level'] < 2:
                await ctx.send(":no_entry_sign:  | Make sure to get to level 2 before using this command!")
                return
        else:
            await ctx.send(":no_entry_sign:  | Make sure to get to level 2 before using this command!")
            return

    output = ''
    case = 'upper'
    step = 2

    for word in args:
        output += word.lower()
        output += " "

    holder = list(output)

    for char in holder:
        for i in range(len(holder)):
            if i % step == 0:
                if case == "upper":
                    holder[i] = holder[i].upper()
                else:
                    holder[i] = holder[i].lower()

    output = ''.join(holder)

    image = None
    for i in ctx.message.attachments:
        image = await i.to_file()
        break

    if image:
        await ctx.send(output, file=image)
    else:
        await ctx.send(output)


# translate - translate the message
import googletrans

trans = googletrans.Translator()


# @client.command(aliases=['trans'])
async def translate(ctx, src='auto', dest='en', *args):
    output = ""
    for word in args:
        output += word.lower()
        output += " "

    src = src.lower()
    dest = dest.lower()

    if src == 'auto':
        pass
    elif src == 'zh' or src == 'ch':
        src = 'chinese (simplified)'
    else:
        if src not in googletrans.LANGUAGES.item_keys() and src not in googletrans.LANGUAGES.items():
            await ctx.send(
                ":warning: | That is not a valid source language. Please use `=help translate` for more info")
            return

    if dest == 'auto':
        pass
    elif dest == 'zh':
        dest = 'chinese (simplified)'
    else:
        if dest not in googletrans.LANGUAGES.item_keys() and dest not in googletrans.LANGUAGES.items():
            await ctx.send(
                ":warning: | That is not a valid destination language. Please use `=help translate` for more info")
            return

    output = trans.translate(output, dest=dest, src=src).text

    await ctx.send(output)


# shuffle - shuffles the message
import random


@client.command(aliases=['shuf'])
async def shuffle(ctx, *args):
    with open('users.json') as u:
        f = json.load(u)
        if str(ctx.message.author.id) in f:
            if f[str(ctx.message.author.id)]['level'] < 2:
                await ctx.send(":no_entry_sign:  | Make sure to get to level 2 before using this command!")
                return
        else:
            await ctx.send(":no_entry_sign:  | Make sure to get to level 2 before using this command!")
            return

    output = ''
    temp = list(args)
    holder = ''

    for i in temp:
        holder += i + ' '  # holder will be the whole argument

    holder = holder[:-1]

    temp = list(holder)  # make temp into a list of all chars in holder

    random.shuffle(temp)  # shuffle the characters

    for i in temp:
        output += i  # compile the characters together

    image = None
    for i in ctx.message.attachments:
        image = await i.to_file()
        break

    for i in output:
        if i in ['fu' + 'ck', 'sh' + 'it', 'bit' + 'ch']:  # humanity
            await shuffle(ctx, *args)
            return

    if image:
        await ctx.send(output, file=image)
    else:
        await ctx.send(output)


# hex - converts the message into hex
@client.command(aliases=['hex'])
async def hexadecimal(ctx, *args):
    with open('users.json') as u:
        f = json.load(u)
        if str(ctx.message.author.id) in f:
            if f[str(ctx.message.author.id)]['level'] < 2:
                await ctx.send(":no_entry_sign:  | Make sure to get to level 2 before using this command!")
                return
        else:
            await ctx.send(":no_entry_sign:  | Make sure to get to level 2 before using this command!")
            return

    holder = ''
    for word in args:
        holder += word
        holder += " "

    hex_conv = []

    for c in holder:
        ascii_val = ord(c)

        hex_val = hex(ascii_val)
        hex_conv.append(hex_val[2:])

    output = ' '.join(hex_conv[:-1])

    image = None
    for i in ctx.message.attachments:
        image = await i.to_file()
        break

    if image:
        await ctx.send(output, file=image)
    else:
        await ctx.send(output)


# binary - converts the message into binary
@client.command(aliases=['bin'])
async def binary(ctx, *args):
    with open('users.json') as u:
        f = json.load(u)
        if str(ctx.message.author.id) in f:
            if f[str(ctx.message.author.id)]['level'] < 2:
                await ctx.send(":no_entry_sign:  | Make sure to get to level 2 before using this command!")
                return
        else:
            await ctx.send(":no_entry_sign:  | Make sure to get to level 2 before using this command!")
            return

    holder = ''
    for word in args:
        holder += word
        holder += " "

    bin_conv = []

    for c in holder:
        ascii_val = ord(c)

        binary_val = bin(ascii_val)
        bin_conv.append(binary_val[2:])

    output = ' '.join(bin_conv[:-1])

    image = None
    for i in ctx.message.attachments:
        image = await i.to_file()
        break

    if image:
        await ctx.send(output, file=image)
    else:
        await ctx.send(output)


# calculate - formats the message in a given way
@client.command(aliases=['calc', 'cal'])
async def calculate(ctx, *args):
    with open('users.json') as u:
        f = json.load(u)
        if str(ctx.message.author.id) in f:
            if f[str(ctx.message.author.id)]['level'] < 2:
                await ctx.send(":no_entry_sign:  | Make sure to get to level 2 before using this command!")
                return
        else:
            await ctx.send(":no_entry_sign:  | Make sure to get to level 2 before using this command!")
            return

    holder = ''
    for word in args:
        holder += word
        holder += " "

    try:
        output = str(solve(tokenize(holder)))
    except OverflowError:
        await ctx.send(":warning: | That value is too big. Please try another number")
        return
    except TypeError:
        await ctx.send(":warning: | That calculation returns an imaginary value. Please try again")
        return
    except IndexError:
        await ctx.send(":warning: | Please make sure you entered a valid expression.")
        return
    except TimeoutError:
        await ctx.send(":warning: | Please make sure you entered a valid expression that is not too big. "
                       "Please use * for the multiplication sign explicitly everytime you need to multiply")
        return

    await ctx.send(output)


# format - formats the message in a given way
@client.command(aliases=['fmt'])
async def format(ctx, format, *args):
    with open('users.json') as u:
        f = json.load(u)
        if str(ctx.message.author.id) in f:
            if f[str(ctx.message.author.id)]['level'] < 2:
                await ctx.send(":no_entry_sign:  | Make sure to get to level 2 before using this command!")
                return
        else:
            await ctx.send(":no_entry_sign:  | Make sure to get to level 2 before using this command!")
            return

    holder = ''
    for word in args:
        holder += word
        holder += " "

    output = holder
    if output[0] == ' ':
        output = output[0:]
    if output[len(output) - 1] == ' ':
        output = output[:-1]

    if 'i' in format.lower():
        output = "*" + output + "*"
    if 'b' in format.lower():
        output = "**" + output + "**"
    if 's' in format.lower():
        output = "||" + output + "||"
    if '`' in format.lower() and \
            not '```' in format.lower():
        output = "`" + output + "`"
    if '~' in format.lower():
        output = "~~" + output + "~~"
    if 'u' in format.lower():
        output = "__" + output + "__"

    image = None
    for i in ctx.message.attachments:
        image = await i.to_file()
        break

    if image:
        await ctx.send(output, file=image)
    else:
        await ctx.send(output)


# markdown - markdowns the message in a user specified way
@client.command(aliases=['md'])
async def markdown(ctx, md, *args):
    with open('users.json') as u:
        f = json.load(u)
        if str(ctx.message.author.id) in f:
            if f[str(ctx.message.author.id)]['level'] < 2:
                await ctx.send(":no_entry_sign:  | Make sure to get to level 2 before using this command!")
                return
        else:
            await ctx.send(":no_entry_sign:  | Make sure to get to level 2 before using this command!")
            return

    output = ''
    holder = ''
    for word in args:
        holder += word
        holder += " "

    output = holder
    output = "```{}\n".format(md) + holder + "\n```"

    image = None
    for i in ctx.message.attachments:
        image = await i.to_file()
        break

    if image:
        await ctx.send(output, file=image)
    else:
        await ctx.send(output)


# embed - turns message to embed
@client.command(aliases=['emb'])
async def embed(ctx, *args):
    with open('users.json') as u:
        f = json.load(u)
        if str(ctx.message.author.id) in f:
            if f[str(ctx.message.author.id)]['level'] < 5:
                await ctx.send(":no_entry_sign:  | Make sure to get to level 5 before using this command!")
                return
        else:
            await ctx.send(":no_entry_sign:  | Make sure to get to level 5 before using this command!")

    author = ctx.message.author

    holder = ''
    for word in args:
        holder += word
        holder += " "

    embed = discord.Embed(
        color=discord.Color(3447003),
        title='Message from ' + str(author),
        description=holder,
        timestamp=ctx.message.created_at
    )

    embed.set_author(name="Copy-Bot")
    embed.set_thumbnail(url="https://github.com/Brocoliman/TheBrocolimanDing/blob/master/copy-bot.png?raw=true")

    try:
        image = ctx.message.attachments[0].url
        embed.set_image(url=image)
    except IndexError:
        pass

    await ctx.send(embed=embed)


# encrypt - encrypts a message using a numeric shift key
@client.command(aliases=['enc', 'crypt'])
async def encrypt(ctx, strkey, *args):
    with open('users.json') as u:
        f = json.load(u)
        if str(ctx.message.author.id) in f:
            if f[str(ctx.message.author.id)]['level'] < 5:
                await ctx.send(":no_entry_sign:  | Make sure to get to level 5 before using this command!")
                return
        else:
            await ctx.send(":no_entry_sign:  | Make sure to get to level 5 before using this command!")

    output = ''
    for word in args:
        output += str(word)
        output += " "

    casing = []
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    cryptletters = letters

    key = int(strkey)

    def rotate(arr, l):
        return arr[l:] + arr[:l]

    for i in range(len(output)):
        if output[i].isupper():
            casing.append(True)
        else:
            casing.append(False)

    output = output.lower()
    cryptletters = rotate(cryptletters, key)

    for i in range(len(output)):
        for j in range(len(letters)):
            if output[i] == letters[j]:
                output = output[:i] + cryptletters[j] + output[i + 1:]
                break

    output = output.lower()

    for i in range(len(casing)):
        if casing[i]:
            output = output[:i] + output[i].upper() + output[i + 1:]

    image = None
    for i in ctx.message.attachments:
        image = await i.to_file()
        break

    if image:
        await ctx.send(output, file=image)
    else:
        await ctx.send(output)


# poll - makes a poll with either abc choices or (yes, maybe, no)
@client.command()
async def poll(ctx, type, *args):
    with open('users.json') as u:
        f = json.load(u)
        if str(ctx.message.author.id) in f:
            if f[str(ctx.message.author.id)]['level'] < 5:
                await ctx.send(":no_entry_sign:  | Make sure to get to level 5 before using this command!")
                return
        else:
            await ctx.send(":no_entry_sign:  | Make sure to get to level 5 before using this command!")

    output = ''
    for word in args:
        output += str(word)
        output += " "

    if output != '':
        image = None
        for i in ctx.message.attachments:
            image = await i.to_file()
            break

        if type == "ab" or type == "abc" or type == "abcd" or type == "abcde" or type == "updown" or type == "updownmid" \
                or type == "check" or type == "yn":
            if image:
                message = await ctx.send(output, file=image)
            else:
                message = await ctx.send(output)

        if type == "ab":
            await message.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER A}')
            await message.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER B}')
        elif type == "abc":
            await message.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER A}')
            await message.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER B}')
            await message.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER C}')
        elif type == "abcd":
            await message.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER A}')
            await message.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER B}')
            await message.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER C}')
            await message.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER D}')
        elif type == "abcde":
            await message.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER A}')
            await message.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER B}')
            await message.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER C}')
            await message.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER D}')
            await message.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER E}')
        elif type == "updown":
            await message.add_reaction('\N{UPWARDS BLACK ARROW}')
            await message.add_reaction('\N{DOWNWARDS BLACK ARROW}')
        elif type == "updownmid":
            await message.add_reaction('\N{UPWARDS BLACK ARROW}')
            await message.add_reaction('\N{SHRUG}')
            await message.add_reaction('\N{DOWNWARDS BLACK ARROW}')
        elif type == "check":
            await message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
        elif type == "yn":
            await message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
            await message.add_reaction('\N{CROSS MARK}')
        else:
            await ctx.send(
                f":warning: | That is not a valid poll. Use either `{prefix}poll check ...`, `{prefix}poll yn ...`, `"
                f"{prefix}poll ab ...`, `{prefix}poll abc ...`, `{prefix}poll abcd ...`, `{prefix}poll abcde ...`, `"
                f"{prefix}poll updown ...` or `{prefix}poll updownmid ...`")
    else:
        await ctx.send(
            f":warning: | That is not a valid poll. Use either `{prefix}poll check ...`, `{prefix}poll yn ...`, `"
            f"{prefix}poll ab ...`, `{prefix}poll abc ...`, `{prefix}poll abcd ...`, `{prefix}poll abcde ...`, `"
            f"{prefix}poll updown ...` or `{prefix}poll updownmid ...`")


# webhook - creates a temporary webhook to use and sends a message with it
@client.command(aliases=['web', 'hook'])
async def webhook(ctx, name, *args):
    with open('users.json') as u:
        f = json.load(u)
        if str(ctx.message.author.id) in f:
            if f[str(ctx.message.author.id)]['level'] < 5:
                await ctx.send(":no_entry_sign:  | Make sure to get to level 5 before using this command!")
                return
        else:
            await ctx.send(":no_entry_sign:  | Make sure to get to level 5 before using this command!")

    holder = ''
    for word in args:
        holder += word
        holder += " "

    n = ''
    for i in name:
        if i == "_":
            n += " "
        else:
            n += i

    try:
        image = await ctx.message.attachments[0].read(use_cached=True)
        w = await ctx.channel.create_webhook(name=n, avatar=image,
                                             reason=f"Command invoked by {ctx.message.author.name}, id: "
                                                    f"{ctx.message.author.id}")
    except IndexError:
        w = await ctx.channel.create_webhook(name=n, reason=f"Command invoked by {ctx.message.author.name}, id: "
                                                            f"{ctx.message.author.id}")
    except discord.ext.commands.errors.CommandInvokeError:
        await ctx.send(
            ":warning: | Missing Permissions. Please enable permission MANAGE WEBHOOKS or ADMIN for this bot")
        return

    try:
        await w.send(holder, username=n)
    except:
        await ctx.send(":warning: | Please enter a message for the webhook to send")
    else:
        await ctx.message.delete()
    finally:
        await w.delete()


# ============================================================================================================
# Mod Commands
# ============================================================================================================

# clear - purges message from the channel
@client.command(aliases=['purge'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount):
    if int(amount) < 0 or int(amount) > 5000:
        await ctx.send(":warning: | That is not a valid value. Please enter a positive integer value less than 5000")
        return

    try:
        await ctx.channel.purge(limit=int(amount) + 1)
        await ctx.send(f":white_check_mark: | Successfully purged {amount} messages", delete_after=5)
        await ctx.message.delete(delay=5)
    except (commands.errors.MissingPermissions, commands.errors.CommandInvokeError):
        await ctx.send(
            ":warning: | I do not have permissions to do this. Please check the guild/channel permissions for me")
    except ValueError:
        await ctx.send(":warning: | That is not a valid value. Please enter an integer value")


# ban - bans a member
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f':white_check_mark: | Successfully banned {member.mention}', delete_after=5)
        await ctx.message.delete(delay=5)
    except (commands.errors.MissingPermissions, commands.errors.CommandInvokeError):
        await ctx.send(
            ":warning: | I do not have permissions to do this. Please check the guild/channel permissions for me")


# kick - kicks a member
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
        await ctx.send(f':white_check_mark: | Successfully kicked {member.mention}', delete_after=5)
        await ctx.message.delete(delay=5)
    except (commands.errors.MissingPermissions, commands.errors.CommandInvokeError):
        await ctx.send(
            ":warning: | I do not have permissions to do this. Please check the guild/channel permissions for me")


# unban - unbans a user
@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            try:
                await ctx.guild.unban(user)
                await ctx.send(f':white_check_mark: | Successfully unbanned {user.name}#{user.discriminator}',
                               delete_after=5)
                await ctx.message.delete(delay=5)
            except (commands.errors.MissingPermissions, commands.errors.CommandInvokeError):
                await ctx.send(
                    ":warning: | I do not have permissions to do this. Please check the guild/channel permissions for me")
            return

    await ctx.send(f':warning: | Did not find user {user.name}#{user.discriminator}', delete_after=5)


# slowmode - casts a slowmode onto the current channel
@client.command(aliases=['slow'])
@commands.has_permissions(manage_messages=True)
async def slowmode(ctx, time):
    try:
        await ctx.channel.edit(slowmode_delay=int(time))
        await ctx.send(f":white_check_mark: | Successfully set slowmode to {time} seconds", delete_after=5)
        await ctx.message.delete(delay=5)
    except commands.errors.MissingPermissions:
        await ctx.send(
            ":warning: | I do not have permissions to do this. Please check the guild/channel permissions for me")
    except (ValueError, commands.errors.CommandInvokeError):
        await ctx.send(":warning: | That is not a valid value. Please enter a positive integer value")


# ============================================================================================================
# Misc. Commands
# ============================================================================================================


# Console Copy Command - repeats console input
@client.command()
async def cs_CMD(ctx):
    async def send(context):
        while True:
            msg = input("Console MSG:\n")
            if msg == '':
                continue
            elif msg == 'exit':
                await context.send(":slight_smile: | Dropping Off!")
                break
            elif msg.startswith('purge'):
                await context.channel.purge(limit=int(msg[6:]))
            elif msg == 'type' or msg == 'typing':
                with context.channel.typing():
                    await send(context)
            elif msg == 'untype':
                return
            else:
                await ctx.send(msg)

    if ctx.message.author.id == 663543937197146122:
        await ctx.message.delete()
        await send(ctx)


# Level checker
@client.command(aliases=['l', 'rank'])
async def level(ctx, m: discord.Member = None):
    author = ctx.message.author

    with open('users.json', 'r') as f:
        users = json.load(f)

    if not m:
        if str(author.id) in users:
            embed = discord.Embed(
                color=discord.Color(3447003),
                title=str(author) + "'s level info:",
                description="This is the level information for " + str(author),
                timestamp=ctx.message.created_at
            )

            embed.set_author(name='Copy-Bot')
            embed.set_thumbnail(url=author.avatar_url)

            embed.add_field(name="Level", value=users[str(author.id)]['level'], inline=False)
            embed.add_field(name="Experience", value=users[str(author.id)]['experience'], inline=False)

            await ctx.send(embed=embed)

        else:
            print("not in")
            await ctx.send(":no_entry_sign:  | Please use a command before checking your level")
            await on_command(ctx, exp_gain=0)

    else:
        try:
            if not m.id in users:
                embed = discord.Embed(
                    color=discord.Color(3447003),
                    title=m.name + "'s level info:",
                    description="This is the level information for " + m.name,
                    timestamp=ctx.message.created_at
                )

                embed.set_author(name='Copy-Bot')
                embed.set_thumbnail(url=m.avatar_url)

                embed.add_field(name="Level", value=users[str(m.id)]['level'], inline=False)
                embed.add_field(name="Experience", value=users[str(m.id)]['experience'], inline=False)

                await ctx.send(embed=embed)

        except:
            await ctx.send(":no_entry_sign:  | That user has not used a command yet")


# Level leaderboard
@client.command(aliases=['s', 'scoreboard', 'leader', 'scores'])
async def leaderboard(ctx):
    # author = ctx.message.author

    with open('users.json', 'r') as f:
        users = json.load(f)

    sortdict = {}
    for i in users:
        sortdict.update({i: users[i]['experience']})  # appends userID:exp pairs to the sortdict

    temp = sorted(sortdict.items(), key=lambda x: x[1],
                  reverse=True)  # makes a list of tuples of the sorted dictionary (id, exp)

    embed = discord.Embed(
        color=discord.Color(3447003),
        title='Copy-Bot Leaderboard',
        description=f"These are the top 10 users! \nFor more information about me, go to {DISCORD_LINK}",
        timestamp=ctx.message.created_at
    )

    embed.set_author(name="Copy-Bot")
    embed.set_thumbnail(url="https://github.com/Brocoliman/TheBrocolimanDing/blob/master/copy-bot.png?raw=true")

    for i in range(10):
        header = ''
        try:
            x = client.get_user(int(temp[i][0])).name
        except AttributeError:  # If user not found
            with open("users.json", 'w') as w:
                users.pop(temp[i][0])
                json.dump(users, w)
            await leaderboard(ctx)

        if i == 0:
            header = 'st: '
        elif i == 1:
            header = 'nd: '
        elif i == 2:
            header = 'rd: '
        else:
            header = 'th: '
        header = str(i + 1) + header
        embed.add_field(name=header + x,
                        value="Level: " + str(users[temp[i][0]]['level']) + "\nExperience: " + str(temp[i][1]),
                        inline=True)
    await ctx.send(embed=embed)


# Status changer - Broc only
@client.command()
async def set(ctx, *args):
    global gameActivity
    author = ctx.message.author
    holder = ''
    for word in args[1:]:
        holder += word
        holder += " "
    if str(author) == "Broc#8247":
        if args[0] == 'game':
            with open('activity.txt', 'r') as r_status:
                with open('activity.txt', 'w') as w_status:
                    w_status.write(holder)

            await ctx.send(":white_check_mark: | Success!")

            with open('activity.txt', 'r') as activity:
                gameActivity = activity.read()
                await client.change_presence(status=discord.Status.online, activity=discord.Game(gameActivity))
        if args[0] == 'watch':
            with open('activity.txt', 'r') as r_status:
                with open('activity.txt', 'w') as w_status:
                    w_status.write(holder)

            await ctx.send(":white_check_mark: | Success!")

            with open('activity.txt', 'r') as activity:
                gameActivity = activity.read()
                await client.change_presence(
                    status=discord.Status.online,
                    activity=discord.Activity(type=discord.ActivityType.watching, name=gameActivity)
                )

    else:
        await ctx.send(":no_entry_sign:  | You are not Brocolimanx...most likely...")


# Run command - Broc
# @client.command()
async def run(ctx, *args):
    if ctx.author.id == 663543937197146122:
        code = ''
        for arg in args:
            code += arg + ' '

        exec(code)


# Info command - all
@client.command(pass_context=True, aliases=['i'])
async def info(ctx, specific="bot"):
    author = ctx.message.author

    with open('users.json', 'r') as f:
        users = json.load(f)

    s = specific.lower()
    if s == "bot":
        embed = discord.Embed(
            color=discord.Color(3447003),
            title='Copy-Bot Info',
            description="Hi! I'm Copy-Bot. Nice to meet you! I am a fun/level/mod bot.\nFor more information about me, go to "
                        "" + DISCORD_LINK + "",
            timestamp=ctx.message.created_at
        )

        embed.set_author(name="Copy-Bot")
        embed.set_thumbnail(url="https://github.com/Brocoliman/TheBrocolimanDing/blob/master/copy-bot.png?raw=true")

        embed.add_field(name="Joined this server", value=str(ctx.guild.me.joined_at)[:-7], inline=False)
        embed.add_field(name="Owner", value="Broc#8247", inline=True)
        # embed.add_field(name="Uptime", value=tdelta, inline=False)
        embed.add_field(name="Ping", value=str(client.latency)[:-14], inline=True)
        embed.add_field(name="Guilds", value=str(len(client.guilds)), inline=True)
        embed.add_field(name="Users", value=str(len(users)), inline=True)

    elif s == "level" or s == "levels" or s == "ranks":
        embed = discord.Embed(
            color=discord.Color(3447003),
            title='Copy-Bot Info',
            description=f"Hi! I'm Copy-Bot. Here is the information about my leveling system / FAQ about it. \nFor more information about me, go to "
                        "" + DISCORD_LINK + "",
            timestamp=ctx.message.created_at
        )

        embed.set_author(name="Copy-Bot")
        embed.set_thumbnail(url="https://github.com/Brocoliman/TheBrocolimanDing/blob/master/copy-bot.png?raw=true")

        embed.add_field(name="What is the Leveling System?",
                        value='Basically, you get exp or xp from using my commands, '
                              'and you get to use special perks at certain levels!', inline=False)
        embed.add_field(name="How do I earn experience?", value='To earn exp, simply use my commands! Note that my '
                                                                'miscellaneous commands and mod commands don\'t earn exp. ',
                        inline=False)
        embed.add_field(name="What can I do with exp?",
                        value='Getting exp levels you up! If you get to a certain level, '
                              'you get certain perks like cooler commands!', inline=False)
        embed.add_field(name="Stats", value=f'There is a total of **{len(users)}** users!\n', inline=False)

    elif s == "mod" or s == "moderator":
        embed = discord.Embed(
            color=discord.Color(3447003),
            title='Copy-Bot Info',
            description="Hi! I'm Copy-Bot. Here is the information about my moderator commands.\nFor more information about me, go to "
                        "" + DISCORD_LINK + "",
            timestamp=ctx.message.created_at
        )

        embed.set_author(name="Copy-Bot")
        embed.set_thumbnail(url="https://github.com/Brocoliman/TheBrocolimanDing/blob/master/copy-bot.png?raw=true")

        embed.add_field(name="Info",
                        value='Moderator commands are commands that you can easily use to manage the members in the guild',
                        inline=False)
        embed.add_field(name="Who can use them?",
                        value='Only people who have certain permissions can use certain mod commands', inline=False)

    else:
        await ctx.send(":warning: | That is not a valid module!")
        return

    await ctx.send(embed=embed)


# Help command - all
@client.command(pass_context=True, aliases=['h'])
async def help(ctx, command=None):
    author = ctx.message.author

    if not command:
        embed = discord.Embed(
            color=discord.Color(3447003),
            title='Copy-Bot Commands',
            description="Here are a list of commands so far.\nFor more information, " + DISCORD_LINK + "",
        )

        embed.set_author(name="Copy-Bot")
        embed.set_thumbnail(url="https://github.com/Brocoliman/TheBrocolimanDing/blob/master/copy-bot.png?raw=true")

        embed.add_field(name=str(prefix) + '------------------------------------------------------------',
                        value="**Basic (lvl 0&1) Commands**", inline=False)
        for i in cmd:
            if cmd[i]['category'] == 'lvl1':
                embed.add_field(name=str(prefix) + i, value=cmd[i]['desc'], inline=True)

        embedL2 = discord.Embed(
            color=discord.Color(3447003),
            timestamp=ctx.message.created_at
        )

        embedL2.add_field(name=str(prefix) + '------------------------------------------------------------',
                          value="**Novice (lvl 2) Commands**", inline=False)

        for i in cmd:
            if cmd[i]['category'] == 'lvl2':
                embedL2.add_field(name=str(prefix) + i, value=cmd[i]['desc'], inline=True)

        embedL5 = discord.Embed(
            color=discord.Color(3447003),
            timestamp=ctx.message.created_at
        )

        embedL5.add_field(name=str(prefix) + '------------------------------------------------------------',
                          value="**Rookie (lvl 5) Commands**", inline=False)

        for i in cmd:
            if cmd[i]['category'] == 'lvl5':
                embedL5.add_field(name=str(prefix) + i, value=cmd[i]['desc'], inline=True)

        embedMod = discord.Embed(
            color=discord.Color(3447003),
            timestamp=ctx.message.created_at
        )

        embedMod.add_field(name=str(prefix) + '------------------------------------------------------------',
                           value="**Moderator Commands**", inline=False)

        for i in cmd:
            if cmd[i]['category'] == 'mod':
                embedMod.add_field(name=str(prefix) + i, value=cmd[i]['desc'], inline=True)

        embedMisc = discord.Embed(
            color=discord.Color(3447003),
            timestamp=ctx.message.created_at
        )

        embedMisc.add_field(name=str(prefix) + '------------------------------------------------------------',
                            value="**Misc Commands**", inline=False)

        for i in cmd:
            if cmd[i]['category'] == 'misc':
                embedMisc.add_field(name=str(prefix) + i, value=cmd[i]['desc'], inline=True)

        if not isinstance(ctx.message.channel, discord.DMChannel):
            await ctx.send(":white_check_mark: | The commands were sent to your DMs!")
        await ctx.message.author.send(embed=embed)
        await ctx.message.author.send(embed=embedL2)
        await ctx.message.author.send(embed=embedL5)
        await ctx.message.author.send(embed=embedMod)
        await ctx.message.author.send(embed=embedMisc)

    else:
        try:
            embed = discord.Embed(
                color=discord.Color(3447003),
                title=f'Command: {command}',
                description=f"Here is the information for command {command}",
                timestamp=ctx.message.created_at
            )

            embed.set_author(name="Copy-Bot")
            embed.set_thumbnail(url="https://github.com/Brocoliman/TheBrocolimanDing/blob/master/copy-bot.png?raw=true")

            x = ''
            if cmd[command]['category'] == 'lvl1':
                x = 'none'
            elif cmd[command]['category'] == 'lvl2':
                x = 'be level 2'
            elif cmd[command]['category'] == 'lvl5':
                x = 'be level 5'
            elif cmd[command]['category'] == 'misc':
                x = 'none'
            elif cmd[command]['category'] == 'mod':
                x = 'have moderator permissions in this guild'

            embed.add_field(name=str(prefix) + command, value=cmd[command]['desc'], inline=False)
            embed.add_field(name="Requirements", value=x, inline=False)
            embed.add_field(name="Arguments", value=f"```{cmd[command]['arguments']}```", inline=False)

            await ctx.send(embed=embed)

        except KeyError:
            await ctx.send(
                ":warning: | That command wasn't found. Make sure to type the name of the command listed in the `=help` command!")


# Invite command - all
@client.command()
async def invite(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        color=discord.Color(3447003),
        title='Invite Copy-Bot',
        description="These are the links I associate with:",
        timestamp=ctx.message.created_at
    )

    embed.set_author(name="Copy-Bot")
    embed.set_thumbnail(url="https://github.com/Brocoliman/TheBrocolimanDing/blob/master/copy-bot.png?raw=true")

    embed.add_field(name="Invite me to your server",
                    value="[Invite](https://discord.com/api/oauth2/authorize?client_id=738958895015526411&permissions=8&scope=bot)",
                    inline=False)
    embed.add_field(name="Brocolimanx's Hangout", value="[Server Link](" + DISCORD_LINK + ")", inline=False)

    await ctx.send(embed=embed)


client.run(f'{TOKEN}')
