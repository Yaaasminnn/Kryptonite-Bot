import os
from src.utils.json_utils import *
import datetime
import asyncio
from src.constants import *
#from src.constants import tax_rate, taxed_trading_limit_dollars, tax_free_trading_limit_dollars, trading_limit_shares, \
#    max_transfer_limit, start_amount, max_balance

class User:
    def __init__(self, uid:int):
        """
        Initializes the User.

        Takes in the user id and loads the respective file in db/users/[uid].json.
        Then, we verify all tokens the user has still exist, if not, we delete the non-existent ones.
        finally, we update the last time this user was accessed.

        we do not save afterward and that is up to the user to save the data after use.
        this is because the user can do many things(trade, gamble, transfer) after accessing their account.
        Thus, the program must load the userdata, trade/gamble/transfer and then save seperately.
        """

        try: # assuming the user exists in the database, just load them l=normally
            user = load_json(f"db/users/{uid}.json")
            self.uid = uid
            self.wallet = user["wallet"]
            self.accounts = user["accounts"]
            self.last_accessed = user["last_accessed"]

        except: # if they dont exist, create them
            create_json(f"db/users/{uid}.json") # creates the user
            user = load_json(f"db/users/{uid}.json")
            self.uid = uid
            self.wallet = start_amount
            self.create_accounts() # creates all accounts
            self.update_last_accessed()

            self.save() # saves the user

        """try: # if the json file dosent already exist, create it
            self.user = load_json(f"db/users/{uid}.json")
        except:
            create_json(f"db/users/{uid}.json")
            self.user = load_json(f"db/users/{uid}.json")
            self.user["uid"] = uid
            self.user["wallet"] = start_amount
            self.create_accounts() # creates both crypto accounts

            # saves the user
            self.save()"""
        # verifies that all holdings they own still exist.
        # incase a coin crashes, the holdings will have no value anymore and are deleted.
        self.verify_holdings()
        self.update_last_accessed()

    def create_accounts(self):
        """
        Creates the 2 crypto accounts.

        Creates a Tax free account and a regular account.
        """
        accounts = {}
        accounts["ntfa"] =  {
                "tax_free": False,
                "name": "ntfa",
                "balance": 0,
                "holdings": {},
                "num_holdings": 0
            } # the Non-Tax Free Account; ntfa
        accounts["tfa"] = {
                "tax_free": True,
                "name": "tfa",
                "balance":0,
                "holdings": {},
                "num_holdings": 0
            } # the Tax Free Account; tfa

        self.accounts = accounts

    def obj_to_dict(self)->dict:
        """
        Transforms an object into a JSON dictionary to save.
        :return:
        """
        user = {}

        user["uid"] = self.uid
        user["wallet"] = self.wallet
        user["accounts"] = self.accounts
        user["last_accessed"] = self.last_accessed

        return user

    @staticmethod
    def clear_userbase(): # removes all users
        pass

    @staticmethod
    def clear_account(uid:int): # removes a user
        os.remove(f"db/users/{uid}.json")

    def dict_to_obj(self):pass

    def save(self):
        """
        Saves the Userdata.
        """
        user = self.obj_to_dict() # transforms the object to a dict

        update_json(f"db/users/{self.uid}.json", user)

    def verify_holdings(self):
        """
        Verifies that all the tokens in a user's holdings still exist.

        runs through all holdings in both accounts. for every token in the holdings,
        check if it exists in the database. if not, delete it from the holdings.
        """
        crypto_db = load_json("db/crypto_currencies.json")
        not_in_db=[]
        accounts = ["tfa", "ntfa"]

        for account in accounts:

            for holding in self.accounts[account]["holdings"]:
                in_db = False
                for crypto in crypto_db["currencies"]:
                    if holding == crypto["name"]:
                        in_db = True
                        break

                if not in_db:
                    not_in_db.append(holding)

            for holding in not_in_db:
                del_dict_key(self.accounts[account]["holdings"], key=holding)

            not_in_db = []

    def update_last_accessed(self):
        """
        Sets last_accessed to the current datetime.

        This is to keep track of the last time this user was accessed.
        :return:
        """
        self.last_accessed = str(datetime.datetime.now().replace(second=0, microsecond=0))

    def trade(self): pass

    def bank_deposit(self, amount:float, account_name:str):
        """
        Deposits the user's wallet into the bank account.

        There are no limits on how often/how much one can transfer from their own accounts.
        todo:
            add support for depositing/withdrawing all
        """
        if amount > self.wallet:
            return f"Insufficient wallet balance\nBalance: {self.wallet}\nNeeded: {amount}"

        self.wallet -=amount
        self.accounts[account_name]["balance"] += amount

    def bank_withdraw(self, amount:float, account_name:str):
        """
        Withdraws money from the bank account to the user's wallet.

        No limits on how often/how much can be withdrawn.
        """
        # determines which account
        if account_name == "tfa": account_index = 1
        else: account_index = 0

        if amount > self.accounts[account_name]["balance"]: # cannot exceed existing funds
            return f"Insufficient bank balance.\nBalance: {self.accounts[account_name]['balance']}\nNeeded: {amount}"

        self.accounts[account_name]["balance"] -= amount
        self.wallet += amount

    def c_buy(self, account_name:str, num:int, token_val:int, token_name:str):
        """
        Buy function. Modifies the user's balance.

        When buying the account's balance in decreased by the number of shares * the value of each token multiplied by
        the tax rate.

        First determines which account you are using. Tax free(tfa) or regular(ntfa). from there it determines the volume
        of the purchase with and without taxes as well as the tax rates. If the volume of the purchase without tax
        exceeds the trading limit(dollars), the order will be cancelled. also, if the volume(tax included) is greater
        than what the user has in their account, it will be cancelled as well. If a transfer goes through, deduct the
        money and add the holding to the account.

        Any other checks(currency exists, account exists, not exceeding the amount of shares.) will be handled in the
        bot's async method.
        """

        # determines which account to use. and calculates the value.
        if account_name == "tfa":
            account_index = 1
            volume = num*token_val
            volume_no_tax = volume
            if volume_no_tax > tax_free_trading_limit_dollars:  # the user cannot transfer more than the trading limit
                return f"Amount exceeds trading limit\nLimit: {tax_free_trading_limit_dollars}\nYour amount(without tax): {volume_no_tax}"
        else:  # if its a taxed account, tax them
            account_index = 0
            volume = tax_rate * (num*token_val) # the volume is calculated with tax
            volume_no_tax = volume/tax_rate
            if volume_no_tax > taxed_trading_limit_dollars:  # the user cannot transfer more than the trading limit
                return f"Amount exceeds trading limit\nLimit: {taxed_trading_limit_dollars}\nYour amount(without tax): {volume_no_tax}"


        # checks if the user's account balance is >= the volume of the purchase
        if self.accounts[account_index]["balance"] < volume:
            return f"Insufficient balance.\nBalance: {self.accounts[account_index]['balance']}\nNeeded: {volume}"

        # subtracts volume from the bank balance
        self.accounts[account_index]["balance"] -= volume

        # Adds the holdings to the account. if the holding does not exist, create it
        if token_name not in self.user["accounts"][account_index]["holdings"]:
            self.user["accounts"][account_index]["holdings"][token_name] = 0
            self.user["accounts"][account_index]["num_holdings"] +=1
        self.user["accounts"][account_index]["holdings"][token_name]+=num

    def c_sell(self, account_name:str, num:float, token_val:int, token_name:str):
        """
        Sell function. Modifies the user's account balance

        When selling, the account's balance is increased by the num_shares*token_val.
        additionally, the holding is decreased. if the holding volume reaches 0, the holding is deleted.
        """
        # determines which account to use.
        if account_name == "tfa": account_index = 1
        else: account_index = 0

        # checks that the user has enough shares to sell. if not generate an error code.
        shares_owned = self.user["accounts"][account_index]["holdings"][token_name]
        if num > shares_owned:
            return f"number of shares to sell exceeds number of shares owned.\nto sell: {num}\nowned:{shares_owned}"

        # adds the money to the bank balance
        self.user["accounts"][account_index]["balance"] += num*token_val # we take the min to ensure they dont sell more than they have

        # subtracts the number of shares sold from the account's holdings
        self.user["accounts"][account_index]["holdings"][token_name] -= num

        # if the number of owned tokens reach 0, remove it
        if self.user["accounts"][account_index]["holdings"][token_name] == 0:
            del_dict_key(self.user["accounts"][account_index]["holdings"], key=token_name)
            self.user["accounts"][account_index]["num_holdings"] -=1

    def wallet_modify(self): pass

    def bank_modify(self): pass

    def transfer(self, amount:float, uid:int):
        """
        Transfers money from one user to another.

        Transfers money from 1 wallet to the next. Withdraws the money from the user's wallet and deposits it into the
        recipient's wallet. Has to be within the maximum transfer amount

        The bot calling this function will determine needed.(positive integers only, who to ping etc)
        """
        if amount > max_transfer_limit: # cant  exceed the transfer limit.
            return f"Transfer amount exceeds transfer limit.\nTransfer limit: {max_transfer_limit}"

        if amount > self.wallet:
            return f"Insufficient funds to transfer.\n Your wallet: {self.wallet}\nAmount to send: {amount}"

        recipient = User(uid) # loads the recipient
        self.wallet -=amount
        recipient.wallet += amount
        recipient.save()

    def shares_exceeds_trade_limit(self, shares:int)->bool:
        """
        Determines if the number of shares exceed the trading limit.
        """
        if shares > trading_limit_shares: return True
        return False

    def volume_exceeds_trade_limit(self, account_name:str, volume:float)->bool:
        """
        Determines if the volume of the trade exceeds the trading limits.

        there are different trading limits depending on the account.
        """

        if account_name == "tfa":
            if volume > tax_free_trading_limit_dollars: return True
        elif account_name == "ntfa":
            if volume > taxed_trading_limit_dollars: return True
        return False

    def has_enough_balance(self, account_name:str, cost:float)->bool:
        """
        Determines if the user has enough money to cover a certain purchase.
        """
        return self.accounts[account_name]["balance"] >= cost

    def has_enough_shares(self, account_name:str, coin_name:str, shares:int)->bool:
        """
        determines if the user has enough shares to sell.

        we need the account name, what coin and how many shares we are selling.
        then we can just access that coin's holding in the right account and compare the number of shares.

        Also returns False if the user has no shares as the user does not have enough to sell.
        """

        # incase the user owns no shares, return False because they dont have enough to sell.
        if not self.holding_exists(account_name=account_name, coin_name=coin_name):
            return False
        else:
            return shares <= self.accounts[account_name]["holdings"][coin_name]


    def balance_exceeds_limit(self, account_name:str, amount:float)->bool:
        """
        Ensures that the user's bank account does not exceed the maximum balance.
        """
        if (self.accounts[account_name]["balance"] + amount) > max_balance: return True
        return False

    def modify_account(self, account_name:str, amount:float, buying:bool):
        """
        modifies a bank account with the given amount of money.

        is called after checking if the user can afford the purchase or sale.

        sales are positive
        purchases are negative
        """
        if not buying: self.accounts[account_name]["balance"] += amount
        else: self.accounts[account_name]["balance"] -= amount

    @staticmethod
    def calc_tax(account_name:str, subtotal:float):
        """
        Calculates the tax rate of a purchase given a subtotal.

        the user gives an account name, either tfa or ntfa. it is only taxed if it is a ntfa(non-tax free account)
        """
        if account_name == "tfa":
            return subtotal
        else:
            return tax_rate * subtotal

    def increase_holding(self, account_name:str, coin_name:str, shares:int):
        """
        Adds a holding in. used when buying

        checks if the holding exists, holding_exists(). if not, we add it.
        if it does, we simply add the currenct shares to it
        """
        if not self.holding_exists(account_name=account_name, coin_name=coin_name):
            self.accounts[account_name]["holdings"][coin_name] = shares
            self.accounts[account_name]["num_holdings"] += 1
        else:
            self.accounts[account_name]["holdings"][coin_name] += shares

    def holding_exists(self, account_name:str, coin_name:str)->bool:
        """
        Checks if a holding exists.

        check account_name for the holding named coin_name. if it exists, return true,
        else, return false.

        used when buying or selling currencies.
        """
        try:
            holding = self.accounts[account_name]["holdings"][coin_name]
        except KeyError: return False
        return True

    def decrease_holding(self, account_name:str, coin_name:str, shares:int):
        """
        removes a holding.

        we already check if the holding doesnt exist in self.has_enough_shares()

        reduce the number of shares by amount and if it == 0: remove it
        """
        self.accounts[account_name]["holdings"][coin_name] -= shares
        if self.accounts[account_name]["holdings"][coin_name] <= 0:
            del_dict_key(self.accounts[account_name]["holdings"], coin_name)
            self.accounts[account_name]["num_holdings"] -=1

    def calc_num_of_intervals(self, shares:int):
        """
        determines how many intervals there are when determining the cost

        each interval, we calculate the costs and coin fluctuations 50 shares at a time.
        however, if there are less than 50 shares left, we must use the remaining shares.

        this function determines how many intervals there will be in total.

        It uses the modulus to determine how far away the number of shares is from being divisible
        by 50. then it is divided by 50 to determine how many times, 50 fits into the num of shares. this is the quotient
        Example:
            70 is not divisible by 50.
            >>>70 % 50 # = 20
            >>>70-20 # = 50
            >>>50/50 # = 1
            50 fits into 70 1 time, so the function will run at least once.

        Next, it determines if there is a remainder. if so, it will run once more. else, it wont run an extra time
        Example:
            >>>70 % 50 # = 20
            20 != 0
            remainder = 1
        Example 2:
            >>>100 % 50 # = 0
            0 == 0
            remainder = 0

        to get the total amount of times run, we just add the quotient and the remainder
        """
        remainder:int
        mod = shares % shares_per_interval # the modulus

        # determines the remainder
        if mod == 0:
            remainder = 0
        else:
            remainder = 1

        quotient = (shares - mod) / shares_per_interval # determines the quotient

        return quotient + remainder