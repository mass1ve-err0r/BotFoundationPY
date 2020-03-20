import ast
import discord
from discord.ext import commands


class Maintenance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def insert_returns(self, body):
        if isinstance(body[-1], ast.Expr):
            body[-1] = ast.Return(body[-1].value)
            ast.fix_missing_locations(body[-1])
        if isinstance(body[-1], ast.If):
            self.insert_returns(body[-1].body)
            self.insert_returns(body[-1].orelse)
        if isinstance(body[-1], ast.With):
            self.insert_returns(body[-1].body)

    @commands.command(name='eval')
    async def eval_function(self, ctx, *, fnstr):
        # restrict eval to the bot creator
        if ctx.author.id != 485880883119783956:
            return

        fn_name = "_eval_expr"
        cmd = fnstr.strip("` ")
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
        body = f"async def {fn_name}():\n{cmd}"
        parsed = ast.parse(body)
        body = parsed.body[0].body
        self.insert_returns(body)
        env = {
            'bot': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)
        result = (await eval(f"{fn_name}()", env))
        await ctx.send(result)

    @commands.command(name='ping')
    async def ping(self, ctx):
        if ctx.author.id != 485880883119783956:
            return

        await ctx.send('pong! (Latency: {0} seconds)'.format(round(self.bot.latency, 1)))


def setup(bot):
    bot.add_cog(Maintenance(bot))
