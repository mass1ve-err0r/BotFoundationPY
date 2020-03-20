from os import environ
from re import match
from datetime import datetime
from discord import Embed, Colour
from discord.ext import commands
from discord.utils import get
from Utilities.DatabaseHandler import DatabaseHandler

reportChannelID = int(environ.get('LEVEL0'))
modID = int(environ.get('ROLE0'))


class Filter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.filtered_words = []
        self.dbHandler = DatabaseHandler()
        dList = self.dbHandler.getAllBadWordsSYNC()
        for entry in dList:
            self.filtered_words.append(entry['badword'])

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        for bad_word in self.filtered_words:
            if bad_word in message.content.lower().replace(" ", ""):
                dt = datetime.now()
                uUser = message.author.display_name + " (<@" + str(message.author.id) + ">)"
                uAvatar = message.author.avatar_url_as(static_format='jpeg')
                bad_channel = message.channel.mention
                orig_msg = message.content
                targetCH = self.bot.get_channel(reportChannelID)
                pingMods = get(message.guild.roles, id=modID).mention

                await message.delete()

                embedx = Embed(title="Member Report (Bad Word)", colour=Colour(0x8B572A), timestamp=dt)
                embedx.set_thumbnail(url=uAvatar)
                embedx.set_footer(text="Prototype X1")
                embedx.add_field(name="Member", value=uUser, inline=False)
                embedx.add_field(name="Word", value=bad_word, inline=False)
                embedx.add_field(name="Original Message", value=orig_msg, inline=False)
                embedx.add_field(name="Channel", value=bad_channel, inline=False)

                await targetCH.send(pingMods)
                await targetCH.send(embed=embedx)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if match("(.*)\|\|(.*)\|\|(.*)", message.content):
            await message.delete()
            return

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if len(message.content) > 5:
            if match("^[A-Z\s]+$", message.content):
                await message.delete()
                return

    @commands.command(name="reloadFilter")
    @commands.has_role('Moderators')
    @commands.guild_only()
    async def reloadFilter(self, ctx, really: int = 0):
        if really == 1:
            self.filtered_words = []
            dList = await self.dbHandler.getAllBadWords()
            for entry in dList:
                self.filtered_words.append(entry['badword'])
            await ctx.send("Reloaded Filter!")
            return
        else:
            await ctx.send("Command not executed (Missing or faulty param)")
            return


def setup(bot):
    bot.add_cog(Filter(bot))
