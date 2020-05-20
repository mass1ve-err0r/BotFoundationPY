from os import environ
from datetime import datetime
from discord import Embed, Colour, NotFound
from discord.ext import commands
from discord.utils import get
from Utilities.DatabaseHandler import DatabaseHandler

serverLogsID = int(environ.get('LEVEL2'))
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

        try:
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
                    return
        except NotFound:
            return

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author == self.bot.user:
            return

        serverLogsChannel = self.bot.get_channel(serverLogsID)
        uUser = before.author.display_name + " (<@" + str(before.author.id) + ">)"
        uAvatar = before.author.avatar_url_as(static_format='jpeg')
        msg_old = before.content if len(before.content) > 0 else "<empty_message>"
        msg_new = after.content if len(after.content) > 0 else "<empty_message>"
        msg_cnl = "<#" + str(before.channel.id) + ">"
        dt = datetime.now()

        embedx = Embed(title="Message Edited", colour=Colour(0x4A90E2), timestamp=dt)
        embedx.set_thumbnail(url=uAvatar)
        embedx.set_footer(text="Prototype X1")
        embedx.add_field(name="Member", value=uUser, inline=False)
        embedx.add_field(name="Original Message", value=msg_old, inline=False)
        embedx.add_field(name="New Message", value=msg_new, inline=False)
        if len(before.attachments) != 0:
            item = before.attachments[0].url
            embedx.add_field(name="Image URL", value=item, inline=False)
        embedx.add_field(name="Channel", value=msg_cnl, inline=False)

        await serverLogsChannel.send(embed=embedx)
        await self.on_message(after)

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
