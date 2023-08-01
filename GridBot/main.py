import ccxt
from pprint import pprint

class Balance:
    def __init__(self, coin, free, used, total):
        self.coin = coin
        self.free = free
        self.used = used
        self.total = total

class BalanceManager:
    def __init__(self, exchange):
        self.exchange = exchange

    def get_balances(self):
        balances = self.exchange.fetch_balance()
        result = []
        keys = ["free", "used", "total"]
        for key in keys:
            coins = balances[key].keys()
            for coin in coins:
                result.append(Balance(coin, balances["free"][coin], balances["used"][coin], balances["total"][coin]))
        return result
    
class OrderManager:
    def __init__(self, exchange, symbol):
        self.exchange = exchange
        self.symbol = symbol

    def get_open_orders(self):
        return self.exchange.fetch_open_orders(self.symbol)

    def place_grid_order(self, price, side, amount):
        return self.exchange.create_order(self.symbol, 'limit', side, amount, price)

    def cancel_order(self, id):
        return self.exchange.cancel_order(id, self.symbol)

    def update_order_status(self):
        orders = self.get_open_orders()
        for order in orders:
            order.update(self.exchange.fetch_order(order['id']))

    def is_order_in_range(self, target_price, percentage_range):
        orders = self.get_open_orders()
        for order in orders:
            lower_bound = target_price * (1 - percentage_range / 2)
            upper_bound = target_price * (1 + percentage_range / 2)
            if lower_bound <= order['price'] <= upper_bound:
                return True
        return False


class Ticker:
    def __init__(self, exchange, symbol):
        self.exchange = exchange
        self.symbol = symbol

    def get_ticker(self):
        return self.exchange.fetch_ticker(self.symbol)


class GridBot:
    def __init__(self, api_key, api_secret, symbol, grid_levels=10, grid_range=0.1):
        self.exchange = ccxt.bybit({
            'apiKey': api_key,
            'secret': api_secret
        })
        self.symbol = symbol
        self.grid_levels = grid_levels
        self.grid_range = grid_range
        self.balance_manager = BalanceManager(self.exchange)
        self.order_manager = OrderManager(self.exchange, symbol)
        self.ticker = Ticker(self.exchange, symbol)

    def run(self):
        print("Iniciando el bot...")
        while True:
            balances = self.balance_manager.get_balances()
            pprint(balances)
            ticker = self.ticker.get_ticker()
            pprint(ticker)
            current_price = ticker['last']

            # Paso 4: Calcular los índices de cada orden para el grid
            grid_prices = [current_price * (1 + self.grid_range * (i - self.grid_levels // 2)) 
                           for i in range(self.grid_levels)]

            # Pasos 5 y 6: gestionar las órdenes según los precios del grid
            for price in grid_prices:
                if not self.order_manager.is_order_in_range(price, self.grid_range):
                    side = 'buy' if price < current_price else 'sell'
                    self.order_manager.place_grid_order(price, side, amount=1.0)  # ejemplo de cantidad fija

            # Paso 7: actualizar el estado de las órdenes
            self.order_manager.update_order_status()

KEY = "3DM7tTuySNUyaHXcQq"
SECRET = "YyNse5prCs7CwDARrE4b8HwgKuhnWMAyRHWe"
symbol = "LTC/USDT"
grid_range = 0.01

bot = GridBot(KEY, SECRET, symbol, grid_range=grid_range)
bot.run()