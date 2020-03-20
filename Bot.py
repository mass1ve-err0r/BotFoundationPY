import os
from discord import Game
from datetime import datetime
from discord.ext import commands

bot = commands.Bot(command_prefix='?')
bot.remove_command("help")

extensions = ['Cogs.Moderators',
              'Cogs.Logger',
              'Cogs.Filter',
              'Cogs.Fun',
              'Cogs.Maintenance',
              'Cogs.AntiSpam']

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print('Logged in at: {0}'.format(datetime.now()))
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=Game(name='Be nice to people!'))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

bot.run(os.environ.get('TOKEN'))
