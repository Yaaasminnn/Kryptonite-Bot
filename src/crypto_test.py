import csv
import datetime

from utils.crypto_currency import *
import utils.json_utils
from src.constants import *
"""
Tester for the Cryptocurrency class.
Dev: lvlon-Emperor
Date: 2022-04-25 2:30 am
objective:
    simulates a currency over the course of a month. assuming no trading.
    simulates a currency over the course of a month with trading.
    
    takes the results and outputs them to a .csv file
"""

fields = ["time(min)", "value", "sale", "purchase", "threshold", "Market cap", "number of shares"] # the fields used in the csv file

def simulate_notrade(time_period=10080):
    """
    Over the course of a month, simulate the currency.

    for loop that iterates for 43200 intervals(number of minutes in a month).
    in said loop, load database, load the first currency, simulate it and save, then repeat

    scenarios:
        value reaching self.max_value
    """

    filename = "simulated_no_trade.csv"
    rows = []

    for i in range(time_period):
        db = utils.json_utils.load_json("db/crypto_currencies.json") # loads all currencies

        try:
            coin = CryptoCurrency(db["currencies"][0])  # creates the coin
            coin.simulate() # simulates the coin

            rows.append([ # appends the values to the rows
                i,
                coin.value,
                coin.Vmax_mag,
                coin.Tmax_mag,
                coin.threshold,
                coin.market_cap,
                coin.total_shares
            ])

            print(f"Iteration: {i}    ||    Value: {coin.value}")
        except IndexError: print("Coin value crashed");break

    save_to_file(filename, rows)

def simulate_with_trade(time_period=10080):
    """
    Simulate the currency with trades.

    for loop that iterates for a given amount of intervals(number of minutes).
    In said loop, load the db, load a currency, trade and simulate it. then repeat.

    stress test:
        when buying pushes the value above the max limit
    """
    filename = "simulated_with_trade.csv"
    rows = []

    for i in range(time_period):
        try:
            coin = CryptoCurrency(crypto_cache[0])

            # trades
            purchase = 0
            sale=0
            buyshares = randint(100,1000)
            sellshares = randint(100, 1000)
            if randint(0,1440)==1: purchase =coin_buy(buyshares, coin)
            if randint(0,1440)==1: sale =coin_sell(sellshares, coin)

            coin.simulate()

            rows.append([  # appends the values to the rows
                i,
                coin.value,
                sale,
                purchase,
                coin.threshold,
                coin.market_cap,
                coin.total_shares
            ])
            print(f"Iteration: {i}    ||    Value: {coin.value}")
        except IndexError: print("Coin value crashed"); break

    save_to_file(filename, rows)

def coin_buy(shares:int, coin):
    #coin = CryptoCurrency(crypto_cache[cache_index])
    return coin.buy(coin.value * shares)

def coin_sell(shares:int, coin):
    return coin.sell(coin.value * shares)

def save_to_file(filename, rows):
    with open(f"tests/{filename}", "w") as file:
        writer = csv.writer(file) # creates the csv writer object

        # write the fields
        writer.writerow(fields)

        # write the data rows
        writer.writerows(rows)
    print(f"Saved {filename}!")

def exists_test():
    new = CryptoCurrency()
    name = new.name
    print(new.exists(name))

def load_db_into_cache_test():
    load_db_into_cache()

def add_currencies_test(): # tests adding currencies to the db
    add_currencies()
    db = load_json("src/db/crypto_currencies.json")
    print(db["count"])

def simulate_cache_test():
    simulate_cache()

if __name__ == '__main__':
    #clear_db()

    CryptoCurrency()

    #load_db_into_cache_test()

    #add_currencies_test()

    #simulate_cache_test()



