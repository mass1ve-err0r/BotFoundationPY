import os
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
bot.remove_command("help")

extensions = ['Cogs.Moderators',
              'Cogs.Logger',
              'Cogs.Filter',
              'Cogs.Fun']

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name='Be nice to people!'))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)


bot.run(os.environ.get('TOKEN'))
