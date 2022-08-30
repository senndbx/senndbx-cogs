import aiohttp
import discord
from random import randint
from redbot.core import commands, checks, bank, errors, commands
from azurlane.azurapi import AzurAPI

defaultPayout = 100
api = AzurAPI()

class Rabotcogs(commands.Cog):
    """Rabi Rabot cogs here."""

    def __init__(self, ctx):
        # self.bot = bot
        self.ctx = ctx

    # @commands.command()
    # @checks.mod_or_permissions(administrator=True)
    # async def asdf(self, ctx: commands.Context):
    #     credits_name = await bank.get_currency_name(ctx.guild)
    #     await ctx.send("{}".format(credits_name))

    @commands.command()
    @checks.mod_or_permissions(administrator=True)
    @commands.bot_has_permissions(embed_links=True)
    async def boatinfo(self, ctx: commands.Context, shipName):
        obj = api.getShip(ship=shipName)
        await ctx.send("`{}`".format(obj))

        
    @commands.command(pass_context=True)
    async def dubs(self, ctx: commands.Context):
        """Imageboard-style RNG. Try for repeating digits on the end"""
        author = ctx.message.author
        payout = defaultPayout
        dub = randint(100000000, 500000000)
        if repr(dub)[-1] == repr(dub)[-2]:
            await ctx.send("{} check em: `>>{}`".format(author.mention, dub))
            dubsholder = repr(dub)[-1] + repr(dub)[-2]
            payout = int(dubsholder)
            if dubsholder == "00":
                payout = defaultPayout
            if dubsholder == "77":
                payout = defaultPayout
            try:
                await bank.deposit_credits(author, payout)
            except errors.BalanceTooHigh as e:
                await bank.set_balance(author, e.max_balance)
            await ctx.send("Congratulations! You scored a repeating digits! You have received {num} {currency}.".format(num= payout, currency= await bank.get_currency_name(ctx.guild)))
        else:
            await ctx.send("{mention}, check em: `>>{digits}`".format(mention= author.nick, digits= dub))

    @commands.command(pass_context=True)
    @checks.mod_or_permissions(administrator=True)
    async def rigdubs(self, ctx: commands.Context):
        """Rigged gets only for testing purpose"""
        author = ctx.message.author
        dub = randint(10000000, 50000000)
        result = repr(dub) + repr(dub)[-1]
        await ctx.send("This is only for testing purpose.")
        await ctx.send("{}".format(result))