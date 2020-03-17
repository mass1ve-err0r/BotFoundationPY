import discord
from discord.ext import commands
from Utilities.DatabaseHandler import DatabaseHandler


class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Logger(bot))