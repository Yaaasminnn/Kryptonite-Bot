import discord
from discord.ext.tasks import loop

async def dm_user(bot, id:int, msg:str): # dm's a user a message
    dm_channel = await bot.fetch_user(id) # gets the dm channel
    await discord.DMChannel.send(dm_channel, msg)

async def embed(): pass # makes an embed ???

@loop(seconds=30)
async def change_status(): pass # changes the status