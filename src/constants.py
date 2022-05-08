# keeps track of all constants
# these constants can be used throughout the program but can also be changed on the fly
# we import the variables from a json file and then can load them anywhere
from src.utils.json_utils import *

# the actual constants
constants = load_json("kryptonite_bot/constants.json")
max_transfer_limit = constants["max transfer limit"]
trading_limit_shares = constants["trading limit shares"]
tax_free_trading_limit_dollars = constants["tax free trading limit dollars"]
taxed_trading_limit_dollars = constants["taxed trading limit dollars"]
tax_rate = constants["tax rate"]
start_amount = constants["start amount"]
max_balance = constants["max balance"]
max_market_cap = constants["max market cap"]
shares_per_interval = constants["shares per interval"]


def reload_constants():
    """
    Loads constants that are used.

    These are in a json so they can easily be permanently changed during runtime.
    """
    global tax_rate, tax_free_trading_limit_dollars, trading_limit_shares, max_transfer_limit, start_amount, \
        taxed_trading_limit_dollars, max_balance, max_market_cap, shares_per_interval
    constants = load_json("kryptonite_bot/constants.json")
    max_transfer_limit = constants["max transfer limit"]
    trading_limit_shares = constants["trading limit shares"]
    tax_free_trading_limit_dollars = constants["tax free trading limit dollars"]
    taxed_trading_limit_dollars = constants["taxed trading limit dollars"]
    tax_rate = constants["tax rate"]
    start_amount = constants["start amount"]
    max_balance = constants["max balance"]
    max_market_cap = constants["max market cap"]
    shares_per_interval = constants["shares per interval"]
