import os
from json_utils import *
import datetime
import asyncio

tax_rate, taxed_trading_limit_dollars, tax_free_trading_limit_dollars, \
trading_limit_shares, max_transfer_limit, start_amount,\
max_balance = None, None, None, None, None, None, None

def load_constants():
    """
    Loads constants that are used.

    These are in a json so they can easily be permanently changed during runtime.
    """
    global tax_rate, tax_free_trading_limit_dollars, trading_limit_shares, max_transfer_limit, start_amount, taxed_trading_limit_dollars, max_balance
    constants = load_json("kryptonite_bot/constants.json")
    max_transfer_limit = ["max transfer limit"]
    trading_limit_shares = constants["trading limit shares"]
    tax_free_trading_limit_dollars = constants["tax free trading limit dollars"]
    taxed_trading_limit_dollars = constants["taxed trading limit dollars"]
    tax_rate = constants["tax rate"]
    start_amount = constants["start amount"]
    max_balance = constants["max balance"]

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
        try: # if the json file dosent already exist, create it
            self.user = load_json(f"db/users/{uid}.json")
        except:
            create_json(f"db/users/{uid}.json")
            self.user = load_json(f"db/users/{uid}.json")
            self.user["uid"] = uid
            self.user["wallet"] = start_amount
            self.create_accounts() # creates both crypto accounts

            # saves the user
            self.save()


        self.verify_holdings()
        self.update_last_accessed()
        #pretty_print(self.user)

    def create_accounts(self):
        """
        Creates the 2 crypto accounts.

        Creates a Tax free account and a regular account.
        """
        accounts = []
        accounts.append( # regular account
            {
                "tax_free": False,
                "name": "ntfa",
                "balance": 0,
                "holdings": {},
                "num_holdings": 0
            }
        )
        accounts.append( # tax-free account
            {
                "tax_free": True,
                "name": "tfa",
                "balance":0,
                "holdings": {},
                "num_holdings": 0
            }
        )
        self.user["accounts"] = accounts

    def save(self):
        """
        Saves the Userdata.
        """
        update_json(f"db/users/{self.user['uid']}.json", self.user)

    def verify_holdings(self):
        """
        Verifies that all the tokens in a user's holdings still exist.

        runs through all holdings in both accounts. for every token in the holdings,
        check if it exists in the database. if not, delete it from the holdings.
        """
        crypto_db = load_json("db/crypto_currencies.json")
        not_in_db=[]
        for i, account in enumerate(self.user["accounts"]): # we enumerate so we can delete the account index easily

            for j in account["holdings"]: # we iterate backwards because we are modifying an index as we iterate through it
                in_db=False
                for crypto in crypto_db["currencies"]: # if the specific holding exists, we break
                    if j == crypto["name"]:
                        in_db = True
                        break

                if not in_db:
                    not_in_db.append(j)

            for k in not_in_db:
                del_dict_key(self.user["accounts"][i]["holdings"], key=k)

            not_in_db=[]

    def update_last_accessed(self):
        """
        Sets last_accessed to the current datetime.

        This is to keep track of the last time this user was accessed.
        :return:
        """
        self.user["last_accessed"] = str(datetime.datetime.now().replace(second=0, microsecond=0))

    def trade(self): pass

    def bank_deposit(self, amount:float, account_name:str):
        """
        Deposits the user's wallet into the bank account.

        There are no limits on how often/how much one can transfer from their own accounts.
        todo:
            add support for depositing/withdrawing all
        """
        if amount > self.user["wallet"]:
            return f"Insufficient wallet balance\nBalance: {self.user['wallet']}\nNeeded: {amount}"

        self.user["wallet"] -=amount
        if account_name == "tfa":
            self.user["accounts"][1]["balance"] += amount
        else:
            self.user["accounts"][0]["balance"] += amount

    def bank_withdraw(self, amount:float, account_name:str):
        """
        Withdraws money from the bank account to the user's wallet.

        No limits on how often/how much can be withdrawn.
        """
        # determines which account
        if account_name == "tfa": account_index = 1
        else: account_index = 0

        if amount > self.user["accounts"][account_index]["balance"]: # cannot exceed existing funds
            return f"Insufficient balance.\nBalance: {self.user['accounts'][account_index]['balance']}\nNeeded: {amount}"

        self.user["accounts"][account_index]["balance"] -= amount
        self.user["wallet"] += amount

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
        if self.user["accounts"][account_index]["balance"] < volume:
            return f"Insufficient balance.\nBalance: {self.user['accounts'][account_index]['balance']}\nNeeded: {volume}"

        # subtracts volume from the bank balance
        self.user["accounts"][account_index]["balance"] -= volume

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
            return f"Transfer amount exceeds transfer limit.\nTransfer limit: {self.user['max transfer limit']}"

        if amount > self.user["wallet"]:
            return f"Insufficient funds to transfer.\n Your wallet: {self.user['wallet']}\nAmount to send: {amount}"

        recipient = User(uid) # loads the recipient
        self.user["wallet"] -=amount
        recipient.user["wallet"] += amount

    def check_limit(self): pass

if __name__ == '__main__':
    os.chdir("/home/loona/programming/Kryptonite-Bot/src")
    load_constants()

    new = User(1)

    """# testing sell
    kbx_value = 10
    kbx_name = "kbx"
    new.user["accounts"][1]["holdings"][kbx_name] =1
    new.user["accounts"][1]["balance"] = 10
    new.c_sell("tfa", num=1, token_val=kbx_value, token_name=kbx_name)
    new.save()"""



    # tesing buy
    """
    kbx_value = 10
    kbx_name = "kbx"
    # tax free
    new.user["accounts"][1]["balance"] = 10
    print(new.c_buy("tfa", 1, 11000, kbx_name))
    # taxed
    new.user["accounts"][0]["balance"] = 10
    print(new.c_buy("ntfa", 1, 520000, kbx_name))


    # sell
    #new.c_sell("tfa", 1, kbx_value, kbx_name)

    new.save()
    """



    # depositing and withdrawing
    """
    new.bank_deposit(10, "tfa")
    new.save()
    """