import os
from datetime import datetime
from discord import Member, Embed, Colour, NotFound
from discord.ext import commands
from discord.utils import get

reportChannelID = int(os.environ.get('LEVEL0'))
modID = int(os.environ.get('ROLE0'))


class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def getAntiSpamEmbed(self, member: Member, channelString):
        dt = datetime.now()
        uUser = member.display_name + " (<@" + str(member.id) + ">)"
        uAvatar = member.avatar_url_as(static_format='jpeg')

        embedx = Embed(title="Member Report (SPAM)", colour=Colour(0x8B572A), timestamp=dt)
        embedx.set_thumbnail(url=uAvatar)
        embedx.set_footer(text="Prototype X1")
        embedx.add_field(name="Member", value=uUser, inline=False)
        embedx.add_field(name="Channel", value=channelString, inline=False)

        return embedx

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        targetChannel = message.channel
        previousMessage = None
        async for oldMessage in targetChannel.history(limit=3):
            previousMessage = oldMessage

        if not message.clean_content or not previousMessage.clean_content:
            return

        try:
            if previousMessage is not None and \
                    previousMessage.author.display_name == message.author.display_name and \
                    previousMessage.clean_content == message.clean_content:

                embedx = await self.getAntiSpamEmbed(message.author, message.channel.mention)
                targetCH = self.bot.get_channel(reportChannelID)
                pingMods = get(message.guild.roles, id=modID).mention

                await message.delete()
                await targetCH.send(pingMods)
                await targetCH.send(embed=embedx)
        except NotFound:
            return


def setup(bot):
    bot.add_cog(AntiSpam(bot))
