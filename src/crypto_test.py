import csv
import datetime

from utils.crypto_currency import *
import utils.json_utils
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
    """

    filename = "simulated_no_trade.csv"
    rows = []

    for i in range(time_period):
        db = utils.json_utils.load_json("db/crypto_currencies.json") # loads all currencies

        try:
            coin = CryptoCurrency(db["currencies"][0]) # creates the coin
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
    """
    filename = "simulated_with_trade.csv"
    rows = []

    for i in range(time_period):
        try:
            coin = CryptoCurrency(crypto_cache[0])

            # trades
            purchase = 0
            sale=0
            buyshares = randint(10_000,500_000)
            sellshares = randint(10_000, 500_000)
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

if __name__ == '__main__':
    db = utils.json_utils.load_json("db/crypto_currencies.json")

    for dict in db["currencies"]: # deletes all existing currencies
        #print(dict)
        coin = CryptoCurrency(dict)
        coin.delete()
    #update_json("db/crypto_currencies.json", db)

    new = CryptoCurrency()

    #print(new.total_shares)
    #print(new.value)
    #print(coin_buy(1_000_000, new))
    #print(new.value)

    simulate_with_trade(43200)

