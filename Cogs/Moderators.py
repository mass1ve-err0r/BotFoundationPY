from discord import Embed, Colour
from discord.ext import commands
from Utilities.DatabaseHandler import DatabaseHandler


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
            #
            return
        else:
            raise Exception()

    @removebadword.error
    @addbadword.error
    async def common_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.delete()
            embedx = Embed(title="Command Error", colour=Colour(0x000001))
            embedx.add_field(name="dmesg", value="An argument was missing!")
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
