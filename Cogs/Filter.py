import re
from datetime import datetime
from discord import Embed, Colour
from discord.ext import commands
from Utilities.DatabaseHandler import DatabaseHandler


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

        if re.match("(.*)\|\|(.*)\|\|(.*)", message.content):
            await message.delete()
            return

        for bad_word in self.filtered_words:
            if bad_word in message.content.lower().replace(" ", ""):
                dt = datetime.now()
                uUser = message.author.display_name + " (<@" + str(message.author.id) + ">)"
                uAvatar = message.author.avatar_url
                bad_channel = message.channel.name
                targetCH = message.channel

                await message.delete()

                embedx = Embed(title="Member Report (Bad Word)", colour=Colour(0x417505), timestamp=dt)
                embedx.set_thumbnail(url=uAvatar)
                embedx.set_footer(text="r/Jailbreak Bot")
                embedx.add_field(name="Member", value=uUser, inline=False)
                embedx.add_field(name="Word", value=bad_word, inline=False)
                embedx.add_field(name="Channel", value=bad_channel, inline=False)

                await targetCH.send(embed=embedx)

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