import unittest
from machine import Machine, Rack, Coin

class MachineTest(unittest.TestCase):
    def test_refill(self):
        rack = Rack("A", "Biscuit", 100)
        machine = Machine([rack])
        machine.refill("A", 10)
        self.assertEqual(machine.racks['A'].quantity, 10)

    def test_buy_biscuit(self):
        rack = Rack("A", "Biscuit", 100)
        machine = Machine([rack])
        machine.refill("A", 1)
        for i in range(4):
            machine.insert(Coin.QUARTER)
        machine.press("A")
        self.assertEqual(machine.racks['A'].quantity, 0)
        self.assertEqual(machine.coins[Coin.QUARTER], 4)

    def test_buy_biscuit_no_quantity(self):
        rack = Rack("A", "Biscuit", 100)
        machine = Machine([rack])
        for i in range(4):
            machine.insert(Coin.QUARTER)
        machine.press("A")
        self.assertEqual(machine.racks['A'].quantity, 0)
        self.assertEqual(machine.coins[Coin.QUARTER], 0)

    def test_buy_biscuit_not_enough_coins(self):
        rack = Rack("A", "Biscuit", 100)
        machine = Machine([rack])
        machine.refill("A", 1)
        for i in range(3):
            machine.insert(Coin.QUARTER)
        machine.press("A")
        self.assertEqual(machine.racks['A'].quantity, 1)
        self.assertEqual(machine.coins[Coin.QUARTER], 3)

    def test_buy_biscuit_too_many_coins(self):
        rack = Rack("A", "Biscuit", 100)
        machine = Machine([rack], 10)
        machine.refill("A", 1)
        for i in range(3):
            machine.insert(Coin.QUARTER)
        for i in range(3):
            machine.insert(Coin.DIME)
        machine.press("A")
        self.assertEqual(machine.racks['A'].quantity, 0)
        self.assertEqual(machine.coins[Coin.QUARTER], 13)
        self.assertEqual(machine.coins[Coin.DIME], 13)
        self.assertEqual(machine.coins[Coin.NICKEL], 9)

    def test_buy_biscuit_too_many_coins2(self):
        rack = Rack("A", "Biscuit", 90)
        machine = Machine([rack], 0)
        machine.coins[Coin.DIME] = 1
        machine.refill("A", 1)
        for i in range(1):
            machine.insert(Coin.QUARTER)
        for i in range(10):
            machine.insert(Coin.DIME)
        machine.press("A")
        self.assertEqual(machine.racks['A'].quantity, 0)
        self.assertEqual(sum([ k.value*v for k,v in machine.coins.items() ]), 100)

    def test_make_change(self):
        machine = Machine([], 0)
        for change in [ 5, 10, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80 ]:
            machine.coins = {
                Coin.QUARTER: 2,
                Coin.DIME: 2,
                Coin.NICKEL: 2,
            }
            left = sum([ k.value*v for k,v in machine.coins.items() ]) - change 
            self.assertTrue(machine.make_change(change))
            self.assertEqual(sum([ k.value*v for k,v in machine.coins.items() ]), left)

    def test_make_change_fail(self):
        machine = Machine([], 0)
        machine.coins = {
            Coin.DOLLAR: 0,
            Coin.QUARTER: 1,
            Coin.DIME: 1,
            Coin.NICKEL: 0,
        }
        change = 30
        self.assertFalse(machine.make_change(change))
