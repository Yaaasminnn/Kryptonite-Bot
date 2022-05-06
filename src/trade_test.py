from src.utils.crypto_currency import *
from src.utils.users import *

# unit tests for buy/sell
# unit tests for each individual method
# finish up the needed methods. (add holding)

def buy_test(uid, account_name:str, coin_name:str, shares:int):

    user = User(uid) # loads up the user instance

    # if the coin does not exist, return, otherwise load up the currency instance.
    if CryptoCurrency.exists(coin_name) == False:
        return "Currency does not exist"
    else:
        coin = CryptoCurrency(CryptoCurrency.exists(coin_name))

    # actually calculates the volume of the purchase
    subtotal = 0
    v= coin.value
    for: # determine how many times this runs.
        v = coin.calc_value(v,shares)
        subtotal += coin.calc_cost(v, shares)
    total = user.calc_tax(account_name=account_name, subtotal=subtotal)

    # a number of extra checks to make sure the trade is valid
    if not user.has_enough_balance(account_name=account_name, cost=total): return "Does not have enough money"
    if not user.volume_exceeds_trade_limit(account_name=account_name, volume=subtotal): return "subtotal exceeds trading limit" # uses subtotal instead of total
    if not user.shares_exceeds_trade_limit(shares): return "Shares exceed trading limit"

    user.modify_account(account_name=account_name, amount=total) # when buying, amount is +, selling, -
    coin.change_currency_value(v) # changes the value of the currency


def sell_test(uid, acount_name:str, coin_name:str, shares:int): pass


if __name__ == '__main__':
    clear_db() # clears the cryptocurrency db

    coin = CryptoCurrency()

    shares = int

    buy_test(1, account_name="tfa", coin_name=coin.name, shares=shares)
    sell_test(1, account_name="tfa", coin_name=coin.name, shares=shares)
