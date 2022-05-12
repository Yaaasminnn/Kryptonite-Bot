# keeps track of all constants
# these constants can be used throughout the program but can also be changed on the fly
# we import the variables from a json file and then can load them anywhere
import os

from src.utils.json_utils import *
from discord.ext.tasks import loop

# the actual constants
constants = load_json("src/kryptonite_bot/constants.json")
max_transfer_limit = constants["max transfer limit"]
trading_limit_shares = constants["trading limit shares"]
tax_free_trading_limit_dollars = constants["tax free trading limit dollars"]
taxed_trading_limit_dollars = constants["taxed trading limit dollars"]
tax_rate = constants["tax rate"]
start_amount = constants["start amount"]
max_balance = constants["max balance"]
max_market_cap = constants["max market cap"]
shares_per_interval = constants["shares per interval"]
min_coins = constants["min_coins"]
max_coins = constants["max_coins"]

@loop(minutes=1)
async def reload_constants():
    """
    Loads constants that are used.

    These are in a json so they can easily be permanently changed during runtime.
    """
    global tax_rate, tax_free_trading_limit_dollars, trading_limit_shares, max_transfer_limit, start_amount, \
        taxed_trading_limit_dollars, max_balance, max_market_cap, shares_per_interval, min_coins, max_coins
    constants = load_json("src/kryptonite_bot/constants.json")
    max_transfer_limit = constants["max transfer limit"]
    trading_limit_shares = constants["trading limit shares"]
    tax_free_trading_limit_dollars = constants["tax free trading limit dollars"]
    taxed_trading_limit_dollars = constants["taxed trading limit dollars"]
    tax_rate = constants["tax rate"]
    start_amount = constants["start amount"]
    max_balance = constants["max balance"]
    max_market_cap = constants["max market cap"]
    shares_per_interval = constants["shares per interval"]
    min_coins = constants["min_coins"]
    max_coins = constants["max_coins"]

async def change_constants(constant_name, value):
    """
    Changes the value of a constant.

    constants are stored in src/kryptonite_bot/constants.json

    these values are meant to be used globally but can be changed and reloaded on the fly.

    Takes in the name of the constant we want to change, as well as a new value for it. then, if the constant exists,
    change it. additionally, we modify the actual json file.
    """
    constants = load_json("src/kryptonite_bot/constants.json") # loas the constants

    if not key_exists(constants, constant_name):
        return f"{constant_name} does not exist."

    old_val = constants[constant_name] # gets the old value
    constants[constant_name] = value # changes the value of the constant

    update_json("src/kryptonite_bot/constants.json", constants) # updates the json

    return f"changed **{constant_name}**'s value from **{old_val}** to **{value}** successfully."



def reload_constants_sync():
    """
    Loads constants that are used.

    These are in a json so they can easily be permanently changed during runtime.
    """
    global tax_rate, tax_free_trading_limit_dollars, trading_limit_shares, max_transfer_limit, start_amount, \
        taxed_trading_limit_dollars, max_balance, max_market_cap, shares_per_interval, min_coins, max_coins
    constants = load_json("src/kryptonite_bot/constants.json")
    max_transfer_limit = constants["max transfer limit"]
    trading_limit_shares = constants["trading limit shares"]
    tax_free_trading_limit_dollars = constants["tax free trading limit dollars"]
    taxed_trading_limit_dollars = constants["taxed trading limit dollars"]
    tax_rate = constants["tax rate"]
    start_amount = constants["start amount"]
    max_balance = constants["max balance"]
    max_market_cap = constants["max market cap"]
    shares_per_interval = constants["shares per interval"]
    min_coins = constants["min_coins"]
    max_coins = constants["max_coins"]

def change_constants_sync(constant_name, value):
    """
    Changes the value of a constant.

    constants are stored in src/kryptonite_bot/constants.json

    these values are meant to be used globally but can be changed and reloaded on the fly.

    Takes in the name of the constant we want to change, as well as a new value for it. then, if the constant exists,
    change it. additionally, we modify the actual json file.
    """
    constants = load_json("src/kryptonite_bot/constants.json") # loas the constants

    if not key_exists(constants, constant_name):
        return f"{constant_name} does not exist."

    old_val = constants[constant_name] # gets the old value
    constants[constant_name] = value # changes the value of the constant

    update_json("src/kryptonite_bot/constants.json", constants) # updates the json

    return f"changed **{constant_name}**'s value from **{old_val}** to **{value}** successfully."
