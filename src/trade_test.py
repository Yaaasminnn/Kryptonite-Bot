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

def calc_value_test(coin:CryptoCurrency, shares:int, buying:bool):
    # calculates the value after buying a few shares
    # scenarios:
    #   selling     value drops below 0
    #   buying      value reaches max_market cap / total_shares
    print(coin.calc_value(coin.value,shares, buying))

def calc_cost_test(coin:CryptoCurrency, shares:int, buying:bool):
    # the subtotal(cost) is simply the new value multiplied by the number of shares to purchase
    v = coin.calc_value(coin.value, shares, buying)
    print(v)
    subtotal = coin.calc_cost(v, shares)
    print(subtotal)

def calc_taxes_test(user:User, coin:CryptoCurrency, shares:int, buying:bool):
    # the taxes add on 12% of the subtotal
    # there are 2 scenarios:
    #   tax-free: total = subtotal          account_name="tfa"
    #   taxed: total = 1.12 * subtotal      account_name="ntfa"
    v = coin.calc_value(coin.value, shares, buying)
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
    #if buying: total = -total # if we are buying, make total negative
    user.modify_account(account_name, total, buying)

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

def has_enough_shares_test(user:User, account_name:str, coin_name:str, shares:int):
    # scenarios:
    #   doe not have a holding
    #   has a holing, not enough
    #   has a aholding, enough
    print(user.has_enough_shares(account_name, coin_name, shares))

def balance_exceeds_limit_test(user:User, account_name:str ,amount:float):
    # scenarios:
    #   does not exceed limit
    #   does
    print(user.balance_exceeds_limit(account_name, amount))

def cap_balance_test(user:User, account_name:str ,amount:float):
    # scenarios
    #   balance < limit
    # balance >= limit
    print(user.cap_balance(account_name, amount))

def buy_test(uid, account_name:str, coin_name:str, shares:int):
    # buying the currency.
    # checks if the currency exists first, if not return. if it does, load it up
    # proceeds to calculate the value. only calculating the cost/value shares_per_interval(or 50) at a time
    # or by the number of shares if it is less than shares_per_interval
    # during this time, we keep track of the number of shares traded. the number you pass in vs the number traded may be different
    # this is if the coin's value reaches 0 or passes the maximum limit
    # afterward, it simply calculates the total and modifies the user and currency data
    # scenarios:
    #    value is driven beyond max limit. to test this, set the max_market_cap 10 10k, total_shares to 100 and value to 100 or slightly lower



    user = User(uid) # loads up the user instance

    # if the coin does not exist, return, otherwise load up the currency instance.
    if CryptoCurrency.exists(coin_name) == False:
        return "Currency does not exist"
    else:
        coin = CryptoCurrency(CryptoCurrency.load_coin_dict(coin_name))



    # actually calculates the volume of the purchase
    subtotal = 0
    shares_traded = 0 # keeps track of the number of shares u traded
    v= coin.value
    shares_total = shares # keeps track of the total number of shares
    # determine how many times this runs. this section's "shares" will be replaced
    # runs so long as the value dosent crash nor rise beyond the max_value
    # also while the shares > 0 as they are deducted every iteration
    print("value", v)
    while (shares > 0 and (v > coin.delete_value and v < coin.max_value)):

        deducted_shares = min(shares_per_interval, shares)

        v = coin.calc_value(v,deducted_shares, buying=True) # given the number of shares, calculates the new value of v
        subtotal += coin.calc_cost(v, deducted_shares) # calculates the subtotal given v and the number of shares

        if shares >= shares_per_interval:
            shares -= shares_per_interval

        elif shares < shares_per_interval:
            shares = 0

        shares_traded += deducted_shares
        print("value: ", v)
        #print("shares: ", shares, "\nvalue: ", v, "\nshares traded: ", shares_traded, "\nsubtotal: ",subtotal, "\nmax: ", coin.max_value,"\n")

    total = user.calc_tax(account_name=account_name, subtotal=subtotal) # the total including taxes
    print("total", total)


    # a number of checks for:
    if not user.has_enough_balance(account_name=account_name, cost=total): # if the user cannot afford to pay
        return f"Does not have enough money\nHas: {user.accounts[account_name]['balance']}.\n needs: {total}"

    if user.volume_exceeds_trade_limit(account_name=account_name, volume=subtotal): # if the volume of the purchase exceeds the limit
        # uses subtotal instead of total
        return f"subtotal exceeds trading limit\nsubtotal: {subtotal}\nlimit: {taxed_trading_limit_dollars} {tax_free_trading_limit_dollars}"


    if user.shares_exceeds_trade_limit(shares_total): # if the user has attempted to trade more shares than they are allowed to.
        # uses the shares_total
        return f"Shares exceed trading limit. \nto buy: {shares_total}\nmax:{trading_limit_shares}"



    user.modify_account(account_name=account_name, amount=-total) # when buying, amount is +, selling, -
    coin.change_currency_value(v) # changes the value of the currency
    user.increase_holding(account_name=account_name, coin_name=coin_name, shares=shares_traded) # modifies the holding

    coin.should_delete()
    coin.save()
    user.save()

def sell_test(uid, account_name:str, coin_name:str, shares:int):
    # need to add user.has_enough_shares()
    # and user.balance_exceeds_limit()
    # remove user.has_enough_balance()
    # need to test
    # checks for unit tests of the afore mentioned
    # scenario:
    #   drive the value to 0

    user = User(uid)  # loads up the user instance

    # if the coin does not exist, return, otherwise load up the currency instance.
    if CryptoCurrency.exists(coin_name) == False:
        return "Currency does not exist"
    else:
        coin = CryptoCurrency(CryptoCurrency.load_coin_dict(coin_name))

    # actually calculates the volume of the purchase
    subtotal = 0
    shares_traded = 0  # keeps track of the number of shares u traded
    v = coin.value
    shares_total = shares  # keeps track of the total number of shares
    print("init value: ", v)
    while (shares > 0 and (v > coin.delete_value and v < coin.max_value)):  # determine how many times this runs. this section's "shares" will be replaced

        deducted_shares = min(shares_per_interval, shares)

        v = coin.calc_value(v, deducted_shares, buying=False)  # given the number of shares, calculates the new value of v
        subtotal += coin.calc_cost(v, deducted_shares)  # calculates the subtotal given v and the number of shares

        if shares >= shares_per_interval:
            shares -= shares_per_interval

        elif shares < shares_per_interval:
            shares = 0

        shares_traded += deducted_shares
        print("shares: ", shares, "\nvalue: ", v, "\nshares traded: ", shares_traded, "\nsubtotal: ", subtotal,"\n")



    # a number of extra checks to make sure the trade is valid------------

    if not user.has_enough_shares(account_name=account_name, coin_name=coin_name, shares=shares_total):
        # uses shares_total
        # if the coin does not exist in their holdings, it means they have no shares
        try: return f"not enough shares to sell\nto sell: {shares_total}\nhas: {user.accounts[account_name]['holdings'][coin_name]}"
        except KeyError: return f"You dont own {coin_name}"


    if user.volume_exceeds_trade_limit(account_name=account_name,volume=subtotal): # if the volume of the purchase exceeds the limit
        # uses subtotal instead of total
        return f"subtotal exceeds trading limit\nsubtotal: {subtotal}\nlimit: {taxed_trading_limit_dollars} {tax_free_trading_limit_dollars}"

    if user.shares_exceeds_trade_limit(shares_total): # if the user has attempted to trade more shares than they are allowed to.
        # uses the shares_total
        return f"Shares exceed trading limit. \nto buy: {shares_total}\nmax:{trading_limit_shares}"


    user.cap_balance(account_name=account_name, amount=subtotal) # sets the new balance. if it passes the limit, it caps it
    coin.change_currency_value(v)  # changes the value of the currency
    user.decrease_holding(account_name=account_name, coin_name=coin_name, shares=shares_traded)  # modifies the holding

    coin.should_delete()
    coin.save()
    user.save()

def buying_interval_test(shares:int):
    # determines the number of intervals when buying work.
    # takes in a certain number of shares, compares it to shares_per_interval
    # if it is lower than shares_per_interval, we deduct itself every iteration.
    # otherwise we deduct by shares_per_interval every iteration
    # scenarios:
    #   shares divisible by shares_per_interval. >=
    #   shares not divisible by shares_per_interval. >
    #   shares < shares_per_interval                    (dosent matter if divisble anyway)
    while shares > 0:

        deducted_shares = min(shares_per_interval, shares)

        print("shares: ", shares)
        print("deducted: ", deducted_shares)
        print("")

        if shares >= shares_per_interval:
            shares -= shares_per_interval

        elif shares < shares_per_interval:
            shares = 0

    print("shares: ", shares)
    #print("deducted: ", deducted_shares)
    print("")

if __name__ == '__main__':
    clear_db() # clears the cryptocurrency db
    load_db_into_cache_sync()

    coin = CryptoCurrency()
    coin.value = 50
    coin.save()
    #coin.value = 99
    #coin.total_shares = 100
    #coin.save()

    shares = 500_000

    #calc_value_test(coin, shares=shares, buying=True)

    print(buy_test(1, "tfa", crypto_cache[0]["name"], shares))

    #cap_balance_test(User(1), "ntfa", amount=100)

    #print(sell_test(1, "tfa", crypto_cache[0]["name"], shares=shares))