# granitepy

A library for the Lavalink like audio provider called [Andesite](https://github.com/natanbc/andesite-node) for use with [discord.py](https://github.com/Rapptz/discord.py)



For support join [here](https://discord.gg/CHemuhc)




# Installing
 
The library isn't on PyPi yet so installing it will require git

`pip install git+https://github.com/twitch0001/granitepy`


# Example



```Python
import discord
from discord.ext import commands

import andesite # import the lib

bot = commands.Bot(command_prefix = "!")
bot.andesite = andesite.Client(bot)


@bot.event
async def on_ready():
    await bot.andesite.start_node(
            "127.0.0.1",
            5000,
            rest_uri = "http://127.0.0.1:5000/",
            password = None, # set as None if andesite password in application.conf is null :smh:
            identifier = "hello-there", # identifier is only for internal use.
    )

@bot.command()
async def connect(ctx):
    player = bot.andesite.get_player(ctx.guild.id) # fetches the player

    if not ctx.author.voice:
        return await ctx.send("Must be connected to a voice channel")
    
    await player.connect(ctx.author.voice.channel.id) # connects to the channel the command invoker is in

    await ctx.send(f"Connected to {ctx.author.voice.channel.name}!")

@bot.command()
async def play(ctx, *, search):
    player = bot.andesite.get_player(ctx.guild.id)

    tracks = await player.node.get_tracks(f"ytsearch: {search}") # returns a list andesite.Track objects 
    if not tracks: # andesite returned no tracks.
        return await ctx.send("Nothing found.")


    await player.play(tracks[0]) # plays the first track from the list.


bot.run("token")
```


This lib is heavily based on [Wavelink](https://github.com/EvieePy/Wavelink) made by [EvieePy](https://github.com/EvieePy) Huge thanks for making wavelink, would be stuck on a few connection things if it weren't for wavelink.


