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

from random import randint, uniform, choice
from math import floor
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
    # dm me that it started
    reload_constants() # loads all the constants into memory
    load_db_into_cache() # loads all currencies

@bot.command()
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = f"Your running commands too quickly, you can try that again in {error.retry_after}"
        await ctx.send(msg)

@bot.command(aliases=["d"])
@commands.cooldown(1, 86400, commands.BucketType.user) # only used once per day.
async def daily(ctx): # daily command to give the user money into their wallet
    user = User(ctx.author.id)
    amount = randint(5000, 35_000)/100 # we use ints and divide by 100 so we can get better precision. range: 50-350
    user.wallet += amount
    user.save()
    await ctx.send(f"You recived ${amount}. the money has been deposited into your wallet")

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

@bot.command(aliases=["t"])
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

@bot.command(aliases=["bw"])
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

@bot.command(aliases=["bd"])
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

@bot.command(aliases=["v"])
async def view(ctx, coin_name:str): # view info on a specific currency
    """
    Displays information on a specific currency
    """
    msg =""
    # looks through the cache for the currency with the same name. if it matches, return it
    for currency_dict in crypto_cache:
        if currency_dict["name"] == coin_name:
            coin = CryptoCurrency(currency_dict)
            msg += f"{coin.name}:    Value: ${coin.value}, Total coins: ${coin.total_shares}, Market cap: ${coin.market_cap}"
            break
    await ctx.send(msg)


@bot.command(aliases=["l"])
async def list(ctx): # view a list of all currencies and their values
    """
    Loads all the currencies from the cache and displays their details.
    """
    msg = ""
    for i in range(len(crypto_cache)): # we directly use the cached dict, because loading the Cryptocurrency obj dont work
        msg += f"{crypto_cache[i]['name']}:" \
               f"    Value: ${crypto_cache[i]['value']}, " \
               f"Total coins: ${crypto_cache[i]['total_shares']}, " \
               f"Market cap: ${crypto_cache[i]['value'] * crypto_cache[i]['total_shares']}\n"
    await ctx.send(msg)

@bot.command(aliases=["purchase", "p"])
async def buy(ctx, account_name:str, coin_name:str, shares:int): # buy a currency
    """
    Buys shares of a cryptocurrency.

    Checks if the number of shares is a non-zero positive number greater than 1. if not, return. if the shares are valid,
    we check if the currency exists in the cache. If it does, we can calculate the value of the purchase,
    how much the coin will now cost, and what the total with taxes will be.
    Finally, we make some final checks to see if the purchase is valid. (has enough money, dosent exceed limits)
    then we can make the purchase and save.

    When calculating the value, it is compounded. we calculate the value of the currency and purchase 50 shares at a time.
    
    """

    if shares <1: # ensures the number of shares bought is at least 1
        ctx.send("You must purchase at least 1 share.")
        return

    shares = floor(shares) # makes sure all shares bought are int. not float.

    user = User(ctx.author.id) # loads the user

    if not CryptoCurrency.exists(coin_name): # checks if the coin exists. if so, load up the coin
        ctx.send(f"Crypto curency: {coin_name} does not exist")
        return
    else:
        coin = CryptoCurrency(CryptoCurrency.load_coin_dict(coin_name))

    # calculates the volume of the purchase
    subtotal = 0
    shares_traded = 0 # keeps track of the number of shares you buy
    v = coin.value # v keeps track of the value as we calculate the purchase
    shares_total = shares # the total number of shares bought
    # every iteraction of the loop, shares is decremented by at most, 50.
    # so as long as shares > 0, this loop will continue to run. or so long as the value dosent crash or surpass the
    # maximum value.



@bot.command(aliases=["s"])
async def sell(ctx, account_name:str, coin_name:str, shares:int): pass # sell a currency


# Run command and all the subprocesses
# subprocesses:
#   simulate all currencies
#   reload constants
#   change status?
bot.run(imp_info["token"])