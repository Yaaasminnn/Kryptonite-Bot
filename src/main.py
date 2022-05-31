"""
A dynamic economy bot

developer: lvlonEmperor
date created: February 17 2022
version: v1.0
"""

import discord
from discord.ext import commands
from discord.ext.tasks import loop
import asyncio
import logging

from random import randint, uniform, choice
from math import floor
import sys
#sys.path.insert(0, '../src'); print(sys.path[0])
from constants import *
from src.utils.json_utils import *
from src.utils.users import *
from src.utils.crypto_currency import *
from src.utils.discord_utils import *

# sets up logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="logs/discord.log", encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

imp_info = load_json("src/kryptonite_bot/imp_info.json") # loads the important info

bot = commands.Bot(command_prefix=">", help_command=None) # initializes the bot. disables the default help command


# GENERAL BOT COMMANDS =================================================================#


@bot.event
async def on_ready(): # runs this on startup
    print("online")

    # dm me that it started
    await dm_user(bot, id=imp_info['owner id'], msg="Online")

    await reload_constants() # loads all the constants into memory

    await load_db_into_cache() # loads all currencies

    await print_cache() # prints the cache

    #pretty_print(crypto_cache)

@bot.event
async def on_command_error(ctx, error):
    # the cooldown error
    # if the user tries to run a command while on cooldown, this message is sent
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title="Your sending commands too quickly!",
                           description=f"You can try that again in {int(error.retry_after)} seconds")
        await ctx.send(embed=em)

@bot.command()
async def change_constants(ctx, constant_name:str, value):# allows me to change the constants
    if ctx.author.id != imp_info['owner id']: return

    await change_constants(constant_name, value)

@bot.command()
async def clear_coins(ctx): # allows me to clear the crypto db
    if ctx.author.id != imp_info['owner id']: return

    clear_db() # clears the db

    await dm_user(bot,imp_info["owner id"], "Cleared the Crypto Database")

    print("Cleared the Crypto Database")

@bot.command(aliases=['add'])
async def add_currency(ctx): # allows me to add currencies
    if ctx.author.id != imp_info['owner id']: return

    coin = CryptoCurrency()

    await dm_user(bot, imp_info["owner id"], f"Added new currency, {coin.name}")
    print(f"Added new currency, {coin.name}")


# HELP COMMAND STUFF =================================================================#


@bot.group(invoke_without_command=True, aliases=['h'])
async def help(ctx): # make this a docs page
    em = discord.Embed(title="Help Menu", description="Use '>help [command]' for more info.", color=c.purple())
    em.add_field(name="How to play", value="coins, accounts, taxes, wallet", inline=False)
    em.add_field(name="Economy commands:", value="daily, init, balance, deposit, withdraw, transfer, beg", inline=False)
    em.add_field(name="Crypto commands:", value="holdings, view, buy, sell, list", inline=False)
    em.add_field(name="Gambling commands:", value="coin_flip, lower", inline=False)

    await ctx.send(embed=em)

@help.command()
async def daily(ctx):
    em = discord.Embed(title="Daily", description="daily command to get more money.", color=c.purple())
    em.add_field(name="Usage", value="'>daily' or '>d'", inline=False)
    em.add_field(name="Description", value="Can earn $50-$350 dollars added to your bank account once every 24 hours.\n\n"
                                           "For more info on your wallet, use; '>help wallet'", inline=False)

    await ctx.send(embed=em)

@help.command()
async def init(ctx):
    em = discord.Embed(title="Init", description="Initialize your account.", color=c.purple())
    em.add_field(name="Usage", value="'>init'", inline=False)
    em.add_field(name="Description", value="Creates your bank accounts and gives your wallet a starting value of $200.\n"
                                           " Use this command to get started.\n\n"
                                           "For more info on your accounts, use; '>help accounts'\n"
                                           "For more info on your wallet, use; '>help wallet'", inline=False)

    await ctx.send(embed=em)

@help.command()
async def bal(ctx):
    em = discord.Embed(title="Balance", description="View your current balance.", color=c.purple())
    em.add_field(name="Usage", value="'>b', '>balance' or '>bal'", inline=False)
    em.add_field(name="Description", value="View how much money you have in your wallet and bank accounts.\n\n"
                                           "For more info on your accounts, use; '>help accounts'", inline=False)
    em.add_field(name="Examples", value="Wallet: 200.0\n"
                                        "TFA: 0.0\n"
                                        "NTFA: 25.0", inline=False)

    await ctx.send(embed=em)

@help.command()
async def holdings(ctx):
    em = discord.Embed(title="Holdings", description="View your investments.", color=c.purple())
    em.add_field(name="Usage", value="'>holdings', '>investments' or '>i'", inline=False)
    em.add_field(name="Description", value="View the number of coins you currently own across both accounts.\n\n"
                                           "For more info on accounts, use; '>help accounts'\n"
                                           "For more help on coins, use; '>help coins'", inline=False)
    em.add_field(name="Example", value="TFA: ----------------------------\n"
                                       "   coin_1: 4\n"
                                       "NTFA: ---------------------------\n"
                                       "   coin_3: 2", inline=False)

    await ctx.send(embed=em)

@help.command()
async def transfer(ctx):
    em = discord.Embed(title="Transfer", description="Transfer money from your wallet to another's wallet.", color=c.purple())
    em.add_field(name="Usage", value="'>transfer [**amount**] [**@user**]' or '>t [**amount**] [**@user**]'", inline=False)
    em.add_field(name="Example", value=">transfer 500 @user\n"
                                       "*Transfers $500 from your wallet to @user's wallet*", inline=False)
    em.add_field(name="Description", value=f"transfer money from your wallet to the specified user's wallet.\n "
                                           f"Has to be less than ${max_transfer_limit/100} and greater then 0 since you cant steal money from people.\n\n"
                                           f"For more info on your wallet, use; '>help wallet'",
                 inline=False)

    await ctx.send(embed=em)

@help.command()
async def withdraw(ctx):
    em = discord.Embed(title="Withdraw", description="Withdraw money from the bank.", color=c.purple())
    em.add_field(name="Usage", value="'>withdraw [**ntfa or tfa**] [**amount**]' or '>bw  [**ntfa or tfa**] [**amount**]'", inline=False)
    em.add_field(name="Example", value=">withdraw tfa 500\n"
                                       "*Withdraws $500 from your tax-free account*", inline=False)
    em.add_field(name="Description",
                 value=f"You can withdraw money from a certain bank account. you have 2 bank accounts, tfa(Tax-Free account)"
                       f" and ntfa(Non-Tax-Free account).\n "
                       f"There are no limits on how much you can transfer between your wallet and accounts.\n"
                       f"The only constraints is that amount must be a positive number.\n\n"
                       f"Withdraw works the same way as the deposit command does.\n\n"
                       f"For more info on your accounts, use; '>help accounts'\n"
                       f"For more info on your wallet, use; '>help wallet'", inline=False)

    await ctx.send(embed=em)

@help.command()
async def deposit(ctx):
    em = discord.Embed(title="Deposit", description="Deposit money into the bank.", color=c.purple())
    em.add_field(name="Usage", value="'>deposit [**ntfa or tfa**] [**amount**]' or '>bd  [**ntfa or tfa**] [**amount**]'", inline=False)
    em.add_field(name="Example", value=">deposit tfa 500\n"
                                       "*Deposits $500 into your tax-free account*", inline=False)
    em.add_field(name="Description",
                 value=f"You can deposit money from a certain bank account. you have 2 bank accounts, tfa(Tax-Free account)"
                       f" and ntfa(Non-Tax-Free account).\n"
                       f"There are no limits on how much you can transfer between your wallet and accounts.\n"
                       f"The only constraints is that amount must be a positive number.\n"
                       f"Deposit works the same way as the withdraw command does"
                       f"For more info on your accounts, use; '>help accounts'\n"
                       f"For more info on your wallet, use; '>help wallet'", inline=False)

    await ctx.send(embed=em)

@help.command()
async def view(ctx):
    em = discord.Embed(title="View", description="View the details of a Cryptocurrency.", color=c.purple())
    em.add_field(name="Usage", value="'>view [**coin name**]' or '>v  [**coin name**]'", inline=False)
    em.add_field(name="Example", value=">view kuki-bux\n"
                                       "*Views the value, total coins and market cap of kuki-bux*", inline=False)
    em.add_field(name="Description",
                 value=f"View the value, total coins and market cap of a certain cryptocurrency.\n"
                       f"The cryptocurrency must be given by name.\n\n"
                       f"for more info on Crypto Currencies, use; '>help coins'", inline=False)

    await ctx.send(embed=em)

@help.command()
async def list(ctx):
    em = discord.Embed(title="List", description="View the details of all Cryptocurrencies.", color=c.purple())
    em.add_field(name="Usage", value="'>list' or '>l'", inline=False)
    em.add_field(name="Description",
                 value=f"View the value, total coins and market cap of all cryptocurrencies.\n\n"
                       f"for more info on Crypto Currencies, use; '>help coins'\n", inline=False)

    await ctx.send(embed=em)

@help.command()
async def buy(ctx):
    em = discord.Embed(title="Buy", description="Buy a cryptocurrency.", color=c.purple())
    em.add_field(name="Usage", value="'>buy [**ntfa or tfa**] [**coin name**] [**num coins to buy**]',\n '>purchase [**ntfa or tfa**] [**coin name**] [**num coins to buy**]'\n or '>p [**ntfa or tfa**] [**coin name**] [**num coins to buy**]'", inline=False)
    em.add_field(name="Example", value=f">buy ntfa {crypto_cache[0]['name']} 1\n"
                                       f"*Buys 1 {crypto_cache[0]['name']} coin for your ntfa account. this will be taxed*")
    em.add_field(name="Description",
                 value=f"Buy into a Cryptocurrency. you must specify which account you will use (tfa or ntfa)."
                       f"The chosen account will store the holding of said cryptocurrency's coins.\n This means that each account can hold different investments."
                       f"Both accounts can hold coins of the same currency.\n "
                       f"(ntfa can hold your {crypto_cache[0]['name']} coins while tfa can also hold {crypto_cache[0]['name']} coins at the same time)\n\n"
                       f"You must buy at least 1 of a coin. no fractional buys.\n\n"
                       f"Do note that there are limits set in place for how many coins you can buy/sell at a time({trading_limit_shares}) and maximum trade volumes(for more info, use; '>help accounts'). Trades are also limited to 1 every 15 seconds.\n\n"
                       f"Additionally, there are taxes(12%) imposed on your purchase if you are using a ntfa bank account.\n\n"
                       f"For more info on taxes, use; '>help taxes'", inline=False)

    await ctx.send(embed=em)

@help.command()
async def sell(ctx):
    em = discord.Embed(title="Sell", description="Sell a cryptocurrency.", color=c.purple())
    em.add_field(name="Usage",
                 value="'>sell [**ntfa or tfa**] [**coin name**] [**num coins to buy**]'\nor '>s [**ntfa or tfa**] [**coin name**] [**num coins to buy**]'",
                 inline=False)
    em.add_field(name="Example", value=f">sell ntfa {crypto_cache[0]['name']} 1\n"
                                       f"*Sells 1 {crypto_cache[0]['name']} coin from your ntfa account.*")
    em.add_field(name="Description",
                 value=f"Sell coins of a Cryptocurrency. you must specify which account you will use (tfa or ntfa)."
                       f"The chosen account will sell shares of said cryptocurrency's coins.\n This means that each account can hold different investments. "
                       f"Both accounts can hold coins of the same cryptocurrency.\n "
                       f"(ntfa can hold your {crypto_cache[0]['name']} coins while tfa can also hold {crypto_cache[0]['name']} coins at the same time)\n\n"
                       f"You must sell at least 1 of a coin. no fractional sales.\n\n"
                       f"Do note that there are limits set in place for how many coins you can buy/sell at a time({trading_limit_shares}) and maximum trade volumes(for more info, use; '>help accounts'). Trades are also limited to 1 every 15 seconds.\n\n"
                       f"There are no taxes on sales.\n\n"
                       f"For more info on taxes, use; '>help taxes'", inline=False)

    await ctx.send(embed=em)

@help.command()
async def coins(ctx):
    em = discord.Embed(title="Coins", description="All about coins and cryptocurrencies", color=c.purple())
    em.add_field(name="What are cryptocurrencies?",
                 value=f"Cryptocurrencies are coins that users can invest in using their money from their bank accounts.",
                 inline=False)
    em.add_field(name="How do cryptocurrencies work?",
                 value=f"The bot stores between 2-7 cryptocurrencies at a time.\n"
                       f" every minute, each cryptocurrency is simulated and it's value changes.\n"
                       f" occasionally, they might spike or fall in value significantly.\n "
                       f"For more info on viewing the value and details of a cryptocurrency, use; '>help view'\n\n"
                       f"Sometimes a cryptocurrency might reach a value of $0, "
                       f"if this is the case, it will crash, be deleted, and anyone who had invested in said coin, will "
                       f"lose their investments.",
                 inline=False)
    em.add_field(name="Can I buy them? How?",
                 value="Yes. You can purchase them using one of your bank accounts so long as your bank account has enough balance.\n"
                       "To learn how to trade cryptocurrencies, use; '>help buy' or '>help sell'.\n"
                       "For more info on bank accounts, use; '>help accounts'.")

    await ctx.send(embed=em)

@help.command()
async def accounts(ctx):
    em = discord.Embed(title="Accounts", description="All about your bank accounts.", color=c.purple())
    em.add_field(name="What are accounts?",
                 value="Bank accounts are used to store money and investments. simple as that.\n",
                 inline=False)
    em.add_field(name="What kind of accounts are there?",
                 value=f"There are 2 accounts:\n\n"
                       f" **Tax-free accounts**, also known as **tfa**. these are not taxed on purchases. "
                       f"This means that crypto purchases will be cheaper with a tax-free account, however, trades with said account are limited(max of ${tax_free_trading_limit_dollars/100})."
                       f"These accounts are better suited for smaller purchases.\n\n"
                       f"Next, there are **Non-Tax-free accounts** also known as **ntfa**. these accounts are taxed."
                       f"Every cryptocurrency purchase will be taxed by 12%, however, you can make much larger trades with ntfa accounts(max of ${taxed_trading_limit_dollars/100})",
                 inline=False)
    em.add_field(name="How do my accounts store my investments?",
                 value=f"Upon purchasing, the name of the currency and the number of coins you have purchased are logged into your account. you can view this using '>holdings'\n\n"
                       f"The account you specify will hold that purchase. "
                       f"This means each accounts investments are independent and seperate of eachother. Another note is that just because one account has investments in a certain coin, "
                       f"does not mean another cannot also have investments of the same coin.",
                 inline=False)
    em.add_field(name="How can i transfer my money to my bank account?",
                 value="For info on how to transfer money from your wallet to your bank accounts and back, use; '>help withdraw' or '>help deposit'",
                 inline=False)
    em.add_field(name="Properties of accounts",
                 value="- name: [tfa/ntfa]\n"
                       "- balance: [balance in your account]\n"
                       "- holdings: [list of all your holdings]",
                 inline=False)

    await ctx.send(embed=em)

@help.command()
async def taxes(ctx):
    em = discord.Embed(title="Taxes", description="All about your taxes.", color=c.purple())
    em.add_field(name="When are there taxes used??",
                 value="Taxes are only placed when the user is buying a currency using a ntfa account. \n"
                       "Otherwise, all interactions are tax-free\n"
                       "For more info on accounts, use; '>help accounts'\n"
                       "For more info on cryptocurrencies, use; '>help coins'",
                 inline=False)
    em.add_field(name="How much are taxes?",
                 value="12% of the total cost of the purchase.",
                 inline=False)

    await ctx.send(embed=em)

@help.command()
async def wallet(ctx):
    em = discord.Embed(title="Wallet", description="All about your Wallet.", color=c.purple())
    em.add_field(name="What is my Wallet for?",
                 value="Your wallet is used for money on your person. "
                       "Any money you make daily, gambling or transfers use your wallet.\n"
                       "For more info on daily, use; '>help daily'\n"
                       "For more info on gambling, use; '>help gambling'\n"
                       "For more infor on transfers, use; '>help transfer'",
                 inline=False)
    em.add_field(name="How do i Use it?",
                 value=f"You can use your wallet to transfer money to others.\n"
                       f"For more info on transfers, use; '>help transfer'",
                 inline=False)
    em.add_field(name="How do i move money to and from my Bank accounts?",
                 value="To learn how to move money between accounts, use; '>help withdraw' or '>help deposit'\n",
                 inline=False)

    await ctx.send(embed=em)

@help.command()
async def beg(ctx):
    em = discord.Embed(title="Begging", description=f"{'Beg for money if you dont got any.' if randint(0,10)!=1 else f'No money {bot.get_emoji(977639838641688596)} ?'}", color=c.purple())
    em.add_field(name="Usage",value="'>beg'",inline=False)
    em.add_field(name="Description",
                 value="You can get for money and earn between $10 and $75.\n"
                       f"Note that you can only beg if you have less than ${poverty_line} in both your wallet and in both bank account balances.\n"
                       f"This means that if you have more than ${poverty_line} in any of your account balances or wallet, you cannot beg.\n\n"
                       f"For more info on accounts, use; '>help accounts'\n"
                       f"For more info on your wallet, use; '>help wallet'",
                 inline=False)

    await ctx.send(embed=em)

@help.command()
async def coin_flip(ctx):
    em = discord.Embed(title="Coin Flip", description=f"{'Flip a coin and gamble money' if randint(0,10)!=1 else 'Ah... making life decisions on the flip of a coin. a smart chap, arent ya? ya bloody wanker'}", color=c.purple())
    em.add_field(name="Usage",
                 value="'>coin_flip [**heads or tails**] [**amount**]' or '>flip [**heads or tails**] [**amount**]' or '>cf [**heas or tails**] [**amount**]'",
                 inline=False)
    em.add_field(name="Description",
                 value=f"Choose either heads or tails(or 'h'/'t') and bet an amount of money from your wallet.\n"
                       f"If your guess is correct, you win that amount.\n"
                       f"If you lose, you lose that amount.\n\n"
                       f"For more info on your wallet, use; '>help wallet'",
                 inline=False)

    await ctx.send(embed=em)

@help.command()
async def lower(ctx):
    em = discord.Embed(title="Lower",
                       description=f"{'Choose a number and gamble money' if randint(0, 10) != 1 else f'Lower? yeah thats where my stocks been going {bot.get_emoji(980704198637281290)}'}", color=c.purple())
    em.add_field(name="Usage",
                 value="'>lower [**guess**] [**amount**]' or '>low [**guess**] [**amount**]'",
                 inline=False)
    em.add_field(name="Description",
                 value=f"Choose a number form 1-99 and bet an amount of money from your wallet.\n"
                       f"The bot generates a number form 0-100.\n"
                       f"If your number is lower than that bot's, you win that amount. if your number is higher than 65, you win more money proportional to how high your number was\n"
                       f"If you lose, you lose that amount.\n\n"
                       f"For more info on your wallet, use; '>help wallet'",
                 inline=False)

    await ctx.send(embed=em)



# GAMBLING COMMANDS ========================================================================#


@bot.command()
async def beg(ctx):
    """
    Command that lets the user beg for more money.

    The user can only use this command if they have less money than the poverty line in both wallet and bank accounts.

    Examples:
        poverty_line =50

        user.wallet = 40
        user.bank.tfa.balance = 40
        user.bank.ntfa.balance = 40
        >>>beg()

        user.wallet = 40
        user.bank.tfa.balance = 51
        user.bank.ntfa.balance = 40
        will not beg.
    """

    if ctx.author.bot: return

    user = User(ctx.author.id)

    em = discord.Embed(title="Beg for money", color=c.yellow())

    # verifies if the user is poor enough
    # only works if the user has less than the poverty line
    if (user.wallet > poverty_line or
        user.accounts["tfa"]["balance"] > poverty_line or
            user.accounts["ntfa"]["balance"] > poverty_line):
        em.add_field(name="Error",
                     value=f"You have too much money!\n"
                           f" You must have less than ${poverty_line} in both your bank accounts and wallet!\n"
                           f"run '>bal' to determine how much money you have.",
                     inline=False)

    else: # otherwise gives the user money

        amount = randint(10, 75)
        user.wallet += amount
        user.save()

        if randint(1,10) ==1: # no money ?
            msg = f"No money {bot.get_emoji(977639838641688596)} ?"
        else: msg = "You begged for money"

        em.add_field(name=msg, value=f"You begged and earned ${amount}")

    await ctx.send(embed=em)

@bot.command(aliases=["flip", "cf"])
@commands.cooldown(20, 30, commands.BucketType.user) # max usage of 20 times and have to wait 30 seconds afterward
async def coin_flip(ctx, guess:str, amount:float):
    """
    Coinflip command.

    the user guesses either heads or tails and bets a certain amount.
    if the user's guess is the same as the coin, they earn :amount: dollars
    if they lose, they lose :amount: dollars
    """

    if ctx.author.bot: return # dosent answer to bots

    em = discord.Embed(title="Coin Flip",color=c.green())
    user = User(ctx.author.id)

    # the user can only gamble positive amounts of money
    if amount <= 0:
        em.add_field(name="Error",
                     value="Must bet a positive amount of money",
                     inline=False)
        await ctx.send(embed=em)
        return

    # checks if the user has enough money
    if amount > user.wallet:
        if randint(1,10) ==1: # no money ?
            msg = f"No money {bot.get_emoji(977639838641688596)} ?"
        else: msg = "Error"

        em.add_field(name=msg,
                     value=f"Not enough money to gamble.",
                     inline=False)
        em.add_field(name="Has:",
                     value=f"${user.wallet}",
                     inline=False)
        em.add_field(name="Needs:",
                     value=f"${amount}",
                     inline=False)
        await ctx.send(embed=em)
        return

    # checks if the guess is formatted right
    if guess.lower() not in ["tails", "t", "heads", "h"]:
        em.add_field(name="Error",
                     value=f"Must format guess properly!\n"
                           f"Must look like: 'tails', 't', 'heads', 'h'\n"
                           f"You guessed: {guess}",
                     inline=False)
        await ctx.send(embed=em)
        return

    # rolls the dice
    if randint(1,2) == 1:
        user.wallet += amount
        em.add_field(name="You Won!",
                     value=f"You gained ${amount}!",
                     inline=False)
    else:
        user.wallet -=amount
        em.add_field(name="You Lost!",
                     value=f"You lost ${amount}!",
                     inline=False)

    user.save() # saves the user
    await ctx.send(embed=em)

@bot.command(asliases=['low'])
@commands.cooldown(20, 30, commands.BucketType.user) # max usage of 20 times and have to wait 30 seconds afterward
async def lower(ctx, guess:int, amount:float):
    """
    Lower/Upper command.

    The user guesses a number from 1-99(guess) and bets a certain amount(amount).
    The computer also generates a number from 0-100(reference).
    if guess is higher than referece, deduct amount from the user wallet.
    otherwise, depending on how high your vote was, add multiples of amount to the wallet.
    """

    if ctx.author.bot: return # dosent answer to bots

    em = discord.Embed(title="Lower",color=c.green())
    user = User(ctx.author.id)

    # the user can only gamble positive amounts of money
    if amount <= 0:
        em.add_field(name="Error",
                     value="Must bet a positive amount of money",
                     inline=False)
        await ctx.send(embed=em)
        return

    # checks if the user has enough money
    if amount > user.wallet:
        if randint(1, 10) == 1:  # no money ?
            msg = f"No money {bot.get_emoji(977639838641688596)} ?"
        else:
            msg = "Error"

        em.add_field(name=msg,
                     value=f"Not enough money to gamble.",
                     inline=False)
        em.add_field(name="Has:",
                     value=f"${user.wallet}",
                     inline=False)
        em.add_field(name="Needs:",
                     value=f"${amount}",
                     inline=False)
        await ctx.send(embed=em)
        return

    # the user's guess must fall between [1-99]
    if guess >99 or guess < 1:
        em.add_field(name="Error",
                     value="Value must be within 1-99",
                     inline=False)
        await ctx.send(embed=em)
        return

    reference = randint(0,100) # the number generated by the computer.

    if guess <= reference: # if the user number is less than the generated on, the user wins
        won=True
        # if less than 35, give 0.25x less for every 5 points lower
        if guess < 35:
            change = max(1, int(amount + (0.05*(guess - 35)*amount) ) )
            user.wallet += change

        # if higher than 65, 0.25x more for every 5 points higher
        elif guess > 65:
            change = int(amount + (0.05*(guess - 65) * amount))
            user.wallet += change

        else: # otherwise
            change = amount
            user.wallet += change

    else: # if the user num is higher, then they lose money
        won=False
        change = amount
        user.wallet -= change

    # make the embed
    em.add_field(name=f"You {'Won' if won else 'Lost'} {'' if won else '' if randint(0,10)!=1 else bot.get_emoji(980704152550277152)}!",
                 value=f"You guessed: {guess}\nThe reference was: {reference}",
                 inline=False)
    em.add_field(name=f"You {'Gained' if won else 'Lost'}:",
                 value=f"{change} coins!",
                 inline=False)
    em.add_field(name="Wallet",
                 value=f"You now have: {round(user.wallet,4)} coins!",
                 inline=False)
    em.add_field(name=f"{'Congratulations!' if won else 'Better luck next time!'}",
                 value=f"Be sure to gimme more money- I MEAN, play again!!",
                 inline=False)

    user.save() # saves
    await ctx.send(embed=em) # sends the embed


# GENERAL ECONOMY COMMANDS =================================================================#


@bot.command(aliases=["d"])
@commands.cooldown(1, 86400, commands.BucketType.user) # only used once per day.
async def daily(ctx): # daily command to give the user money into their wallet

    if ctx.author.bot: return  # does not answer to bots

    user = User(ctx.author.id)
    amount = randint(150, 600) # range 150-600 bucks
    user.wallet += amount
    user.save()

    # creates the embed.
    em = discord.Embed(title="Daily Money",
                       description=f"You recived **${amount}** the money has been deposited into your wallet", color=c.orange())

    await ctx.send(embed=em)

@bot.command(aliases=["start"])
async def init(ctx): # creates an account

    if ctx.author.bot: return  # does not answer to bots

    User(ctx.author.id) # loads up the user

    em = discord.Embed(title="Created your account.", color=c.orange())

    await ctx.send(embed=em)

@bot.command(aliases=["b", "balance"])
async def bal(ctx): # gives the current balance

    if ctx.author.bot: return # does not answer to bots

    user = User(ctx.author.id)

    em = discord.Embed(title="User Balance", color=c.orange())
    em.add_field(name="Wallet", value=f"${round(user.wallet, 4)}", inline=False)
    em.add_field(name="TFA", value=f"${round(user.accounts['tfa']['balance'], 4)}", inline=False)
    em.add_field(name="NTFA", value=f"${round(user.accounts['ntfa']['balance'],4)}", inline=False)

    await ctx.send(embed=em)

@bot.command(aliases=["investments", "i"])
async def holdings(ctx, account_name=None):
    """
    Views the user's holdings.

    By default, shows both. however, if specified, it will show a specific account's investments.

    depending on which account whose holdings we want, we can load holdings_list() which loads all
    holdings in an account and equates it to msg. we can then return msg
    """
    async def holdings_list(user:User, account_name:str):
        # loads all holdings in a user's account
        value = ""
        for holding in user.accounts[account_name]["holdings"]:
            value += f"{holding}: {user.accounts[account_name]['holdings'][holding]}\n"

        # embeds cannot contain empty strings, so if there are no holdings, say that there are no holdings
        if value == "":
            return "No holdings"
        else: return value

    if ctx.author.bot: return  # does not answer to bots

    user = User(ctx.author.id) # loads the user
    em = discord.Embed(title="User Holdings", color=c.orange()) # the embed used.

    if account_name is None: # load all accounts if nothing is specified
        em.add_field(name="TFA",
                     value=await holdings_list(user, "tfa"),
                     inline=False)
        em.add_field(name="NTFA",
                     value=await holdings_list(user, "ntfa"),
                     inline=False)

    elif account_name.lower() == "tfa": # for the tax-free account
        em.add_field(name="TFA",
                     value=await holdings_list(user, account_name))

    elif account_name.lower() == "ntfa": # for the non-tax-free account
        em.add_field(name="NTFA",
                     value=await holdings_list(user, account_name))


    await ctx.send(embed=em) # returns the message

@bot.command(aliases=["t"])
async def transfer(ctx, amount:float, member:discord.Member):
    """
    Transfers money from 1 wallet to the next.

    only accepts non-zero positive values. then it calls the user.transfer() method
    afterward saves.
    """

    if ctx.author.bot: return  # does not answer to bots

    user = User(ctx.author.id)

    em = discord.Embed(title="Transfer Money", color=c.orange())

    if amount<=0.0: # amount has to be greater than 0
        em.add_field(name="Transfer", value="Amount must be a positive number")
        await ctx.send(embed=em)
        return
    if amount > max_transfer_limit: # amount exceeds the trtansfer limit
        em.add_field(name="Error", value="Exceeds transfer limit", inline=False)
        em.add_field(name="max limit:", value=f"${max_transfer_limit}", inline=False)
        em.add_field(nmae="To send:", value=f"${max_transfer_limit}", inline=False)
        await ctx.send(embed=em)
        return

    msg = user.transfer(amount=amount, uid=member.id)

    em.add_field(name="Transfer", value=msg)

    await ctx.send(embed=em)

    user.save() # saves the user

@bot.command(aliases=["bw"])
async def withdraw(ctx, account_name:str, amount:float):
    """
    Withdraws money from the user's bank account.

    The user specifies a non-zero positive amount of money and which bank account to
    choose from. the bank account can be either tfa or ntfa.
    afterward, it just calls the user.withdraw() method

    """

    if ctx.author.bot: return  # does not answer to bots

    em = discord.Embed(title="Bank Withdraw", color=c.orange())

    if amount <=0.0:
        em.add_field(name="Error", value="Amount must be a positive number")
        await ctx.send(embed=em)
        return

    user = User(ctx.author.id)
    msg= user.bank_withdraw(amount=amount, account_name=account_name.lower())
    em.add_field(name="Withdraw", value=msg)
    await ctx.send(embed=em)

    user.save()

@bot.command(aliases=["bd"])
async def deposit(ctx, account_name: str, amount: float):
    """
    deposits money into the user's bank account.

    The user specifies a non-zero positive amount of money and which bank account to
    choose from. the bank account can be either tfa or ntfa.
    afterward, it just calls the user.deposit() method

    """

    if ctx.author.bot: return  # does not answer to bots

    em = discord.Embed(title="Bank Deposit", color=c.orange())

    if amount <= 0.0:
        em.add_field(name="Error", value="Amount must be a positive number")
        await ctx.send(embed=em)
        return

    user = User(ctx.author.id)
    msg= user.bank_deposit(amount=amount, account_name=account_name.lower())
    em.add_field(name="Deposit", value=msg)
    await ctx.send(embed=em)

    user.save() # saves


# CRYPTO COMMANDS =================================================================#


@bot.command(aliases=["v"])
async def view(ctx, coin_name:str): # view info on a specific currency
    """
    Displays information on a specific currency
    """

    if ctx.author.bot: return  # does not answer to bots

    em = discord.Embed(title=f"{coin_name} analytics", color=c.blue())

    # looks through the cache for the currency with the same name. if it matches, return it
    for currency_dict in crypto_cache:
        if currency_dict["name"] == coin_name.lower():
            coin = CryptoCurrency(currency_dict)
            em.add_field(name="Value", value=f"${round(coin.value,4)}", inline=False)
            em.add_field(name="Total coins", value=f"{coin.total_shares} coins", inline=False)
            em.add_field(name="Market cap", value=f"${round(coin.market_cap,4)}", inline=False)
#            msg += f"{coin.name}:    Value: ${coin.value}, Total coins: ${coin.total_shares}, Market cap: ${coin.market_cap}"
            break


    await ctx.send(embed=em)

@bot.command(aliases=["l"])
async def list(ctx): # view a list of all currencies and their values
    """
    Loads all the currencies from the cache and displays their details.
    """

    if ctx.author.bot: return  # does not answer to bots

    msg = ""
    em = discord.Embed(title="List cryptocurrencies", color=c.blue())
    for currency_dict in crypto_cache: # goes through all currencies
        coin = CryptoCurrency(currency_dict)
        msg += f"{coin.name}  -  ${round(coin.value,4)}\n"

    em.add_field(name="Currencies", value=msg)
    await ctx.send(embed=em)

@bot.command(aliases=["purchase", "p"])
@commands.cooldown(1, 15, commands.BucketType.user) # only used once per 15 seconds
async def buy(ctx, account_name:str, coin_name:str, shares:int): # buy a currency
    """
    Buys shares of a cryptocurrency.

    Checks if the number of shares is a non-zero positive number greater than 1. if not, return. if the shares are valid,
    we check if the currency exists in the cache. If it does, we can calculate the value of the purchase,
    how much the coin will now cost, and what the total with taxes will be.
    Finally, we make some final checks to see if the purchase is valid. (has enough money, dosent exceed limits)
    then we can make the purchase and save.

    When calculating the value, it is compounded. we calculate the value of the currency and purchase 50 shares at a time.
    This way, the cost of the purchase is more accurate and higher than if it was all calculated in 1 sitting.
    we have temp variables like v and shares_traded so we know how much has been traded so far.
    v is gradually increased every iteration and after the loop, is assigned to coin.value. meanwhile, shares_traded is
    in case the value crashes or reaches the maximum value before it finishes calculations. this way, the value does not
    go out of hand and the user is not charged unjustly.
    """

    if ctx.author.bot: return  # does not answer to bots

    em = discord.Embed(title="Purchase", color=c.blue()) # sale

    if shares <1: # ensures the number of shares bought is at least 1
        em.add_field(name="Error", value="You must purchase at least 1 share.")
        await ctx.send(embed=em)
        return

    shares = floor(shares) # makes sure all shares bought are int. not float.
    user = User(ctx.author.id)  # loads the user

    if user.shares_exceeds_trade_limit(shares): # if the user has attempted to trade more shares than they are allowed to.
        em.add_field(name="Error", value="Shares exceed trading limit.", inline=False)
        em.add_field(name="To buy:", value=f"{shares}", inline=False)
        em.add_field(name="Max:", value=f"{trading_limit_shares}", inline=False)
        await ctx.send(embed=em)
        
        return

    if not CryptoCurrency.exists(coin_name): # checks if the coin exists. if so, load up the coin
        em.add_field(name="Error", value=f"Crypto curency: {coin_name} does not exist")
        await ctx.send(embed=em)
        return
    else:
        coin = CryptoCurrency(CryptoCurrency.load_coin_dict(coin_name))



    # calculates the volume of the purchase
    subtotal = 0
    shares_traded = 0 # keeps track of the number of shares you buy
    v = coin.value # v keeps track of the value as we calculate the purchase
    shares_total = shares # the total number of shares bought
    # so as long as shares > 0, this loop will continue to run. or so long as the value dosent crash or surpass the
    # maximum value.
    while (shares > 0 and v> coin.delete_value and v < coin.max_value):

        deduted_shares = min(shares_per_interval, shares) # the number of shares we calculate per iteration

        v = coin.calc_value(v, deduted_shares, buying=True) # given the number of shares, calculate the new v
        subtotal += coin.calc_cost(v, deduted_shares) # calculates the subtotal given v and the number of shares

        shares -= deduted_shares # subtracts the number of shares we used this iteration
        shares_traded += deduted_shares # increment the number of shares traded

    # calculates the total. including taxes if applicable
    total = user.calc_tax(account_name=account_name, subtotal=subtotal)



    # a number of checks to ensure the purchase is valid
    if not user.has_enough_balance(account_name=account_name, cost=total): # if the user cannot afford to pay
        em.add_field(name="Error", value="Does not have enough money.", inline=False)
        em.add_field(name="Has:", value=f"${round(user.accounts[account_name]['balance'],4)}", inline=False)
        em.add_field(name="Needs:", value=f"${round(total,4)}", inline=False)
        em.add_field(name="Shares you can afford:", value=f"{int(user.accounts[account_name]['balance'] / coin.value)}", inline=False)
        await ctx.send(embed=em)
        """await ctx.send(f"Does not have enough money\n"
                 f"Has: {user.accounts[account_name]['balance']}\n"
                 f"needs: {total}\n"
                 f"Shares you can afford: {int(user.accounts[account_name]['balance'] / coin.value)}")"""
        return

    if user.volume_exceeds_trade_limit(account_name=account_name, volume=subtotal): # if the volume of the purchase exceeds the limit
        # uses subtotal instead of total
        em.add_field(name="Error", value="Subtotal exceeds trading limit.", inline=False)
        em.add_field(name="Subtotal:", value=f"${round(subtotal,4)}", inline=False)
        em.add_field(name="Limit:", value=f"${taxed_trading_limit_dollars if account_name=='ntfa' else tax_free_trading_limit_dollars}", inline=False)
        """await ctx.send(f"subtotal exceeds trading limit\n"
                 f"subtotal: {subtotal}\n"
                 f"limit: {taxed_trading_limit_dollars if account_name=='ntfa' else tax_free_trading_limit_dollars}")"""
        await ctx.send(embed=em)
        return

    # if all those checks are passed, then make the purchase
    user.modify_account(account_name=account_name, amount=-total) # when buying, amount is (-)
    coin.change_currency_value(v) # changes the value of the currency
    user.increase_holding(account_name=account_name, coin_name=coin_name, shares=shares_traded) # modifies the holding



    coin.should_delete() # checks if the coin has crashed.

    # saves
    coin.save()
    user.save()

    # the embed showing success
    em.add_field(name="Success", value=f"Successfully purchased {shares_traded} coin/s of {coin_name} for ${round(total,4)}")

    await ctx.send(embed=em)

@bot.command(aliases=["s"])
@commands.cooldown(1, 15, commands.BucketType.user) # only used once per 15 seconds
async def sell(ctx, account_name:str, coin_name:str, shares:int): # sell a currency
    """
    Sells shares of a cryptocurrency.

    Checks if the number of shares is a non-zero positive number greater than 1. if not, return. if the shares are valid,
    we check if the currency exists in the cache. If it does, we can calculate the value of the sale,
    how much the coin will now cost, and what the total with taxes will be.
    Finally, we make some final checks to see if the sale is valid. (has enough shares, dosent exceed limits)
    then we can make the sale and save.

    When calculating the value, it is compounded. we calculate the value of the currency and sales 50 shares at a time.
    This way, the cost of the sale is more accurate than if it was all calculated in 1 sitting.
    we have temp variables like v and shares_traded so we know how much has been traded so far.
    v is gradually increased every iteration and after the loop, is assigned to coin.value. meanwhile, shares_traded is
    in case the value crashes or reaches the maximum value before it finishes calculations. this way, the value does not
    go out of hand and the user is not charged unjustly.
    """

    if ctx.author.bot: return  # does not answer to bots

    em = discord.Embed(title="Sale", color=c.blue()) # the embed

    if shares <1: # ensures the number of shares bought is at least 1
        em.add_field(name="Error", value="You must purchase at least 1 share.")
        await ctx.send(embed=em)
        return

    shares = floor(shares) # makes sure all shares bought are int. not float.
    user = User(ctx.author.id)  # loads the user

    # if the user has attempted to trade more shares than they are allowed to.
    if user.shares_exceeds_trade_limit(shares):
        # uses the shares_total
        em.add_field(name="Error", value="Shares exceed trading limit.", inline=False)
        em.add_field(name="To buy:", value=f"{shares}", inline=False)
        em.add_field(name="Max:", value=f"{trading_limit_shares}",inline=False)
        await ctx.send(embed=em)
       
        return

    if not CryptoCurrency.exists(coin_name): # checks if the coin exists. if so, load up the coin
        em.add_field(name="Error", value=f"Crypto curency: {coin_name} does not exist")
        await ctx.send(embed=em)
        return
    else:
        coin = CryptoCurrency(CryptoCurrency.load_coin_dict(coin_name))



    # calculates the volume of the purchase
    subtotal = 0
    shares_traded = 0 # keeps track of the number of shares you buy
    v = coin.value # v keeps track of the value as we calculate the purchase
    shares_total = shares # the total number of shares bought
    # so as long as shares > 0, this loop will continue to run. or so long as the value dosent crash or surpass the
    # maximum value.
    while (shares > 0 and v> coin.delete_value and v < coin.max_value):

        deduted_shares = min(shares_per_interval, shares) # the number of shares we calculate per iteration

        v = coin.calc_value(v, deduted_shares, buying=True) # given the number of shares, calculate the new v
        subtotal += coin.calc_cost(v, deduted_shares) # calculates the subtotal given v and the number of shares

        shares -= deduted_shares # subtracts the number of shares we used this iteration
        shares_traded += deduted_shares # increment the number of shares traded



    # a number of extra checks to make sure the trade is valid
    if not user.has_enough_shares(account_name=account_name, coin_name=coin_name, shares=shares_total):
        # uses shares_total
        em.add_field(name="Error", value="Not enough shares to sell.", inline=False)
        em.add_field(name="To Sell:", value=f"{shares_total}",inline=False)
        em.add_field(name="Has:", value=f"{user.accounts[account_name]['holdings'][coin_name]}", inline=False)
        await ctx.send(embed=em)
        """await ctx.send(f"not enough shares to sell\n"
                 f"to sell: {shares_total}\n"
                 f"has: {user.accounts[account_name]['holdings'][coin_name]}")"""
        return

    # if the volume of the purchase exceeds the limit
    if user.volume_exceeds_trade_limit(account_name=account_name,volume=subtotal):
        # uses subtotal instead of total
        em.add_field(name="Error", value="Subtotal exceeds trading limit.", inline=False)
        em.add_field(name="Subtotal:", value=f"${round(subtotal,4)}", inline=False)
        em.add_field(name="Limit:", value=f"${taxed_trading_limit_dollars if account_name=='ntfa' else tax_free_trading_limit_dollars}", inline=False)
        await ctx.send(embed=em)
        """await ctx.send(f"subtotal exceeds trading limit\n"
                 f"subtotal: {subtotal}\n"
                 f"limit: {taxed_trading_limit_dollars if account_name=='ntfa' else tax_free_trading_limit_dollars}")"""
        return

    # sets the new balance. if it passes the limit, it caps it
    user.cap_balance(account_name=account_name,amount=subtotal)
    coin.change_currency_value(v)  # changes the value of the currency
    user.decrease_holding(account_name=account_name, coin_name=coin_name,shares=shares_traded)  # modifies the holding



    coin.should_delete()  # checks if the coin has crashed.

    # saves
    coin.save()
    user.save()

    # the embed for successful trades
    em.add_field(name="Success", value=f"Successfully sold {shares_traded} coin/s of {coin_name} for ${round(subtotal,4)}")

    await ctx.send(embed=em)


# SUBPROCESSES =================================================================#

"""@bot.event
async def on_message(message): # if kuki annoys me, reply
    if "krypto bot where" in message.content.lower():
        await message.channel.send("here")"""


# Run command and all the subprocesses
# subprocesses:
#   simulate all currencies
#   add new currencies if need be
#   reload constants
#   add shares
#   print cache
#   change status?
simulate_cache.start()
add_currencies.start()
reload_constants.start()
add_shares.start()
print_cache.start()
# changes status

bot.run(imp_info["token"]) # runs the bot
