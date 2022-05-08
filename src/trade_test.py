from utils.crypto_currency import *
from utils.users import *

# unit tests for buy/sell
# unit tests for each individual method
# finish up the needed methods. (add holding)

def exists_test(coin_name:str):
    # simulates if a coin exists
    print(CryptoCurrency.exists(coin_name))

def load_dict_test(coin_name:str):
    # tests CryptoCurrency.load_coin_dict()
    print(CryptoCurrency.load_coin_dict(coin_name))

def calc_value_test(coin:CryptoCurrency, shares:int):
    # calculates the value after buying a few shares
    print(coin.calc_value(coin.value,shares))

def calc_cost_test(coin:CryptoCurrency, shares:int):
    # the subtotal(cost) is simply the new value multiplied by the number of shares to purchase
    v = coin.calc_value(coin.value, shares)
    print(v)
    subtotal = coin.calc_cost(v, shares)
    print(subtotal)

def calc_taxes_test(user:User, coin:CryptoCurrency, shares:int):
    # the taxes add on 12% of the subtotal
    # there are 2 scenarios:
    #   tax-free: total = subtotal          account_name="tfa"
    #   taxed: total = 1.12 * subtotal      account_name="ntfa"
    v = coin.calc_value(coin.value, shares)
    print("value: ",v)

    subtotal = coin.calc_cost(v, shares)
    print("subtotal: ",subtotal)

    tax_free_total = user.calc_tax(account_name="tfa", subtotal=subtotal) # tax free
    print("tax-free total: ",tax_free_total)

    taxed_total = user.calc_tax(account_name="ntfa", subtotal=subtotal) # taxed
    print("taxed: ", taxed_total)

    print("tax rate: ",taxed_total / tax_free_total) # assurance which gives us the tax rate

    # only returned so i can use this in other tests
    return {'value':v, 'subtotal':subtotal, 'taxed_total':taxed_total, 'tax_free total': tax_free_total}

def conditions_test(user:User, account_name:str, subtotal:float, total:float, shares:int):
    # tests the entire block of conditions
    #
    # this command to test:
    #  tax_test = calc_taxes_test(user, coin, shares=50)
    #     print(conditions_test(user, account_name="tfa", subtotal=tax_test["subtotal"], total=tax_test['tax_free total'], shares=50))
    #
    # todo:
    #   rewrite these unit tests to be more specific and thorough. the stuff works, but the unit tests arent good
    print(total, user.accounts[account_name]["balance"])
    if not user.has_enough_balance(account_name=account_name, cost=total): return "Does not have enough money"
    if user.volume_exceeds_trade_limit(account_name=account_name, volume=subtotal): return "subtotal exceeds trading limit" # uses subtotal instead of total
    if user.shares_exceeds_trade_limit(shares): return "Shares exceed trading limit"

def modify_account_test(user:User, account_name:str, total:float, buying:bool):
    # modifies the account.
    # this has 2 scenarios:
    #    buying             total = -total
    #    selling            total = total
    # this is because we add the amount passed in. subtracting it means we are buying
    if buying: total = -total # if we are buying, make total negative
    user.modify_account(account_name, total)

def change_value_test(coin:CryptoCurrency, value):
    # this method just changes coin.value to the given value
    print("old value: ", coin.value)
    coin.change_currency_value(value)
    print("new value: ", coin.value)

def holding_exists_test(user:User, account_name:str, coin_name:str):
    # checks if the holding exists in the account specified by the user.
    print(user.holding_exists(account_name, coin_name))

def increase_holding_test(user:User, account_name:str, coin_name:str, shares:int):
    # increases the holding of a certain coin.
    # the points of failure are:
    #   adding a new coin
    #   modifying an existing one
    #   increments num_holding if adding a new one
    user.increase_holding(account_name, coin_name, shares)
    user.save()

def decrease_holding_test(user:User, account_name:str, coin_name:str, shares:int):
    # decreases the holding of a certain coin.
    # the points of failure are:
    #   when a holding drops below 0        (gets deleted)
    #   holding dosent drop below 0         (holding >0 and does not get deleted)
    #   holding reaches 0                   (gets deleted)
    #   decrements num_holding if the coin is deleted
    # dont cover if the currency dosent exist as it is handled in user.has_enough_shares()
    user.decrease_holding(account_name, coin_name, shares)
    user.save()

def buy_test(uid, account_name:str, coin_name:str, shares:int):

    user = User(uid) # loads up the user instance

    # if the coin does not exist, return, otherwise load up the currency instance.
    if CryptoCurrency.exists(coin_name) == False:
        return "Currency does not exist"
    else:
        coin = CryptoCurrency(CryptoCurrency.load_coin_dict(coin_name))

    # actually calculates the volume of the purchase
    subtotal = 0
    v= coin.value
    mod = shares % shares_per_interval
    shares_cpy = shares
    for i in range(5): # determine how many times this runs. this section's "shares" will be replaced
        v = coin.calc_value(v,shares) # given the number of shares, calculates the new value of v
        subtotal += coin.calc_cost(v, shares) # calculates the subtotal given v and the number of shares

        if shares_cpy >= shares_per_interval:
            shares_cpy -= shares_per_interval

    total = user.calc_tax(account_name=account_name, subtotal=subtotal)

    # a number of extra checks to make sure the trade is valid
    if not user.has_enough_balance(account_name=account_name, cost=total): return "Does not have enough money"
    if not user.volume_exceeds_trade_limit(account_name=account_name, volume=subtotal): return "subtotal exceeds trading limit" # uses subtotal instead of total
    if not user.shares_exceeds_trade_limit(shares): return "Shares exceed trading limit"

    user.modify_account(account_name=account_name, amount=total) # when buying, amount is +, selling, -
    coin.change_currency_value(v) # changes the value of the currency
    user.increase_holding(account_name=account_name, coin_name=coin_name, shares=shares) # modifies the holding

def sell_test(uid, account_name:str, coin_name:str, shares:int): pass


if __name__ == '__main__':
    #clear_db() # clears the cryptocurrency db

    coin = CryptoCurrency()
    user = User(1)

    coin.value = 25

    #user.accounts["tfa"]["holdings"][coin.name] = 5
    #user.save()
    name = "Ruby-Bags"
    increase_holding_test(user, "tfa", name, 15) # holding number

    #holding_exists_test(user, account_name="tfa", coin_name=coin.name)

    #user.save()