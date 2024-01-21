import discord
from discord.ext import commands

class Marble_Racing(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def amr_help(self, ctx, section):
        if section == "basics":
            await ctx.send(
                "https://www.youtube.com/watch?v=Lzq1aDCPBDA&list=PLLg3NKj4Z9HdvgTgFUJRF0PJ-N-x-tFtX&index=1")
        elif section == "marble" or section == "marbl" or section == "mb" or section == "mrb":
            await ctx.send(
                "https://www.youtube.com/watch?v=WBdyIEGLbqk&list=PLLg3NKj4Z9HdvgTgFUJRF0PJ-N-x-tFtX&index=2")
        elif section == "track":
            await ctx.send(
                "https://www.youtube.com/watch?v=vXpOsWWgig0&list=PLLg3NKj4Z9HdvgTgFUJRF0PJ-N-x-tFtX&index=3")
        elif section == "spinner":
            await ctx.send(
                "https://www.youtube.com/watch?v=Gw3JuecinMM&list=PLLg3NKj4Z9HdvgTgFUJRF0PJ-N-x-tFtX&index=4")
        elif section == "text":
            await ctx.send(
                "https://www.youtube.com/watch?v=FHPaZxF9Fmo&list=PLLg3NKj4Z9HdvgTgFUJRF0PJ-N-x-tFtX&index=5")
        elif section == "conveyor":
            await ctx.send(
                "https://www.youtube.com/watch?v=Qq4OuhI2IwY&list=PLLg3NKj4Z9HdvgTgFUJRF0PJ-N-x-tFtX&index=6")
        elif section == "import" or section == "sprites":
            await ctx.send(
                "https://www.youtube.com/watch?v=Oy3m5XSj1ac&list=PLLg3NKj4Z9HdvgTgFUJRF0PJ-N-x-tFtX&index=7")
        elif section == "bounce" or section == "trampoline":
            await ctx.send(
                "https://www.youtube.com/watch?v=h55kH9uol5Q&list=PLLg3NKj4Z9HdvgTgFUJRF0PJ-N-x-tFtX&index=8")
        elif section == "controller" or section == "mixer" or section == "starter":
            await ctx.send(
                "https://www.youtube.com/watch?v=dO6UE7_NUwQ&list=PLLg3NKj4Z9HdvgTgFUJRF0PJ-N-x-tFtX&index=9")
        elif section == "pump" or section == "piston":
            await ctx.send(
                "https://www.youtube.com/watch?v=VsUTp6xYKVw&list=PLLg3NKj4Z9HdvgTgFUJRF0PJ-N-x-tFtX&index=10")
        elif section == "example" or section == "simple":
            await ctx.send(
                "https://www.youtube.com/watch?v=pWsLZxsOCDk&list=PLLg3NKj4Z9HdvgTgFUJRF0PJ-N-x-tFtX&index=11")
        elif section == "snake":
            await ctx.send(
                "https://www.youtube.com/watch?v=ssKlEzu5zwQ&list=PLLg3NKj4Z9HdvgTgFUJRF0PJ-N-x-tFtX&index=12")
        elif section == "elevator" or section == "elev":
            await ctx.send(
                "https://www.youtube.com/watch?v=5kNMgVIhZlA&list=PLLg3NKj4Z9HdvgTgFUJRF0PJ-N-x-tFtX&index=13")
        elif section == "teleporter" or section == "transporter" or section == "tele":
            await ctx.send(
                "https://www.youtube.com/watch?v=2BoabgTzCVE&list=PLLg3NKj4Z9HdvgTgFUJRF0PJ-N-x-tFtX&index=14")
        elif section == "gravity" or section == "grav" or section == "gravity pad":
            await ctx.send(
                "https://www.youtube.com/watch?v=ED_wDVSZB-g&list=PLLg3NKj4Z9HdvgTgFUJRF0PJ-N-x-tFtX&index=15")
        elif section == "velocity" or section == "vel" or section == "velocity pad":
            await ctx.send(
                "https://www.youtube.com/watch?v=lIjaVk9iUVY&list=PLLg3NKj4Z9HdvgTgFUJRF0PJ-N-x-tFtX&index=16")
        elif section == "script" or section == "scripting":
            await ctx.send("https://docs.google.com/document/d/17_CPg-QtU3qWp4Q7eD2csOWNFZ4QiGXfBZmCOxFmy4M")

    @commands.command()
    async def broc_disc(self, ctx):
        await ctx.send("Brocolimanx's Discord Hangout: https://discord.com/invite/K9cKGGY")

    @commands.command()
    async def broc_yt(self, ctx):
        await ctx.send(
            "Brocolimanx's Youtube Channel: https://www.youtube.com/channel/UCxleSqkNgg8lUecJfDFjhGQ?sub_confirmation=1")

    @commands.command()
    async def marble_racers(self, ctx):
        res1 = "You can suggest racers to this list in #suggestions on my server; it is best if they have good aesthetics \n This list includes the best marble racers I think(based on scripting skills: \n 1. Doc671 \n 2. Max Marble \n 3. Woodsie \n 4. Black Cat Gear \n 5. Crazy Marble Race \n "
        res2 = "6. Kenlimepie \n 7. Algorox \n 8. Carson Jay \n This list includes the best marble racers I think(based on design: \n 1. Max Marble \n 2. Doc671 \n 3. Black Cat Gear \n 4. Kenlimepie \n "
        res3 = " 5. Algorox \n 6. Woodsie \n 7. Crazy Marble Race \n 8. Carson Jay \n If you have a lower ranking, this does not mean I am criticizing you in any way; there are many racers who aren't even on the list! \n"
        res = res1 + res2 + res3
        await ctx.send(res)


def setup(client):
    client.add_cog(Marble_Racing(client))