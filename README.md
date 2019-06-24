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
```

