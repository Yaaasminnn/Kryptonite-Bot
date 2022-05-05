from utils.users import *

def varify_holdings_test():
    # loads up a user instance and verifies if the holdings are verified
    user = User(1)
    user.save()

def deposit_test(exceeds:bool=False):
    # tests the User.bank_deposit() method.
    # tests using a regular deposit
    # then with a deposit that exceeds the wallet
    # testing for the wrong bank account will be in the bot's method
    amount = 50
    user = User(1)
    user.wallet = amount
    if not exceeds: print(user.bank_deposit(amount, "tfa"))
    else: print(user.bank_deposit(2*amount, "tfa"))
    user.save()

def withdraw_test(exceeds:bool=False):
    # tests the User.bank_withdraw() method.
    # tests using a regular withdrawal
    # and one that withdraws more money than in the bank account
    # testing for the wrong account will be in the bot's method
    amount = 50
    user = User(1)
    user.accounts["tfa"]["balance"] = amount
    if exceeds: print(user.bank_withdraw(2*amount, "tfa"))
    else: print(user.bank_withdraw(amount, "tfa"))
    user.save()

def transfer_test(scenario:str="normal"):
    # tests transfers between 2 users
    # tests under:
    # normal conditions
    # trading over the transfer limit
    # trading over the wallet
    # trading wallet > trading limit
    # negative values are handled by the bot's method

    amount = 49_999
    if scenario == ">trading_limit": amount +=2

    user1 = User(1)

    user1.wallet = amount

    if scenario == ">wallet": amount +=1

    print(user1.transfer(amount, 2))

    user1.save()

def tax_test(account:str, amount:float):
    # calculates the total(including tax)
    # scenarios:
    #   tfa account
    #   ntfa account
    print(User.calc_tax(account, amount))

if __name__ == '__main__':
    load_constants()
    #User.clear_account(1) # clears the user, 1