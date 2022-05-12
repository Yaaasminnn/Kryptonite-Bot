import discord
from discord.ext.tasks import loop
from discord import Color as c

emb_colours = [ #COLOURS FOR EMBEDS. make this variable names like blue = c.blue(). also we can do hex codes
    c.blue(),
    c.blurple(),
    c.dark_blue(),
    c.dark_gold(),
    c.dark_gray(),
    c.dark_green(),
    c.dark_grey(),
    c.dark_magenta(),
    c.dark_orange(),
    c.dark_purple(),
    c.dark_red(),
    c.dark_teal(),
    c.dark_theme(),
    c.darker_gray(),
    c.darker_grey(),
    c.default(),
    c.gold(),
    c.green(),
    c.greyple(),
    c.light_gray(),
    c.light_grey(),
    c.lighter_gray(),
    c.lighter_grey(),
    c.magenta(),
    c.orange(),
    c.purple(),
    c.red(),
    c.teal() ]


async def dm_user(bot, id:int, msg:str): # dm's a user a message
    dm_channel = await bot.fetch_user(id) # gets the dm channel
    await discord.DMChannel.send(dm_channel, msg)

async def embed(): pass # makes an embed ???

@loop(seconds=30)
async def change_status(): pass # changes the status