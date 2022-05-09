"""
███████████████████████████████████████████████████████████████████████████████
█▄─█─▄█▄─▄▄▀█▄─█─▄█▄─▄▄─█─▄─▄─█─▄▄─█▄─▀█▄─▄█▄─▄█─▄─▄─█▄─▄▄─███▄─▄─▀█─▄▄─█─▄─▄─█
██─▄▀███─▄─▄██▄─▄███─▄▄▄███─███─██─██─█▄▀─███─████─████─▄█▀████─▄─▀█─██─███─███
█▄▄█▄▄█▄▄█▄▄██▄▄▄██▄▄▄████▄▄▄██▄▄▄▄█▄▄▄██▄▄█▄▄▄██▄▄▄██▄▄▄▄▄███▄▄▄▄██▄▄▄▄██▄▄▄██
A dynamic economy bot

developer: lvlonEmperor
date created: February 17 2022
version: v1.0
"""
import discord
from discord.ext import commands
import asyncio
import logging

from constants import *
from src.utils.json_utils import *
from src.utils.users import *
from src.utils.crypto_currency import *

# sets up logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="logs/discord.log", encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

imp_info = load_json("src/kryptonite_bot/imp_info.json") # loads the important info

bot = commands.Bot(command_prefix=">") # initializes the bot

@bot.event
async def on_ready(): # runs this on startup
    print("online")
    reload_constants()

@bot.command(aliases=["start"])
async def init(ctx): # creates an account
    user = User(ctx.author.id)
    await ctx.send("made your account")

@bot.command(aliases=["b", "balance"])
async def bal(ctx): # gives the current balance
    user = User(ctx.author.id)
    await ctx.send(
        f"Wallet: {user.wallet}\n"
        f"TFA: {user.accounts['tfa']['balance']}\n"
        f"NTFA: {user.accounts['ntfa']['balance']}"
    )

@bot.command(aliases=["investments", "i"])
async def holdings(ctx, account_name=None):
    """
    Views the user's holdings.

    By default, shows both. however, if specified, it will show a specific account's investments.

    depending on which account whose holdings we want, we can load holdings_list() which loads all
    holdings in an account and equates it to msg. we can then return msg
    """
    async def holdings_list(user:User, account_name:str ,msg:str):
        # loads all holdings in a user's account
        msg += f"{account_name.upper()}: ------------------------------\n"

        for holding in user.accounts[account_name]["holdings"]:
            msg += f"   {holding}: {user.accounts[account_name]['holdings'][holding]}\n"
        return msg

    user = User(ctx.author.id) # loads the user
    msg = ""

    if account_name == "tfa": # for the tax-free account
        msg = await holdings_list(user, "tfa", msg)

    elif account_name == "ntfa": # for the non-tax-free account
        msg = await holdings_list(user, "ntfa", msg)

    else: # otherwise load all accounts
        msg = await holdings_list(user, "tfa", msg)
        msg = await holdings_list(user, "ntfa", msg)

    await ctx.send(msg) # returns the message

@bot.command()
async def transfer(ctx, amount:float, uid:int):
    """
    Transfers money from 1 wallet to the next.

    only accepts non-zero positive values. then it calls the user.transfer() method
    afterward saves.
    """
    if amount<=0.0:
        await ctx.send("amount must be a positive number")
        return

    user = User(ctx.author.id)
    await ctx.send(user.transfer(amount=amount, uid=uid))

    user.save() # saves the user

@bot.command(aliases=["w"])
async def withdraw(ctx, account_name:str, amount:float):
    """
    Withdraws money from the user's bank account.

    The user specifies a non-zero positive amount of money and which bank account to
    choose from. the bank account can be either tfa or ntfa.
    afterward, it just calls the user.withdraw() method
    """
    if amount <=0.0:
        await ctx.send("amount must be a positive number")
        return

    user = User(ctx.author.id)
    await ctx.send(user.bank_withdraw(amount=amount, account_name=account_name))

    user.save()

@bot.command(aliases=["d"])
async def deposit(ctx, account_name: str, amount: float):
    """
    deposits money into the user's bank account.

    The user specifies a non-zero positive amount of money and which bank account to
    choose from. the bank account can be either tfa or ntfa.
    afterward, it just calls the user.deposit() method
    """
    if amount <= 0.0:
        await ctx.send("amount must be a positive number")
        return

    user = User(ctx.author.id)
    await ctx.send(user.bank_deposit(amount=amount, account_name=account_name))

    user.save() # saves

bot.run(imp_info["token"])