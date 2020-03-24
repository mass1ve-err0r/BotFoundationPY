from os import environ
from re import match
from discord import NotFound
from discord.ext import commands

reportChannelID = int(environ.get('LEVEL0'))
modID = int(environ.get('ROLE0'))


class OptionalFilters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.isSpoilerFiltered = False
        self.isCapsLockFiltered = False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        try:
            if self.isSpoilerFiltered is True:
                if match("(.*)\|\|(.*)\|\|(.*)", message.content):
                    await message.delete()
                    return

            if self.isCapsLockFiltered is True:
                if len(message.content) > 5:
                    if message.content.replace(" ", "").isupper():
                        await message.delete()
                        return
        except NotFound:
            return

    @commands.command(name='ofspoilers')
    @commands.has_role('Moderators')
    @commands.guild_only()
    async def ofspoilers(self, ctx, really: int = -1):
        if really == 1:
            if self.isSpoilerFiltered is True:
                await ctx.send("Spoiler filtering is already enabled!")
                return
            else:
                self.isSpoilerFiltered = True
                await ctx.send("Enabled Spoiler filtering!")
                return
        elif really == 0:
            if self.isSpoilerFiltered is False:
                await ctx.send("Spoiler filtering is already disabled!")
                return
            else:
                self.isSpoilerFiltered = False
                await ctx.send("Disabled Spoiler filtering!")
                return
        else:
            await ctx.send("Did not supply valid number (1 / 0), not changing status.\n(isSpoilerFiltered:" + str(self.isSpoilerFiltered) + ")")
            return

    @commands.command(name='ofcapslock')
    @commands.has_role('Moderators')
    @commands.guild_only()
    async def ofcapslock(self, ctx, really: int = -1):
        if really == 1:
            if self.isCapsLockFiltered is True:
                await ctx.send("Caps-Lock filtering is already enabled!")
                return
            else:
                self.isCapsLockFiltered = True
                await ctx.send("Enabled Caps-Lock filtering!")
                return
        elif really == 0:
            if self.isCapsLockFiltered is False:
                await ctx.send("Caps-Lock filtering is already disabled!")
                return
            else:
                self.isCapsLockFiltered = False
                await ctx.send("Disabled Caps-Lock filtering!")
                return
        else:
            await ctx.send("Did not supply valid number (1 / 0), not changing status.\n(isCapsLockFiltered:" + str(self.isCapsLockFiltered) + ")")
            return


def setup(bot):
    bot.add_cog(OptionalFilters(bot))
