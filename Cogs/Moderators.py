import asyncio
import os
from datetime import datetime
from discord import Embed, Colour, Member
from discord.ext import commands
from discord.utils import get
from Utilities.DatabaseHandler import DatabaseHandler

mutedRoleID = int(os.environ.get('MutedRoleID'))
reportChannelID = int(os.environ.get('LEVEL0'))
modPubChannelID = int(os.environ.get('LEVEL1'))
serverLogsChannelID = int(os.environ.get('LEVEL2'))


class Moderators(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dbManager = DatabaseHandler()

    @commands.command(name='addbadword')
    @commands.has_role('Moderators')
    @commands.guild_only()
    async def addbadword(self, ctx, badw: str):
        await ctx.send("Adding '" + badw + "' to the database...")
        ret = await self.dbManager.addBadWord(badw)
        if ret == 0:
            await ctx.send("Successfully added to Database!\nPlease run `!reloadFilter 1` to update the filter!")
            return
        else:
            raise Exception()

    @commands.command(name='removebadword')
    @commands.has_role('Moderators')
    @commands.guild_only()
    async def removebadword(self, ctx, badw: str):
        await ctx.send("Removing '" + badw + "' from Database...")
        ret = await self.dbManager.removeBadWord(badw)
        if ret == 0:
            await ctx.send("Successfully removed from Database!\nPlease run `!reloadFilter 1` to update the filter!")
            return
        else:
            raise Exception()

    @commands.command(name='showbadwords')
    @commands.has_role('Moderators')
    @commands.guild_only()
    async def showbadwords(self, ctx):
        dt = datetime.now()
        listString = ""
        rdata = []
        udata = await self.dbManager.getAllBadWords()

        for entry in udata:
            rdata.append(entry['badword'])
        for word in rdata:
            listString += word + "\n"

        embedx = Embed(title="(Guild) Filtered Words", color=Colour(0xDA6262), timestamp=dt)
        embedx.set_footer(text="Plebs Watcher")
        embedx.add_field(name="Bad words", value=listString)

        await ctx.send(embed=embedx)

    @commands.command(name='mute')
    @commands.has_role('Moderators')
    @commands.guild_only()
    async def mute(self, ctx, member: Member, duration: str, *, reason: str):
        dt = datetime.now()
        mutedRole = get(ctx.guild.roles, id=mutedRoleID)

        if member == ctx.author:
            await ctx.message.delete()
            embedx1 = Embed(title="ERROR (Mute Command)", color=Colour(0xD0021B), timestamp=dt)
            embedx1.set_footer(text="Prototype X1")
            embedx1.add_field(name="dmsg", value="Cannot Mute Command Executioner!")
            await ctx.send(embed=embedx1, delete_after=3)
            return

        for currentRole in member.roles:
            if currentRole == mutedRole:
                await ctx.message.delete()
                embedx2 = Embed(title="ERROR (Mute Command)", color=Colour(0xD0021B), timestamp=dt)
                embedx2.set_footer(text="Prototype X1")
                embedx2.add_field(name="dmsg", value="User is already muted!")
                await ctx.send(embed=embedx2, delete_after=3)
                return

        dPeriod = duration[-1]
        dTime = 0
        dString = ""
        if dPeriod == 'm':
            dTime = int(duration[:-1]) * 60
            dString = str(int(duration[:-1])) + " Minutes"
        elif dPeriod == 'h':
            dTime = int(duration[:-1]) * 3600
            dString = str(int(duration[:-1])) + " Hours"

        uUser = member.display_name + " (<@" + str(member.id) + ">)"
        uMod = ctx.author.display_name + " (<@" + str(ctx.author.id) + ">)"
        uAvatar = member.avatar_url_as(static_format='jpeg')
        privateCH = self.bot.get_channel(modPubChannelID)

        await ctx.message.delete()
        await member.add_roles(mutedRole)

        embedx3 = Embed(title="Member Muted", colour=Colour(0xD0021B), timestamp=dt)
        embedx3.set_thumbnail(url=uAvatar)
        embedx3.set_footer(text="Prototype X1")
        embedx3.add_field(name="Member", value=uUser, inline=False)
        embedx3.add_field(name="Moderator", value=uMod, inline=False)
        embedx3.add_field(name="Duration", value=dString, inline=False)
        embedx3.add_field(name="Reason", value=reason, inline=False)
        await privateCH.send(embed=embedx3)

        if dTime > 0:
            await asyncio.sleep(dTime)
            for currentRole2 in member.roles:
                if currentRole2 == mutedRole:
                    await member.remove_roles(mutedRole)
                    dt2 = datetime.now()
                    embedx4 = Embed(title="Member Un-Muted", color=Colour(0xD0021B), timestamp=dt2)
                    embedx4.set_footer(text="Prototype X1")
                    embedx4.set_thumbnail(url=uAvatar)
                    embedx4.add_field(name="Member", value=uUser, inline=False)
                    embedx4.add_field(name="Moderator", value=uMod, inline=False)
                    embedx4.add_field(name="Muted at", value=str(dt), inline=False)
                    await privateCH.send(embed=embedx4)

    @commands.command(name='kick')
    @commands.has_role('Moderators')
    @commands.guild_only()
    async def kick(self, ctx, member: Member, *, reason: str):
        dt = datetime.now()
        uUser = member.display_name + " (<@" + str(member.id) + ">)"
        uMod = ctx.author.display_name + " (<@" + str(ctx.author.id) + ">)"
        uAvatar = member.avatar_url_as(static_format='jpeg')
        privateCH = self.bot.get_channel(modPubChannelID)

        if member == ctx.author:
            await ctx.message.delete()
            embedx1 = Embed(title="ERROR (Kick Command)", color=Colour(0xD0021B), timestamp=dt)
            embedx1.set_footer(text="Prototype X1")
            embedx1.add_field(name="dmsg", value="Cannot Kick Command Executioner!")
            await ctx.send(embed=embedx1, delete_after=3)
            return

        await ctx.message.delete()
        await member.kick()

        embedx2 = Embed(title="Member Kicked", colour=Colour(0x50E3C2), timestamp=dt)
        embedx2.set_thumbnail(url=uAvatar)
        embedx2.set_footer(text="Prototype X1")
        embedx2.add_field(name="Member", value=uUser, inline=False)
        embedx2.add_field(name="Moderator", value=uMod, inline=False)
        embedx2.add_field(name="Reason", value=reason, inline=False)
        await privateCH.send(embed=embedx2)

    @commands.command(name='ban')
    @commands.has_role('Moderators')
    @commands.guild_only()
    async def ban(self, ctx, member: Member, *, reason: str):
        dt = datetime.now()
        uUser = member.display_name + " (<@" + str(member.id) + ">)"
        uMod = ctx.author.display_name + " (<@" + str(ctx.author.id) + ">)"
        uAvatar = member.avatar_url_as(static_format='jpeg')
        privateCH = self.bot.get_channel(modPubChannelID)

        if member == ctx.author:
            await ctx.message.delete()
            embedx1 = Embed(title="ERROR (Ban Command)", color=Colour(0xD0021B), timestamp=dt)
            embedx1.set_footer(text="Prototype X1")
            embedx1.add_field(name="dmsg", value="Cannot Ban Command Executioner!")
            await ctx.send(embed=embedx1, delete_after=3)
            return

        await ctx.message.delete()
        await member.ban()

        embedx = Embed(title="Member Banned", colour=Colour(0x4A90E2), timestamp=dt)
        embedx.set_thumbnail(url=uAvatar)
        embedx.set_footer(text="Prototype X1")
        embedx.add_field(name="Member", value=uUser, inline=False)
        embedx.add_field(name="Moderator", value=uMod, inline=False)
        embedx.add_field(name="Reason", value=reason, inline=False)
        await privateCH.send(embed=embedx)

    @removebadword.error
    @addbadword.error
    @mute.error
    @kick.error
    @ban.error
    async def common_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.delete()
            embedx = Embed(title="Command Invocation Error", colour=Colour(0x000001))
            embedx.add_field(name="dmesg", value="Argument number mismatch! Please check your command.")
            await ctx.send(embed=embedx, delete_after=5)
        elif isinstance(error, commands.MissingRole):
            return
        elif isinstance(error, commands.NoPrivateMessage):
            return
        else:
            embedx = Embed(title="Command Error", colour=Colour(0x000001))
            embedx.add_field(name="dmesg", value="Unknown error, contact Bot Administrator!")
            await ctx.send(embed=embedx, delete_after=5)


def setup(bot):
    bot.add_cog(Moderators(bot))
