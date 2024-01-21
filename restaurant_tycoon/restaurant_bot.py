### Restaurant Tycoon

# Setup
import discord
from discord.ext import commands

import os  # easy access for files
import datetime  # discord embed time
import json
import math
import random

prefix = "$"
DISCORD_LINK = "https://discord.gg/K9cKGGY"

os.chdir(r'/Users/jinghuang/Desktop/python_spyder/discord_bots/restaurant_tycoon')

intents = discord.Intents.all()  # Enable all intents

client = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=intents)
client.remove_command('help')

"""
Add:
- shop for equipment
- make menu and restaurant commands work on other users
"""

TOKEN = "ODMwNTAzMzI5MzA1MDY3NTQx.YHHofw.j-ABRhvi9gUsCHPZv00DSInhLtE"
img_url = "https://raw.githubusercontent.com/Brocoliman/Files/374c6b7b53846ff837dc4913cc7533380a390a47/discord-avatar-512%20(1).png"

# Work cooldown time
cld_time = 10

cmd = {
    "help": {"desc": "shows all commands or details a certain command", "arguments": "[optional command name]",
             "aliases": [], "subcommands": {}},
    "invite": {"desc": "gives invite link for the bot", "arguments": "none",
               "aliases": [], "subcommands": {}},
    "create": {"desc": "starts your restaurant; use underscores as spaces for your restaurant name",
               "arguments": "[name][image: icon]", "aliases": ['c'], "subcommands": {}},
    "restaurant": {"desc": "repeats user input", "arguments": "{subcommand} or none", "aliases": ['r', 'restr'],
                   "subcommands": {
                       "name": {"desc": "rename your restaurant", "arguments": "[new name]"},
                       "icon": {"desc": "changes your restaurant's icon", "arguments": "[image: icon]"},
                       "delete": {"desc": "deletes your restaurant (will be permanent once you pass the warning)",
                                  "arguments": "none, but you will need to confirm using a message"},
                       "view": {"desc": f"view your restaurant in whole (using `{prefix}restaurant` will do the same",
                                "arguments": "none"},
                   }},
    "menu": {"desc": "view or edit your menu", "arguments": "{subcommand} or none", "aliases": ['m'], "subcommands": {
        "add": {"desc": "add an item to your menu", "arguments": "[item name], ['appetizer', 'entree', 'dessert',"
                                                                 " or 'drink'], [item price], [item component]"},
        "edit": {"desc": "edit an item already in your menu", "arguments": "[name of item to edit], ['appetizer', "
                                                                           "'entree', 'dessert',  or 'drink'], "
                                                                           "[item price], [item component]"},
        "view": {"desc": f"view your menu in whole (using `{prefix}menu` will do the same)", "arguments": "none"},
        "remove": {"desc": f"remove an item from your menu", "arguments": "[item name]"},
        "components": {"desc": "lists out the components you can use", "arguments": "[component reference name] or none"},
    }},
    "work": {"desc": f"works a day in your restaurant, gaining you money; cooldown of **{cld_time}** minutes",
             "arguments": "none",
             "aliases": ['w'], "subcommands": {}},
    "shop": {"desc": "shows the shop", "arguments": "{subcommand} or none", "aliases": ['s', 'sh'], "subcommands": {
        "view": {"desc": "view the whole shop (using `{prefix}menu` will do the same)", "arguments": "none"},
        "buy": {"desc": "buy an item from the shop", "arguments": "[item reference name] [optional: amount of items]"},
    }},
}

components = {
    "beef": {
        'filet_butterBasted':
            {"name": 'Filet Mignon, Butter Basted', "size": 8, "cuisine": "european", "supply": 14,
             "enjoy_price": 15,
             "service": 5, "required": ['prep/mix_counter', 'stove', 'pan', 'oven']},
        'ribeye_butterBasted':
            {"name": 'Beef Ribeye, Butter Basted', "size": 16, "cuisine": "european", "supply": 16,
             "enjoy_price": 17,
             "service": 5, "required": ['prep/mix_counter', 'stove', 'pan']},
    },
    "chicken": {
        'breast_baked':
            {"name": 'Oven Baked Chicken Breast', "size": 16, "cuisine": "european", "supply": 5, "enjoy_price": 7,
             "service": 3, "required": ['prep/mix_counter', 'oven', 'tray']},
        'breast_dicedWOrangeSauce':
            {"name": 'Orange Chicken', "size": 16, "cuisine": "chinese", "supply": 5, "enjoy_price": 6,
             "service": 2,
             "required": ['prep/mix_counter', 'stove', 'pan']},
        'breast_dicedWKungPaoSauce':
            {"name": 'Kung Pao Chicken', "size": 16, "cuisine": "chinese", "supply": 5, "enjoy_price": 6,
             "service": 2,
             "required": ['prep/mix_counter', 'stove', 'pan']},
    },
    "noodle": {
        'fettuccine_alfredo':
            {"name": 'Alfredo Fettuccine', "size": 16, "cuisine": "italian", "supply": 3, "enjoy_price": 7,
             "service": 3,
             "required": ['stove', 'pan']},
        'spaghetti_marinaraWMeatball':
            {"name": 'Spaghetti & Meatballs with Marinara', "size": 16, "cuisine": "american", "supply": 3,
             "enjoy_price": 6,
             "service": 2, "required": ['stove', 'pan']},
        'macaroni_baked':
            {"name": 'Baked Mac & Cheese', "size": 16, "cuisine": "american", "supply": 2, "enjoy_price": 8,
             "service": 2,
             "required": ['stove', 'pan', 'pot', 'oven', 'tray']},
    },
    "rice": {
        'risotto_mushroom':
            {"name": 'Mushroom Risotto', "size": 16, "cuisine": "italian", "supply": 4, "enjoy_price": 8,
             "service": 3,
             "required": ['stove', 'pan', 'pot']},
        'paella_seafood':
            {"name": 'Seafood Paella', "size": 16, "cuisine": "spanish", "supply": 6, "enjoy_price": 10,
             "service": 3,
             "required": ['prep/mix_counter', 'stove', 'pan']},
    },
    "potato": {
        'potato_mashed':
            {"name": 'Mashed Potatoes', "size": 8, "cuisine": "american", "supply": 1, "enjoy_price": 2,
             "service": 1,
             "required": ['prep/mix_counter', 'stove', 'pot']},
        'potato_baked':
            {"name": 'Buttery Baked Potatoes', "size": 8, "cuisine": "american", "supply": 1, "enjoy_price": 4,
             "service": 2,
             "required": ['prep/mix_counter', 'oven', 'tray']},
    },
    "breads": {
        'baguette':
            {"name": 'Small Baguette', "size": 8, "cuisine": "french", "supply": 0.25, "enjoy_price": 0.5,
             "service": 1,
             "required": ['prep/mix_counter', 'oven', 'tray', 'pot']},
        'burgerBun':
            {"name": 'Burger Bun', "size": 6, "cuisine": "american", "supply": 0.25, "enjoy_price": 0.25,
             "service": 1,
             "required": ['prep/mix_counter', 'oven', 'tray']},
    },
    "baked": {
        'applePie':
            {"name": 'Apple Pie', "size": 12, "cuisine": "british", "supply": 3, "enjoy_price": 5, "service": 4,
             "required": ['prep/mix_counter', 'pot', 'oven', 'baking_pan']}
    },
    "cold": {
        'iceCream_vanilla':
            {"name": 'Vanilla Ice Cream', "size": 4, "cuisine": "american", "supply": 0.5, "enjoy_price": 1, "service": 1,
             "required": ['prep/mix_counter', 'pot', 'refrigerator', 'ice_cream_machine']}
    },
    "drinks": {
        'water':
            {"name": 'Water', "size": 16, "cuisine": "none", "supply": 0, "enjoy_price": 0, "service": 0,
             "required": ['refrigerator']}
    }
}

locations = {
    "village": {'price': 0, 'customer_range': (5, 15)},
    "plaza": {'price': 10000, 'customer_range': (30, 65)},
    "downtown": {'price': 100000, 'customer_range': (60, 200)},
    "beach": {'price': 1000000, 'customer_range': (195, 500)},
}

shop_items = {
    'prep/mix_counter': {'name': 'Preparation and Mixing Counter', 'desc':
        'mix and prepare your ingredients for cooking', 'price': 100, },
    'stove': {'name': 'Stove', 'desc': 'cooking your food with this', 'price': 600, },
    'pan': {'name': 'Frying Pan', 'desc': 'the main equipment for sauteing and many frying methods', 'price': 50, },
    'refrigerator': {'name': 'Refrigerator', 'desc': 'freeze or cool down ingredients before or while cooking',
                     'price': 2500, },
    'pot': {'name': 'Pot', 'desc': 'for heating up and cooking non solids', 'price': 50, },
    'oven': {'name': 'Oven', 'desc': 'the number one item for baking and roasting', 'price': 2250, },
    'tray': {'name': 'Baking Tray', 'desc': 'put your item on this before baking', 'price': 10, },
    'baking_pan': {'name': 'Baking Pan', 'desc': 'for your batter or layers of cake', 'price': 25, },
    'ice_cream_machine': {'name': 'Ice Cream Churner', 'desc': 'just for ice cream churning', 'price': 150, },
}

components_delayered_lower = {}
for section in components:
    for component in components[section].items():
        components_delayered_lower.update({component[0].lower(): component[1]})

color_embed = 15844367
color_error = 15158332
color_success = 3066993

with open('data.json') as data_file:
    try:
        data = json.load(data_file)
    except ValueError:
        data = {}


# ============================================================================================================
# Predefined Functions
# ============================================================================================================

async def update_data():
    with open('data.json', 'w') as w_file:
        json.dump(data, w_file, indent=4)


async def level_up(data, user, channel):
    experience = data[str(user.id)].exp
    lvl_start = data[str(user.id)].level
    lvl_end = int(experience ** (1 / 4))

    if lvl_start < lvl_end:
        await channel.send('{} has leveled up to level {}!'.format(user.mention, lvl_end))
        data[str(user.id)].level = lvl_end
        await update_data()


def make_embed(ctx, title, description, color=color_embed, thumb=img_url, img=None, author=True, timestamp=True):
    if timestamp:
        embed = discord.Embed(
            color=discord.Color(color),
            title=title,
            description=description,
            timestamp=ctx.message.created_at
        )
    else:
        embed = discord.Embed(
            color=discord.Color(color),
            title=title,
            description=description
        )
    if author:
        embed.set_author(name="Restaurant Tycoon")
    if img:
        embed.set_image(url=img)
    embed.set_thumbnail(url=thumb)
    return embed


# ============================================================================================================
# Algorithms
# ============================================================================================================

def get_visit_rate(id):
    r_data = data[str(id)]

    # If nothing on the menu, no visitors
    if len(r_data['menu']) == 0: return 0

    # If menu size is too low, chances are reduced
    menu_factor = round((math.log(min(max(len(r_data['menu']), 2), 20)) / math.log(20)) ** (1 / 6) * 100) / 100

    # See whether the price is worth it or not based on the stars
    entree_overprice = 0
    other_overprice = 0

    entree_count = 0
    other_count = 0

    weighted_overprice = 0

    for item_name in r_data['menu']:
        item = r_data['menu'][item_name]
        if item['category'] == 'entree':
            entree_overprice += item['price'] - (components_delayered_lower[item['components']]['supply'] +
                                                 components_delayered_lower[item['components']]['service'] +
                                                 components_delayered_lower[item['components']]['enjoy_price'])
            entree_count += 1
        else:
            other_overprice += item['price'] - (components_delayered_lower[item['components']]['supply'] +
                                                components_delayered_lower[item['components']]['service'] +
                                                components_delayered_lower[item['components']]['enjoy_price'])
            other_count += 1

    if entree_count:
        entree_overprice /= entree_count
        weighted_overprice += 3 / 4 * entree_overprice
    else:
        weighted_overprice = other_overprice / other_count

    if other_count:
        other_overprice /= other_count
        weighted_overprice += 1 / 4 * other_overprice
    else:
        weighted_overprice = entree_overprice / entree_count

    if weighted_overprice > 0:
        s = r_data['stars']
        price_factor = max(0.1, 1 - (math.log(weighted_overprice + 1) / math.log(10 * s + 1)) ** (s / 2))
    else:
        price_factor = 1

    # print(weighted_overprice, menu_factor)

    return round(((price_factor * menu_factor) ** 2) * 1000) / 1000


# ============================================================================================================
# Events
# ============================================================================================================

# Ready
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Activity(type=discord.ActivityType.watching, name="for $help")
                                 )
    print("Ready!")
    # print(get_visit_rate(807386600337440839))


@client.event
@commands.has_permissions(send_messages=True)
async def on_guild_join(guild):
    if guild.system_channel:
        embed = discord.Embed(
            color=discord.Color(color_embed),
            title='Restaurant Tycoon Invited!',
            description="Thanks for inviting me to your server!",
            timestamp=datetime.datetime.now()
        )

        embed.set_author(name="Copy-Bot")
        embed.set_thumbnail(url="https://github.com/Brocoliman/TheBrocolimanDing/blob/master/copy-bot.png?raw=true")
        await guild.system_channel.send(embed=embed)


@client.event
async def on_command_error(ctx, err):
    if type(err) == discord.ext.commands.errors.CommandOnCooldown and ctx.command.name == 'work':
        await ctx.send(embed=make_embed(
            ctx, 'Restaurant Work',
            f":warning: | Work is on cooldown! You can work the next day in **{err.args[0][34:]}**.",
            color=color_error
        ))


# ============================================================================================================
# Commands
# ============================================================================================================


@client.command(aliases=['c'])
async def create(ctx, *name):
    with open('data.json', 'r') as r_file:  # make sure the user doesn't already have a restaurant
        dt = json.load(r_file)
        try:
            dt[str(ctx.author.id)]
        except KeyError:
            pass
        else:
            await ctx.send(embed=make_embed(
                ctx, 'Create Restaurant',
                ":warning: | You already have a restaurant. "
                f"To see your restaurant, use `{prefix}r`, `{prefix}restr`, or `{prefix}restaurant`.",
                color=color_error
            ))
            return

    if len(name) == 0:  # make sure restaurant has a name
        await ctx.send(embed=make_embed(
            ctx, 'Create Restaurant',
            ":warning: | Please enter a restaurant name.",
            color=color_error
        ))
        return

    if len(ctx.message.attachments) == 0:  # make sure the user has uploaded an image for the icon
        await ctx.send(embed=make_embed(
            ctx, 'Create Restaurant',
            ":warning: | Please upload an image representing your restaurant icon.",
            color=color_error
        ))
        return

    restaurant = {
        'name': ' '.join(name),
        'owner': ctx.author.name + '#' + ctx.author.discriminator,
        'menu': {
            "Water": {
                "category": "drink",
                "price": 0,
                "components": "water"
            }
        },
        'level': 0,
        'exp': 0,
        'created_at': str(ctx.message.created_at).split(' ')[0],
        'cash': 0,
        'inv': ['prep/mix_counter', 'stove', 'pan'],
        'icon': ctx.message.attachments[0].proxy_url,
        'stars': 3,
        'location': 'village',
        'day': 0,
    }

    data.update({str(ctx.author.id): restaurant})
    await update_data()

    await ctx.send(embed=make_embed(
        ctx, 'Create Restaurant',
        f":white_check_mark: | Success! Your restaurant **{' '.join(name)}** has been created. "
        f"To view it, use the command `{prefix}r`, `{prefix}restr`, or `{prefix}restaurant`.",
        color=color_success, thumb=restaurant['icon']
    ))


@client.command(aliases=['r', 'restr'])
async def restaurant(ctx, command=None, *command_arg):
    try:
        restaurant_data = data[str(ctx.author.id)]
    except KeyError:
        await ctx.send(embed=make_embed(
            ctx, 'Restaurant Information',
            f":warning: | You do not have a restaurant yet. To make a restaurant, use `{prefix}create`.",
            color=color_error
        ))
        return

    if command is None or command == 'view':
        embed = make_embed(ctx, 'Restaurant Information', ":star:" * restaurant_data['stars'],
                           color=color_embed, thumb=restaurant_data['icon'])

        menu_display = ''
        if len(restaurant_data['menu']) == 0:
            menu_display = 'No items'
        else:
            for item in restaurant_data['menu']:
                menu_display += f"{item} - ${restaurant_data['menu'][item]['price']}\n"

        inv_display = '\n'.join(restaurant_data['inv'])
        if len(restaurant_data['inv']) == 0:
            inv_display = 'No items'

        embed.add_field(name='Restaurant Name', value=restaurant_data['name'], inline=False)
        embed.add_field(name='Owner', value=restaurant_data['owner'], inline=False)
        embed.add_field(name='Level', value=str(restaurant_data['level']), inline=True)
        embed.add_field(name='XP', value=str(restaurant_data['exp']), inline=True)
        embed.add_field(name='Day', value=str(restaurant_data['day']), inline=True)
        embed.add_field(name='Cash', value='$' + str(restaurant_data['cash']), inline=False)
        embed.add_field(name='Location', value=str(restaurant_data['location']), inline=False)
        embed.add_field(name='Inventory', value=inv_display, inline=False)
        embed.add_field(name='Menu', value=menu_display, inline=False)
        embed.add_field(name='Created At', value=restaurant_data['created_at'], inline=False)

        await ctx.send(embed=embed)

    elif command == 'delete':
        await ctx.send(embed=make_embed(
            ctx, 'Delete Restaurant',
            f":question: | Are you sure you want to delete your restaurant? This cannot be undone. "
            f"Please enter your restaurant name exactly to confirm deletion:",
            color=color_embed, thumb=data[str(ctx.author.id)]['icon']
        ))

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        try:
            msg = await client.wait_for('message', timeout=15.0, check=check)
        except:  # user has not confirmed deletion in time
            await ctx.send(embed=make_embed(
                ctx, 'Delete Restaurant',
                f":warning: | Timeout. Deletion aborted.",
                color=color_error, thumb=data[str(ctx.author.id)]['icon']
            ))
        else:
            if msg.content == data[str(ctx.author.id)]['name']:  # confirm deletion
                await ctx.send(embed=make_embed(
                    ctx, 'Delete Restaurant',
                    f":white_check_mark: | Restaurant has been deleted.",
                    color=color_success, thumb=data[str(ctx.author.id)]['icon']
                ))
                data.pop(str(ctx.author.id))
                await update_data()
            else:  # abort deletion
                await ctx.send(embed=make_embed(
                    ctx, 'Delete Restaurant',
                    f":warning: | Deletion aborted.",
                    color=color_error, thumb=data[str(ctx.author.id)]['icon']
                ))

    elif command == 'name':
        if not command_arg:
            await ctx.send(embed=make_embed(
                ctx, 'Rename Restaurant',
                f":warning: | Please enter a new name for the restaurant",
                color=color_error, thumb=data[str(ctx.author.id)]['icon']
            ))
        else:
            new_name = ' '.join(command_arg)
            await ctx.send(embed=make_embed(
                ctx, 'Rename Restaurant',
                f":white_check_mark: | Success! Your restaurant has been renamed from "
                f"**{data[str(ctx.author.id)]['name']}** to **{new_name}**",
                color=color_success, thumb=data[str(ctx.author.id)]['icon']
            ))
            data[str(ctx.author.id)]['name'] = new_name
            await update_data()

    elif command == 'icon':
        if not ctx.message.attachments:
            await ctx.send(embed=make_embed(
                ctx, 'Change Restaurant Icon',
                f":warning: | Please upload a new icon for the restaurant",
                color=color_error, thumb=data[str(ctx.author.id)]['icon']
            ))
        else:
            new_icon_url = ctx.message.attachments[0].proxy_url
            await ctx.send(embed=make_embed(
                ctx, 'Rename Restaurant',
                f":white_check_mark: | Success! Your restaurant's icon has been changed to:",
                color=color_success, img=new_icon_url, thumb=data[str(ctx.author.id)]['icon']
            ))
            data[str(ctx.author.id)]['icon'] = new_icon_url
            await update_data()


@client.command(aliases=['m'])
async def menu(ctx, command=None, *command_arg):
    try:
        data[str(ctx.author.id)]
    except KeyError:
        await ctx.send(embed=make_embed(
            ctx, 'Restaurant Information',
            f":warning: | You do not have a restaurant yet. To make a restaurant, use `{prefix}create`",
            color=color_error
        ))
        return

    if command is None or command == 'view':  # view menu
        appetizer_display = ''
        entree_display = ''
        dessert_display = ''
        drink_display = ''
        if len(data[str(ctx.author.id)]['menu']) == 0:
            await ctx.send(embed=make_embed(
                ctx, 'Menu',
                f"This is the menu for **{data[str(ctx.author.id)]['name']}**:\nNo items in menu",
                color=color_embed, thumb=data[str(ctx.author.id)]['icon']
            ))
        else:
            await ctx.send(embed=make_embed(
                ctx, 'Menu',
                f"This is the menu for **{data[str(ctx.author.id)]['name']}**:",
                color=color_embed, thumb=data[str(ctx.author.id)]['icon']
            ))

            for item in data[str(ctx.author.id)]['menu']:
                if data[str(ctx.author.id)]['menu'][item]['category'] == 'appetizer':
                    appetizer_display += f"**{item} - ${data[str(ctx.author.id)]['menu'][item]['price']}**\n" \
                                         f"{components_delayered_lower[data[str(ctx.author.id)]['menu'][item]['components']]['name']}\n"
                if data[str(ctx.author.id)]['menu'][item]['category'] == 'entree':
                    entree_display += f"**{item} - ${data[str(ctx.author.id)]['menu'][item]['price']}**\n" \
                                      f"{components_delayered_lower[data[str(ctx.author.id)]['menu'][item]['components']]['name']}\n"
                if data[str(ctx.author.id)]['menu'][item]['category'] == 'dessert':
                    dessert_display += f"**{item} - ${data[str(ctx.author.id)]['menu'][item]['price']}**\n" \
                                       f"{components_delayered_lower[data[str(ctx.author.id)]['menu'][item]['components']]['name']}\n"
                if data[str(ctx.author.id)]['menu'][item]['category'] == 'drink':
                    drink_display += f"**{item} - ${data[str(ctx.author.id)]['menu'][item]['price']}**\n" \
                                     f"{components_delayered_lower[data[str(ctx.author.id)]['menu'][item]['components']]['name']}\n"

            if appetizer_display:
                await ctx.send(embed=make_embed(
                    ctx, 'Appetizers', appetizer_display,
                    color=color_embed, thumb='', author=False, timestamp=False
                ))
            if entree_display:
                await ctx.send(embed=make_embed(
                    ctx, 'Entree', entree_display,
                    color=color_embed, thumb='', author=False, timestamp=False
                ))
            if dessert_display:
                await ctx.send(embed=make_embed(
                    ctx, 'Dessert', dessert_display,
                    color=color_embed, thumb='', author=False, timestamp=False
                ))
            if drink_display:
                await ctx.send(embed=make_embed(
                    ctx, 'Drink', drink_display,
                    color=color_embed, thumb='', author=False, timestamp=False
                ))

    elif command.lower() == 'add' or command.lower() == 'edit':
        try:
            item_name, item_category, item_price, item_component = command_arg

            while '_' in item_name:  # replace all underscores with spaces
                item_name = item_name.replace('_', ' ')

            item_category, item_component = item_category.lower(), item_component.lower()
            item_price = float(item_price)

            if item_category not in ('entree', 'appetizer', 'dessert', 'drink'):
                await ctx.send(embed=make_embed(
                    ctx, 'Menu Editing',
                    f":warning: | Item category must be either `appetizer`, `entree`, `dessert`, or `drink`.",
                    color=color_error, thumb=data[str(ctx.author.id)]['icon']
                ))
                return

            _ = components_delayered_lower[item_component]
        except ValueError:  # if user has not entered correct num of arguments or did not enter a number for the price
            await ctx.send(embed=make_embed(
                ctx, 'Menu Editing',
                f":warning: | Please enter the item name (whatever you wish, but spaced by underscores), "
                f"item's category (appetizer, entree, dessert, or drink), item price (a number without units), and "
                f"the item component (to see which available components there are, please do `{prefix}menu components`",
                color=color_error, thumb=data[str(ctx.author.id)]['icon']
            ))
            return
        except KeyError:  # component was not found
            await ctx.send(embed=make_embed(
                ctx, 'Menu Editing',
                f":warning: | Component `{item_component}` was not found. To see a list of the available components, do"
                f" `{prefix}menu components`",
                color=color_error, thumb=data[str(ctx.author.id)]['icon']
            ))
            return

        if item_category == 'drink':  # make sure items in the drink section are drinks
            try:
                components['drinks'][item_component]
            except KeyError:
                await ctx.send(embed=make_embed(
                    ctx, 'Menu Editing',
                    f":warning: | The item component must be a drink in order to be in the drink section of the menu",
                    color=color_error, thumb=data[str(ctx.author.id)]['icon']
                ))
                return

        if command.lower() == 'add':  # remove interchangeability between edit and add
            try:
                data[str(ctx.author.id)]['menu'][item_name]
            except KeyError:
                pass  # continue, no error
            else:
                await ctx.send(embed=make_embed(
                    ctx, 'Menu Editing',
                    f":warning: | Item `{item_name}` is already in your menu. To edit it, use `{prefix}menu edit` "
                    "instead.",
                    color=color_error, thumb=data[str(ctx.author.id)]['icon']
                ))
                return
        else:  # then it is 'edit
            try:
                data[str(ctx.author.id)]['menu'][item_name]
            except KeyError:
                await ctx.send(embed=make_embed(
                    ctx, 'Menu Editing',
                    f":warning: | Item `{item_name}` is not in your menu. To add it, use `{prefix}menu add`.",
                    color=color_error, thumb=data[str(ctx.author.id)]['icon']
                ))
                return
            else:
                pass  # continue, no error

        component = components_delayered_lower[item_component]
        for equipment in component['required']:
            if equipment not in data[str(ctx.author.id)]['inv']:
                await ctx.send(embed=make_embed(
                    ctx, 'Menu Editing',
                    f":warning: | You do not have the equipment required to make this component!\n"
                    f"The component needs [{', '.join(('`' + shop_items[item]['name'] + '`') for item in component['required'])}]\n"
                    f"You have [{', '.join([('`' + shop_items[item]['name'] + '`') for item in data[str(ctx.author.id)]['inv']])}]",
                    color=color_error, thumb=data[str(ctx.author.id)]['icon']
                ))
                return

        await ctx.send(embed=make_embed(
            ctx, 'Menu Editing',
            f":white_check_mark: | You have added item `{item_name}` with a price tag of `${item_price}` to your "
            f"**{item_category}** menu!",
            color=color_success, thumb=data[str(ctx.author.id)]['icon']
        ))

        data[str(ctx.author.id)]['menu'].update(
            {item_name: {'category': item_category, 'price': item_price, 'components': item_component}}
        )

        await update_data()

    elif command.lower() == 'remove':
        if command_arg:
            item_remove = ' '.join(command_arg)
        else:
            await ctx.send(embed=make_embed(
                ctx, 'Menu Editing',
                f":warning: | Please enter the name of the item from your menu to remove.",
                color=color_error
            ))
            return

        try:
            data[str(ctx.author.id)]['menu'].pop(item_remove)
            await update_data()
            await ctx.send(embed=make_embed(
                ctx, 'Menu Editing',
                f":white_check_mark: | Item `{item_remove}` was removed from your menu.",
                color=color_success
            ))
        except KeyError:  # item does not exist in menu
            await ctx.send(embed=make_embed(
                ctx, 'Menu Editing',
                f":warning: | Item `{item_remove}` does not exist in your menu.",
                color=color_error
            ))

    elif command.lower() == 'components':
        if command_arg:  # specific component
            component_name = command_arg[0].lower()
            try:
                component_data = components_delayered_lower[component_name]
            except KeyError:  # no such component
                await ctx.send(embed=make_embed(
                    ctx, 'Menu Components',
                    f":warning: | Requested component `{component_name}` does not exist. To check available components, "
                    f"do `{prefix}menu components`.",
                    color=color_error
                ))
                return
            embed = make_embed(
                ctx, f'Menu Component: {component_data["name"]}',
                f"This is information for the component {component_data['name']}",
                color=color_embed, thumb=data[str(ctx.author.id)]['icon']
            )
            embed.add_field(name='Cuisine', value=component_data['cuisine'][0].upper()+component_data['cuisine'][1:],
                            inline=False)
            embed.add_field(name='Serving Size', value=str(component_data['size'])+'oz')
            embed.add_field(name='Supply Cost', value="$"+str(component_data['supply']))
            embed.add_field(name='Service Cost', value="$"+str(component_data['service']))
            embed.add_field(name='Required Equipment', value=', '.join([f"`{i}`" for i in component_data['required']]))
            embed.add_field(name='Reference Name', value=f"`{component_name}`")

            await ctx.send(embed=embed)
        else:  # no specific component, show all
            components_display = ''
            for category in components:
                components_display += "__**" + category[0].upper() + category[1:] + '**__\n'
                for component_key in components[category]:
                    component = components[category][component_key]
                    makeable = True
                    for equipment in component['required']:
                        if equipment not in data[str(ctx.author.id)]['inv']:
                            makeable = False
                            break
                    if makeable:
                        components_display += \
                            f"**{component['name']}** {component['size']}oz, reference name: `{component_key}`\n"
                    else:
                        components_display += \
                            f":lock: **{component['name']}** {component['size']}oz, reference name: `{component_key}`\n"
            await ctx.send(embed=make_embed(
                ctx, 'Menu Components',
                f"This is a list of components/dishes you can use in your menu.\nUse the reference name as the reference to "
                f"the component when adding or editing a dish in your menu.\n{components_display}",
                color=color_embed, thumb=data[str(ctx.author.id)]['icon']
            ))


@client.command(aliases=['w'])
@commands.cooldown(rate=1, per=60 * cld_time, type=commands.BucketType.user)
async def work(ctx):
    try:
        data[str(ctx.author.id)]
    except KeyError:
        await ctx.send(embed=make_embed(
            ctx, 'Restaurant Work',
            f":warning: | You do not have a restaurant yet. To make a restaurant, use `{prefix}create`",
            color=color_error
        ))
        return

    r_data = data[str(ctx.author.id)]
    location_range_start, location_range_end = locations[r_data['location']]['customer_range']

    total = random.randint(location_range_start, location_range_end + 1)
    rate = get_visit_rate(ctx.author.id)

    earn = 0
    for customer in range(int(total * rate)):
        if len(r_data['menu']) >= 2:
            rand_menu_items = random.sample(list(r_data['menu']), 2)
        else:
            rand_menu_items = [list(r_data['menu'].keys())[0]]
        for item in rand_menu_items:  # no bias yet
            name = r_data['menu'][item]['components']
            component_info = components_delayered_lower[name]
            earn += r_data['menu'][item]['price'] - (component_info['supply'] + component_info['service'])

    data[str(ctx.author.id)]['day'] += 1
    data[str(ctx.author.id)]['cash'] += earn

    await ctx.send(embed=make_embed(
        ctx, 'Restaurant Work',
        f"You worked **Day {r_data['day']}** and got a total of **${earn}** from **{int(total * rate)} customers**",
        color=color_embed, thumb=data[str(ctx.author.id)]['icon']
    ))

    await update_data()


@client.command()
async def shop(ctx, command=None, *command_arg):
    if command == 'buy':
        try:
            data[str(ctx.author.id)]
        except KeyError:
            await ctx.send(embed=make_embed(
                ctx, 'Shop',
                f":warning: | You do not have a restaurant yet. To make a restaurant, use `{prefix}create`",
                color=color_error
            ))
            return

        if len(command_arg) < 0:
            await ctx.send(embed=make_embed(
                ctx, 'Shop',
                f":warning: | You must enter an item to buy",
                color=color_error
            ))
            return

        item_name = command_arg[0]

        try:
            price = shop_items[item_name]['price']
            r_data = data[str(ctx.author.id)]
            if item_name in r_data['inv']:
                await ctx.send(embed=make_embed(
                    ctx, 'Shop',
                    f":warning: | You already have this item",
                    color=color_error
                ))
                return
            if r_data['cash'] >= price:
                r_data['inv'].append(item_name)
                r_data['cash'] -= price
                data[str(ctx.author.id)] = r_data
                await update_data()
                await ctx.send(embed=make_embed(
                    ctx, 'Shop',
                    f":white_check_mark: | You bought the `{item_name}` for **${price}**.",
                    color=color_success
                ))
            else:  # user cannot afford
                await ctx.send(embed=make_embed(
                    ctx, 'Shop',
                    f":warning: | You cannot afford `{item_name}`. It costs **${price}** and you have "
                    f"**${r_data['cash']}**",
                    color=color_error
                ))
        except KeyError:  # requested item does not exist
            await ctx.send(embed=make_embed(
                ctx, 'Shop',
                f":warning: | Requested item `{item_name}` does not exist. To check available items from the shop, do"
                f"`{prefix}shop view`.",
                color=color_error
            ))

    elif command == 'view' or command is None:
        items_display = ''
        for item in shop_items:
            items_display += f"**{shop_items[item]['name']}** - **${shop_items[item]['price']}**: " \
                             f"{shop_items[item]['desc']}; reference name - `{item}`\n"
        await ctx.send(
            embed=make_embed(ctx, 'Shop', f'Here are the items in the shop.\n{items_display}', color=color_embed)
        )


@client.command()
async def invite(ctx):
    embed = make_embed(
        ctx, 'Invite Restaurant Tycoon',
        "These are the links I associate with:",
        color=color_embed
    )

    embed.add_field(name="Invite me to your server",
                    value="[Invite](https://discord.com/api/oauth2/authorize?client_id=830503329305067541&"
                          "permissions=34360125504&scope=bot)",
                    inline=False)
    embed.add_field(name="Brocolimanx's Hangout (also where the bot's updates are)",
                    value="[Server Link](" + DISCORD_LINK + ")", inline=False)

    await ctx.send(embed=embed)


@client.command()
async def help(ctx, spec=None):
    if not spec:
        desc = ''
        for command in cmd:
            desc += f"\n**{prefix}{command}** - {cmd[command]['desc']}; **{len(cmd[command]['subcommands'])}**" \
                    f" subcommands"
        await ctx.send(embed=make_embed(
            ctx, 'Restaurant Tycoon Commands',
            f"Here are all the commands: {desc}",
            color=color_embed
        ))
        return

    try:
        subcommands = ''
        if cmd[spec]['subcommands']:
            subcommands += 'Subcommands:\n'
            for subcmd in cmd[spec]['subcommands']:
                subcommands += f" - **{prefix}{spec} {subcmd}** - {cmd[spec]['subcommands'][subcmd]['desc']}\n" \
                               f"   ```Arguments: {cmd[spec]['subcommands'][subcmd]['arguments']}```"
        await ctx.send(embed=make_embed(
            ctx, f'Restaurant Tycoon Command: ${spec}',
            f"{cmd[spec]['desc']}\n```Arguments: {cmd[spec]['arguments']}``````Aliases: {cmd[spec]['aliases']}```"
            f"\n{subcommands}",
            color=color_embed
        ))
    except KeyError:  # specified command doesn't exist
        await ctx.send(embed=make_embed(
            ctx, 'Restaurant Tycoon Commands',
            f":warning: | Command `{prefix}{spec}` does not exist. For a list of commands, do `{prefix}help`",
            color=color_error
        ))


client.run(f'{TOKEN}')
