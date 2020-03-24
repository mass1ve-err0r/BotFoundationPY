import os
from datetime import datetime
from discord import Embed, Colour, Member
from discord.ext import commands

reportChannelID = int(os.environ.get('LEVEL0'))
modPubChannelID = int(os.environ.get('LEVEL1'))
serverLogsChannelID = int(os.environ.get('LEVEL2'))


class Administrators(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='loadCog')
    @commands.has_role('Administrators')
    @commands.guild_only()
    async def loadCog(self, ctx, module: str):
        cogName = 'Cogs.' + module
        try:
            self.bot.load_extension(cogName)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send("Loaded Module '" + module + "'")

    @commands.command(name='unloadCog')
    @commands.has_role('Administrators')
    @commands.guild_only()
    async def unloadCog(self, ctx, module: str):
        cogName = 'Cogs.' + module
        try:
            self.bot.unload_extension(cogName)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send("Unloaded Module '" + module + "'")

    @commands.command(name='reloadCog')
    @commands.has_role('Administrators')
    @commands.guild_only()
    async def reloadCog(self, ctx, module: str):
        cogName = 'Cogs.' + module
        try:
            self.bot.reload_extension(cogName)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send("Reloaded Module '" + module + "'")

    @commands.command(name='showLoadedCogs')
    @commands.has_role('Administrators')
    @commands.guild_only()
    async def showLoadedCogs(self, ctx):
        dt = datetime.now()
        cogString = ""
        loadedCogs = self.bot.cogs.items()
        for entry in loadedCogs:
            cogString += entry[0] + "\n"

        embedx1 = Embed(title="Loaded Modules", color=Colour(0x000001), timestamp=dt)
        embedx1.set_footer(text="Prototype X1")
        embedx1.add_field(name="dmsg", value=cogString)
        await ctx.send(embed=embedx1)
        return

    @commands.command(name='showAllCogs')
    @commands.has_role('Administrators')
    @commands.guild_only()
    async def showAllCogs(self, ctx):
        dt = datetime.now()
        cogsWithDetails = {
            'AntiSpam': 'Efficient AntiSpam against low-effort trolling and more',
            'Filter': 'Filter messages for "bad words"',
            'Fun': '(Default) A wide variety of fun functionality (Magic8, Covid-19 stats, say & more)',
            'Logger': 'Log all major discord events in a guild! (Roles, Member updates, joins/ leaves, message manipulation)',
            'Maintenance': '(Default) Perform maintenance tasks -- Bot admin ONLY',
            'Moderator': '(Default) perform various mod-actions such as ban, mute and kick',
            'Music': '(BETA) This provides Music functionality --playback source is YouTube',
            'OptionalFilters': 'Filter for more objects such as caps-lock or spoilers!'
        }

        embedx1 = Embed(title="All Available Modules", color=Colour(0x000001), timestamp=dt)
        embedx1.set_footer(text="Prototype X1")
        for _cog in cogsWithDetails:
            embedx1.add_field(name="**" + _cog + "**", value="*" + cogsWithDetails[_cog] + "*")
        await ctx.send(embed=embedx1)
        return

    @commands.command(name='hardmute')
    @commands.has_role('Administrators')
    @commands.guild_only()
    async def hardmute(self, ctx, member: Member = None, *, reason: str):
        dt =datetime.now()
        await ctx.message.delete()
        uUser = member.display_name + " (<@" + str(member.id) + ">)"
        uAdmin = ctx.author.display_name + " (<@" + str(ctx.author.id) + ">)"
        uAvatar = member.avatar_url_as(static_format='jpeg')
        privateCH = self.bot.get_channel(modPubChannelID)

        for kChannel in ctx.guild.text_channels:
            await kChannel.set_permissions(member, send_messages=False)

        embedx = Embed(title="Member Excluded", colour=Colour(0x00FFC0), timestamp=dt)
        embedx.set_thumbnail(url=uAvatar)
        embedx.set_footer(text="Prototype X1")
        embedx.add_field(name="Member", value=uUser, inline=False)
        embedx.add_field(name="Administrator", value=uAdmin, inline=False)
        embedx.add_field(name="Reason", value=reason, inline=False)
        await privateCH.send(embed=embedx)
        return

    @commands.command(name='hardunmute')
    @commands.has_role('Administrators')
    @commands.guild_only()
    async def hardunmute(self, ctx, member: Member = None):
        dt = datetime.now()
        await ctx.message.delete()
        uUser = member.display_name + " (<@" + str(member.id) + ">)"
        uAdmin = ctx.author.display_name + " (<@" + str(ctx.author.id) + ">)"
        uAvatar = member.avatar_url_as(static_format='jpeg')
        privateCH = self.bot.get_channel(modPubChannelID)

        for kChannel in ctx.guild.text_channels:
            await kChannel.set_permissions(member, send_messages=True)

        embedx = Embed(title="Member Included", colour=Colour(0x00FFC0), timestamp=dt)
        embedx.set_thumbnail(url=uAvatar)
        embedx.set_footer(text="Prototype X1")
        embedx.add_field(name="Member", value=uUser, inline=False)
        embedx.add_field(name="Administrator", value=uAdmin, inline=False)
        await privateCH.send(embed=embedx)
        return


def setup(bot):
    bot.add_cog(Administrators(bot))
