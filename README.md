# granitepy

A library for the lavalink like audio provider called andesite found [here](https://github.com/natanbc/andesite-node)


The library isn't on PyPi yet so installing it will require git

`pip install git+https://github.com/twitch0001/granitepy`



```Python
import discord
from discord.ext import commands

import andesite # import the lib

bot = commands.Bot(command_prefix = "!")
bot.andesite = andesite.Client(bot)


@bot.event
async def on_ready():
    await bot.andesite.andesite.start_node(
            "127.0.0.1",
            5000,
            rest_uri = "http://127.0.0.1:5000/",
            password = None, # set as None if andesite password in application.conf is null :smh:
            identifier = "hello-there", # identifier is only for internal use.
    )

@bot.command()
async def connect(ctx):
    player = bot.andesite.get_player(ctx.guild.id) # fetches the player
    
    await player.connect(ctx.author.voice.channel.id) # connects to the channel the command invoker is in

    await ctx.send(f"Connected to {ctx.author.voice.channel.name}!")

@bot.command()
async def play(ctx, *, search):
    player = bot.andesite.get_player(ctx.guild.id)

    tracks = await player.node.get_tracks(f"ytsearch: {search}") # returns a list andesite.Track objects 

    await player.play(tracks[0]) # plays the first track from the list.


bot.run("token")
```


This lib is heavily based on [Wavelink](https://github.com/EvieePy/Wavelink) made by [EvieePy](https://github.com/EvieePy) Huge thanks for making wavelink, would be stuck on a few connection things if it weren't for wavelink.



