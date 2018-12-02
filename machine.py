from enum import Enum

class Rack:
    def __init__(self, code, name, price):
        self.code = code
        self.name = name
        self.price = price
        self.quantity = 0

class Coin(Enum):
    NICKEL = 5
    DIME = 10
    QUARTER = 25
    DOLLAR = 100

class Machine:
    def __init__(self, racks, coin_count=0):
        self.racks = {}
        self.coins = {
            Coin.DOLLAR: coin_count,
            Coin.QUARTER: coin_count,
            Coin.DIME: coin_count,
            Coin.NICKEL: coin_count,
        }
        for rack in racks:
            self.racks[rack.code] = rack
        self.amount = 0

    def refill(self, code, quantity):
        self.racks[code].quantity += quantity

    def insert(self, coin):
        self.coins[coin] += 1
        self.amount += coin.value

    # Recursive calls to find right coins combination to give change
    def calc_change(self, change, coins_list, coins, val=0, coins_i=0):
        if val == change:
            return coins
        if val > change:
            return None
        for i in range(coins_i, len(coins_list)):
            if coins[coins_list[i]] == 0:
                continue
            ccoins = coins.copy()
            ccoins[coins_list[i]] -= 1
            found = self.calc_change(change, coins_list, ccoins, val+coins_list[i].value, i)
            if found:
                return found
        return None

    def make_change(self, change):
        if change == 0:
            return True
        coins_list = list(self.coins.keys())
        new_coins = self.calc_change(change, coins_list, self.coins)
        if new_coins:
            back_coins = []
            for key, val in self.coins.items():
                nbc = val - new_coins[key]
                if nbc > 0:
                    back_coins.append(f'{nbc} {key.name}')
            print(f'Change: {change} ({", ".join(back_coins)})')
            self.coins = new_coins
            self.amount = 0
            return True
        return False


    def press(self, code):
        if self.amount >= self.racks[code].price:
            change = self.amount - self.racks[code].price
            if self.racks[code].quantity > 0:
                if self.make_change(change):
                    self.racks[code].quantity -= 1
                else:
                    print("no change available")
                    self.make_change(self.amount)
            else:
                print("product not available")
                self.make_change(self.amount)
        else:
            print("not enough money")
