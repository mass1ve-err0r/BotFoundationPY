import os
from datetime import datetime
from discord import Embed, Colour
from discord.ext import commands

serverLogsID = int(os.environ.get('LEVEL2'))


class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.bot.user:
            return

        serverLogsChannel = self.bot.get_channel(serverLogsID)
        uUser = message.author.display_name + " (<@" + str(message.author.id) + ">)"
        uAvatar = message.author.avatar_url_as(static_format='jpeg')
        msg_old = message.content if len(message.content) > 0 else "<empty_message>"
        dt = datetime.now()
        msg_cnl = "<#" + str(message.channel.id) + ">"

        embedx = Embed(title="Message Deleted", colour=Colour(0xD0021B), timestamp=dt)
        embedx.set_thumbnail(url=uAvatar)
        embedx.set_footer(text="Prototype X1")
        embedx.add_field(name="Member", value=uUser, inline=False)
        embedx.add_field(name="Message", value=msg_old, inline=False)
        if len(message.attachments) != 0:
            item = message.attachments[0].url
            embedx.add_field(name="Image URL", value=item, inline=False)
        embedx.add_field(name="Channel", value=msg_cnl, inline=False)

        await serverLogsChannel.send(embed=embedx)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        serverLogsChannel = self.bot.get_channel(serverLogsID)
        uUser = member.display_name + " (<@" + str(member.id) + ">)"
        uUserDate = member.created_at.strftime("%d/%m/%Y at %H:%M:%S")
        uAvatar = member.avatar_url_as(static_format='jpeg')
        dt = datetime.now()

        embedx = Embed(title="Member Joined", colour=Colour(0x40E412), timestamp=dt)
        embedx.set_thumbnail(url=uAvatar)
        embedx.set_footer(text="Prototype X1")
        embedx.add_field(name="Member", value=uUser, inline=False)
        embedx.add_field(name="Account creation date", value=uUserDate, inline=False)

        await serverLogsChannel.send(embed=embedx)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        serverLogsChannel = self.bot.get_channel(serverLogsID)
        uUser = member.display_name + " (<@" + str(member.id) + ">)"
        uUserDate = member.created_at.strftime("%d/%m/%Y at %H:%M:%S")
        uAvatar = member.avatar_url_as(static_format='jpeg')
        dt = datetime.now()

        embedx = Embed(title="Member Left", colour=Colour(0x9013FE), timestamp=dt)
        embedx.set_thumbnail(url=uAvatar)
        embedx.set_footer(text="Prototype X1")
        embedx.add_field(name="Member", value=uUser, inline=False)
        embedx.add_field(name="Account creation date", value=uUserDate, inline=False)

        await serverLogsChannel.send(embed=embedx)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        serverLogsChannel = self.bot.get_channel(serverLogsID)
        uUser = before.display_name + " (<@" + str(before.id) + ">)"
        dt = datetime.now()
        uAvatar = before.avatar_url_as(static_format='jpeg')

        def findDiff(list1, list2):
            s = set(list2)
            return [x for x in list1 if x not in s]

        if len(after.roles) > len(before.roles):
            singularItemList = findDiff(after.roles, before.roles)
            roleName = singularItemList[0]

            embedx1 = Embed(title="Member Role Added", colour=Colour(0x4A90E2), timestamp=dt)
            embedx1.set_thumbnail(url=uAvatar)
            embedx1.set_footer(text="Prototype X1")
            embedx1.add_field(name="Member", value=uUser, inline=False)
            embedx1.add_field(name='Role Added', value=roleName, inline=False)

            await serverLogsChannel.send(embed=embedx1)
            return

        if len(after.roles) < len(before.roles):
            singularItemList = findDiff(before.roles, after.roles)
            roleName = singularItemList[0]

            embedx2 = Embed(title="Member Role Removed", colour=Colour(0x4A90E2), timestamp=dt)
            embedx2.set_thumbnail(url=uAvatar)
            embedx2.set_footer(text="Prototype X1")
            embedx2.add_field(name="Member", value=uUser, inline=False)
            embedx2.add_field(name='Role Removed', value=roleName, inline=False)

            await serverLogsChannel.send(embed=embedx2)
            return

        if after.display_name != before.display_name:
            uUserName_old = before.display_name
            uUserName_new = after.display_name

            embedx3 = Embed(title="Member Name Changed", colour=Colour(0x4A90E2), timestamp=dt)
            embedx3.set_thumbnail(url=uAvatar)
            embedx3.set_footer(text="Prototype X1")
            embedx3.add_field(name="Member", value=uUser, inline=False)
            embedx3.add_field(name="Old Username", value=uUserName_old, inline=False)
            embedx3.add_field(name="New Username", value=uUserName_new, inline=False)
            await serverLogsChannel.send(embed=embedx3)
            return


def setup(bot):
    bot.add_cog(Logger(bot))
