import asyncio
from requests import get
from datetime import datetime
from discord import Embed, Colour, TextChannel
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="corona")
    @commands.has_role('Moderators')
    @commands.guild_only()
    async def corona(self, ctx, country: str=None):
        _global = 0
        dt = datetime.now()
        baseURL = "https://corona.lmao.ninja/countries/"
        targetURL = ""

        if country == None:
            targetURL = "https://corona.lmao.ninja/all"
            _global = 1
        else:
            targetURL = baseURL + country.strip()

        loop = asyncio.get_event_loop()
        future1 = loop.run_in_executor(None, get, targetURL)
        response_data = await future1
        data = response_data.json()

        if _global == 1:
            embedTitle1 = "COVID-19 Statistics (Global)"
            embedx1 = Embed(title=embedTitle1, colour=Colour(0x571212), timestamp=dt)
            embedx1.set_footer(text="Prototype X1")
            embedx1.add_field(name="**Total Cases**", value=str(data['cases']), inline=False)
            embedx1.add_field(name="**Total Deaths**", value=str(data['deaths']), inline=False)
            embedx1.add_field(name="**Total Recovered**", value=str(data['recovered']), inline=False)
            lastUpdate = datetime.fromtimestamp(data['updated']/1000.0).strftime("%d/%m/%Y at %H:%M:%S")
            embedx1.add_field(name="**Last Updated**", value=lastUpdate, inline=False)
            await ctx.send(embed=embedx1)
        else:
            embedTitle2 = "COVID-19 Statistics for " + data['country']
            embedx2 = Embed(title=embedTitle2, colour=Colour(0x571212), timestamp=dt)
            embedx2.set_footer(text="Prototype X1")
            embedx2.add_field(name="**Total Cases**", value=str(data['cases']), inline=False)
            embedx2.add_field(name="**Cases Today**", value=str(data['todayCases']), inline=False)
            embedx2.add_field(name="**Total Deaths**", value=str(data['deaths']), inline=False)
            embedx2.add_field(name="**Deaths Today**", value=str(data['todayDeaths']), inline=False)
            embedx2.add_field(name="**Total Recovered**", value=str(data['recovered']), inline=False)
            embedx2.add_field(name="**Active Cases (Infected)**", value=str(data['active']), inline=False)
            embedx2.add_field(name="**(current) Ratio: Case / 1M**", value=str(data['casesPerOneMillion']), inline=False)
            await ctx.send(embed=embedx2)


def setup(bot):
    bot.add_cog(Fun(bot))
