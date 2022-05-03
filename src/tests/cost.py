a = 50 # the number of shares we buy at a time. compound value?
tot_a = 100_000 # the total number of shares to be bought
s = 54_500 # the total number of shares
v = 25 # the initial share price. this can be changed
v_og = 25 # a copy of the initial share price. this will not be changed
cost = 0

for i in range(int(tot_a/a)):
    v += (v*a)/s**2 # the new value after 50 shares

    cost += a * v
    print(f"value: {v}, cost: {cost}")

print(f"\nwith compound: {cost}")
print(f"without compound: {v_og*tot_a}")