import time
import datetime
import ccxt
from balance_manager import BalanceManager
from order_manager import OrderManager, Order
from ticker_manager import TickerManager

# -------------------------------------------------------------------------------------------------
# Clase GridBot
# Este es el bot principal que coordina todas las operaciones de trading. Utiliza las clases 
# BalanceManager, OrderManager y TickerManager para administrar el balance del usuario, 
# las órdenes de trading y los precios de los pares de monedas, respectivamente.
# -------------------------------------------------------------------------------------------------

class GridBot:
    def __init__(self, api_key, api_secret, symbol, grid_amount = 1, grid_levels=10, grid_range=0.1):
        self.exchange = ccxt.bybit({
            'apiKey': api_key,
            'secret': api_secret,
            "options": {'defaultType': 'spot' }
        })
        self.symbol = symbol
        self.grid_amount = grid_amount
        self.grid_levels = grid_levels
        self.grid_range = grid_range
        self.balance_manager = BalanceManager(self.exchange, symbol)
        self.order_manager = OrderManager(self.exchange, symbol)
        self.ticker_manager = TickerManager(self.exchange, symbol)

    def create_orders(self, mid_price):
        orders = []
        for i in range(1, self.grid_levels + 1):
            price_buy = round(mid_price * (1 - self.grid_range * i), 2)
            price_sell = round(mid_price * (1 + self.grid_range * i), 2)
            order_buy = Order(id=0, datetime=datetime.datetime.utcnow(), symbol=self.symbol, price=price_buy, side="buy", amount=self.grid_amount)
            order_sell = Order(id=0, datetime=datetime.datetime.utcnow(), symbol=self.symbol, price=price_sell, side="sell", amount=self.grid_amount)
            orders.extend([order_buy, order_sell])
        return orders

    def cancel_orders_out_of_range(self, mid_price):
        open_orders = self.order_manager.get_open_orders()
        min_price = mid_price * (1 - self.grid_range * self.grid_levels)
        max_price = mid_price * (1 + self.grid_range * self.grid_levels)

        for order in open_orders:
            if order.price < min_price or order.price > max_price:
                self.order_manager.cancel_order(order.id)

    def process_order(self, order):
        print(order)

        # Send order if an order is not in range
        if not self.order_manager.check_grid_level(order.price, self.grid_range):
            print("Not placing order: grid level check failed.")
            return

        # Check if there are enough balance
        if not self.balance_manager.check_balance(order):
            print("Not placing order: insufficient balance.")
            return

        # Place order
        order = self.order_manager.place_order(order.price, order.side, order.amount)

        # Update balances with the new order, adding or substracting the amount
        self.balance_manager.update_balances(order)

    def run(self):
        print("Iniciando el bot...")
        while True:
            balances = self.balance_manager.get_balances()
            ticker = self.ticker_manager.get_ticker()
            mid_price = ticker.calculate_mid_price()

            orders = self.create_orders(mid_price)
            for order in orders:
                print()
                self.process_order(order)

            time.sleep(60)


# -------------------------------------------------------------------------------------------------
# Configuración y ejecución del bot
# Aquí es donde se configura y se ejecuta el bot. Los parámetros se definen aquí y luego se pasan
# a la instancia del bot antes de ejecutarlo.
# -------------------------------------------------------------------------------------------------
KEY = "3DM7tTuySNUyaHXcQq"
SECRET = "YyNse5prCs7CwDARrE4b8HwgKuhnWMAyRHWe"
symbol = "LTC/USDT"
grid_range = 0.01
grid_levels = 2
grid_amount = 0.02

bot = GridBot(KEY, SECRET, symbol, grid_amount=grid_amount, grid_range=grid_range, grid_levels=grid_levels)
bot.run()
