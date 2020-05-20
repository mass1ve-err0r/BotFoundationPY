import asyncio
from requests import get
from datetime import datetime
from discord import Embed, Colour, TextChannel
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Fun(bot))
