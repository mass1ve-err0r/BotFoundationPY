from discord.ext import commands
from re import match


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot




def setup(bot):
    bot.add_cog(Test(bot))
