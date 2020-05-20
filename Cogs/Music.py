"""
This is adapted from the official lavalink-py example
"""
import asyncio
import re
import discord
import lavalink
from os import environ as env
from datetime import datetime
from lavalink.models import DefaultPlayer, AudioTrack
from discord.ext import commands

url_rx = re.compile(r'https?://(?:www\.)?.+')
LVPassword = env.get('LavalinkPass')
LVAddress = env.get('LavalinkAddr')
LVPort = int(env.get('LavalinkPort'))
LVIdent = env.get('LavalinkID')


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'lavalink'):  # This ensures the client isn't overwritten during cog reloads.
            bot.lavalink = lavalink.Client(bot.user.id)
            bot.lavalink.add_node(LVAddress, LVPort, LVPassword, 'eu', 'default-node', name=LVIdent)
            bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')

        lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        """ Cog unload handler. This removes any event hooks that were registered. """
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        """ Command before-invoke handler. """
        guild_check = ctx.guild is not None

        if guild_check:
            await self.ensure_voice(ctx)

        return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)

    async def ensure_voice(self, ctx):
        """ This check ensures that the bot and command author are in the same voicechannel. """
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        should_connect = ctx.command.name in ('play', 'skip', 'pause', 'loop',)

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandInvokeError('Join a voicechannel first.')

        if not player.is_connected:
            if not should_connect:
                raise commands.CommandInvokeError('Not connected.')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:  # Check user limit too?
                raise commands.CommandInvokeError('I need the `CONNECT` and `SPEAK` permissions.')

            player.store('channel', ctx.channel.id)
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError('You need to be in my voicechannel.')

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        """ Connects to the given voicechannel ID. A channel_id of `None` means disconnect. """
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    @commands.command(name='play')
    async def play(self, ctx, *, query: str):
        """ Searches and plays a song from a given query. """
        dt = datetime.now()
        embed = discord.Embed(color=discord.Color.blurple(), datetime=dt)

        def verify_msg_author(m):
            return m.author == ctx.author and m.channel == ctx.channel

        # Get the player for this guild from cache.
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        # Remove leading and trailing <>. <> may be used to suppress embedding links in Discord.
        query = query.strip('<>')

        # Check if the user input might be a URL. If it isn't, we can Lavalink do a YouTube search for it instead.
        # SoundCloud searching is possible by prefixing "scsearch:" instead.
        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        # Get the results for the query from Lavalink.
        results = await player.node.get_tracks(query)

        # Results could be None if Lavalink returns an invalid response (non-JSON/non-200 (OK)).
        # ALternatively, resullts['tracks'] could be an empty array if the query yielded no tracks.
        if not results or not results['tracks']:
            embed.title = "Search Error"
            embed.description = "Search yielded no results! (Try again maybe?)"
            return await ctx.send(embed=embed)

        # Valid loadTypes are:
        #   TRACK_LOADED    - single video/direct URL)
        #   PLAYLIST_LOADED - direct URL to playlist)
        #   SEARCH_RESULT   - query prefixed with either ytsearch: or scsearch:.
        #   NO_MATCHES      - query yielded no results
        #   LOAD_FAILED     - most likely, the video encountered an exception during loading.
        if results['loadType'] == 'PLAYLIST_LOADED':
            embed.title = "Playback Error"
            embed.description = "Playlist playback is currently NOT supported"
            if player.is_connected and not player.is_playing:
                await self.disconnect(ctx=ctx)
            return await ctx.send(embed=embed)
            # We don't fuck with  for now
        else:
            uChoice = -1
            if (len(results['tracks'])) == 1:
                embed.title = "Song Selected (via URL)"
                oTrack = results['tracks'][0]
                oTrack_t = datetime.fromtimestamp(oTrack['info']['length'] / 1000.0).strftime("%M:%S")
                embed.add_field(name=oTrack['info']['title'],
                                value="Duration: " + oTrack_t,
                                inline=False)
                embed.set_footer(text="Requested by: " + ctx.author.name)
                await ctx.send(embed=embed)

                track = lavalink.models.AudioTrack(oTrack, ctx.author.id, recommended=True)
                player.add(requester=ctx.author.id, track=track)
                if not player.is_playing:
                    await player.play()
                return

            embed.title = "Song Selection"
            for idx, track in enumerate(results['tracks'], start=1):
                if idx > 5:
                    break
                embed.add_field(name="**" + str(idx) + "** \u2B95 " + track["info"]["title"],
                                value="Channel: " + track["info"]["author"],
                                inline=False)
            choiceEmbed = await ctx.send(embed=embed)
            try:
                uC_msg = await self.bot.wait_for('message', check=verify_msg_author, timeout=30.0)
                uChoice = int(uC_msg.content)
            except asyncio.TimeoutError:
                await ctx.send('You took too long...')
            except ValueError:
                embed.title = "Song Selection Failed"
                embed.clear_fields()
                embed.description = "Failed to make a selection! (Did you pass in a Number?)"
                await choiceEmbed.edit(embed=embed)
            else:
                if uChoice <= 0:
                    embed.title = "Song Selection Failed"
                    embed.clear_fields()
                    embed.description = "Failed to make a selection! (Negative Number!)"
                    await choiceEmbed.edit(embed=embed)
                    return
                if uChoice > 5:
                    embed.title = "Song Selection Failed"
                    embed.clear_fields()
                    embed.description = "Failed to make a selection! (Number out of range!)"
                    await choiceEmbed.edit(embed=embed)
                    return
                uChoice -= 1
                fTrack = results['tracks'][uChoice]
                embed.title = "Song Selected"
                embed.clear_fields()
                fTrack_t = datetime.fromtimestamp(fTrack['info']['length']/1000.0).strftime("%M:%S")
                embed.add_field(name=fTrack['info']['title'],
                                value="Duration: " + fTrack_t,
                                inline=False)
                embed.set_footer(text="Requested by: " + ctx.author.name)
                await choiceEmbed.edit(embed=embed)

                track = lavalink.models.AudioTrack(fTrack, ctx.author.id, recommended=True)
                player.add(requester=ctx.author.id, track=track)

        # We don't want to call .play() if the player is playing as that will effectively skip
        # the current track.
        if not player.is_playing:
            await player.play()

    @commands.command(name='stop')
    async def disconnect(self, ctx):
        """ Disconnects the player from the voice channel and clears its queue. """
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            return await ctx.send('Not connected.')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Abuse prevention. Users not in voice channels, or not in the same voice channel as the bot
            # may not disconnect the bot.
            return await ctx.send('You\'re not in my voicechannel!')

        # Clear the queue to ensure old tracks don't start playing
        # when someone else queues something.
        player.queue.clear()
        # Stop the current track so Lavalink consumes less resources.
        await player.stop()
        # Disconnect from the voice channel.
        await self.connect_to(ctx.guild.id, None)
        dt = datetime.now()
        embed = discord.Embed(color=discord.Color.blurple(), datetime=dt)
        embed.title = 'Playback Stopped'
        return await ctx.send(embed=embed)

    @commands.command(name='vol')
    async def vol(self, ctx, volume: int):
        """Changes the player's volume"""
        player: DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            return await ctx.send('Not connected.')

        await player.set_volume(volume)
        dt = datetime.now()
        embed = discord.Embed(color=discord.Color.blurple(), datetime=dt)
        embed.title = 'Player Volume Changed'
        embed.description = "Changed volume to {}%".format(volume)
        return await ctx.send(embed=embed)

    @commands.command(name='queue', aliases=['q'])
    async def queue(self, ctx):
        """Changes the player's volume"""
        player: DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            return await ctx.send('Not connected.')

        dt = datetime.now()
        embed = discord.Embed(color=discord.Color.blurple(), datetime=dt)
        embed.title = 'Queue'
        if len(player.queue) == 0:
            embed.description = "Nothing queued up!"
        else:
            for idx, track in enumerate(player.queue, start=1):
                track_t = datetime.fromtimestamp(track.duration / 1000.0).strftime("%M:%S")
                embed.add_field(name="**"+ str(idx) +".** " + track.title,
                                value="Duration: " + track_t,
                                inline=False)

        embed.set_footer(text="Requested by: " + ctx.author.name)
        await ctx.send(embed=embed)

    @commands.command(name='loop')
    async def loop_s(self, ctx):
        """Loop the current Song"""
        player: DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            return await ctx.send('Not connected.')

        dt = datetime.now()
        embed = discord.Embed(color=discord.Color.blurple(), datetime=dt)
        if player.repeat is False:
            player.repeat = True
            embed.title = 'Endless Playback ON'
            embed.description = "Current Song will be played back indefinitely!"
            await ctx.send(embed=embed)
        else:
            player.repeat = False
            embed.title = 'Endless Playback OFF'
            embed.description = "Song will no longer be played on repeat!"
            await ctx.send(embed=embed)

    @commands.command(name='now', aliases=['np'])
    async def nowplaying(self, ctx):
        """Loop the current Song"""
        player: DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            return await ctx.send('Not connected.')
        if not player.is_playing:
            # We can't show NP info, if we're not playing anything.
            return await ctx.send('Not Playing anything.')

        dt = datetime.now()
        embed = discord.Embed(color=discord.Color.blurple(), datetime=dt)
        embed.title = "Now Playing"
        cTrack: AudioTrack = player.current
        track_t = datetime.fromtimestamp(cTrack.duration / 1000.0).strftime("%M:%S")
        embed.add_field(name=cTrack.title,
                        value="Duration: " + track_t,
                        inline=False)
        await ctx.send(embed=embed)
        return

    @commands.command(name='skip')
    async def skip_s(self, ctx):
        """Loop the current Song"""
        player: DefaultPlayer = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            return await ctx.send('Not connected.')

        dt = datetime.now()
        embed = discord.Embed(color=discord.Color.blurple(), datetime=dt)
        embed.title = "Skipping Song!"
        await ctx.send(embed=embed)
        await player.play()
        await self.nowplaying(ctx=ctx)
        return


def setup(bot):
    bot.add_cog(Music(bot))
