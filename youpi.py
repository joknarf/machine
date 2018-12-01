


def make_change(v, coins, coin_values):
    for coin in coins:
        if len(coin_values[coin]):
            v += coin_values[coin].pop()
            print(v)
            make_change(v,coins,coin_values)

coins = [ 'NICKEL', 'DIME', 'QUARTER']

coin_values = {
    'NICKEL': [ 0, 5, 10],
    'DIME': [ 0, 10, 20],
    'QUARTER': [ 0, 25],
}

#make_change(0, coins, coin_values)

def mk_change_no(coins_c, value):
    global coins, coins_v
    c = coins_c.copy()
    v = 0
    for coin in coins:
        if c[coin] > 0:
            v += c[coin] * coins_v[coin]
            c[coin] -= 1
            mk_change(c)
    print(v)

def mk_change(value, cur_coins, v = 0):
    global coins, coins_v, coins_c, result, found

    if v > value:
        return
    if v == value:
        print('stop', v, cur_coins)
        result = cur_coins.copy()
        found = True
        return
    c = cur_coins.copy()
    for coin in reversed(coins):
        if c[coin] == 0:
            continue
        if coins_c[coin] > c[coin]:
            c[coin] += 1
            if c[coin] > 0:
                val = v + coins_v[coin]
            print(coin, v, c)
            mk_change(value, c, v)
            c[coin] -= 1
        if found:
            break
    print(f'return from {c}')


def mk_change2(value, cur_coins, v = 0):
    global coins, coins_v, coins_c, result, found
    
    c = cur_coins.copy()
    for coin in reversed(coins):
        for i in range(0,coins_c[coin]):
            c[coin] = i
            val = v + coins_v[coin] * i
            print('mk_change2',coin, val, c)
            mk_change2(value, c, val)
    print(f'return from {c}')

def mk_change3(value, cur_coins, v=0, i_coin=0):
    global coins, coins_v, coins_c, result, found
    
    print(v, cur_coins, i_coin)
    if v == value:
        found = True
        result = cur_coins
        print(f'found : {cur_coins}')
        return

    if i_coin == len(coins):
        return
    c = cur_coins.copy()

    if c[coins[i_coin]] == 0:
        mk_change3(value, c, v, i_coin+1)
    else:
        for i in range(i_coin,len(coins)):
            c[coins[i]] -= 1
            mk_change3(value,c, v+coins_v[coins[i]], i)
            if found is True:
                return
            c[coins[i]] += 1
    


def mk_change4(value, cur_coins, v=0, i_coin=0):
    global coins, coins_v, coins_c, result, found
    
    print(v, cur_coins, i_coin)
    if v > value:
        return
    if v == value:
        found = True
        result = cur_coins
        print(f'found : {cur_coins}')
        return
   
    for i in range(i_coin,len(coins)):
        c = cur_coins.copy()
        if c[coins[i]] == coins_c[coins[i]]:
            continue
        c[coins[i]] += 1
        mk_change4(value,c, v+coins_v[coins[i]], i)
        if found is True:
            return

def make_change(value,coins_c, coins_v):
    return mk_change5( value, coins_c, coins_v, list(coins_c.keys()), 
        {key:0 for (key,value) in coins_c.items()})


def mk_change5(value, coins_c, coins_v, coins, change_coins, val=0, i_coin=0):    
    print(val, change_coins, i_coin)
    if val > value:
        return None
    if val == value:
        print(f'found : {change_coins}')
        return change_coins
   
    for i in range(i_coin,len(coins)):
        c = change_coins.copy()
        if c[coins[i]] == coins_c[coins[i]]:
            continue
        c[coins[i]] += 1
        found = mk_change5(value, coins_c, coins_v, coins, c, val+coins_v[coins[i]], i)
        if found:
            return found
    return None

coins = [ 'QUARTER', 'DIME', 'NICKEL' ]
coins_c = {
    'QUARTER': 3,
    'DIME': 3,
    'NICKEL': 5,
}
 

coins_v = {
    'NICKEL': 5,
    'DIME': 10,
    'QUARTER': 25,
}

change_coins = {
    'NICKEL': 0,
    'DIME': 0,
    'QUARTER': 0,
}
result = {}
found = False
#mk_change(15,change_coins)
result = make_change(130, coins_c, coins_v)
print(result)