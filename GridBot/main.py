import time
import datetime
import ccxt
from pprint import pprint


class Ticker:
    def __init__(self, symbol, bid, ask, last):
        self.symbol = symbol
        self.bid = bid
        self.ask = ask
        self.last = last
    
    def calculate_mid_price(self):
        return (self.bid + self.ask) / 2

    def __repr__(self) -> str:
        return f"Ticker(symbol={self.symbol}, bid={self.bid}, ask={self.ask}, last={self.last})"
    
class TickerManager:
    def __init__(self, exchange, symbol):
        self.exchange = exchange
        self.symbol = symbol

    def get_ticker(self):
        ticker = self.exchange.fetch_ticker(self.symbol)
        return Ticker(self.symbol, ticker['bid'], ticker['ask'], ticker['last'])

    def __repr__(self) -> str:
        return f"Ticker(symbol={self.symbol}, bid={self.bid}, ask={self.ask}, last={self.last})"

class Balance:
    def __init__(self, coin, free, used, total):
        self.coin = coin
        self.free = free
        self.used = used
        self.total = total
    
    def __eq__(self, other):
        if isinstance(other, Balance):
            return self.coin == other.coin
        return False

    def __repr__(self) -> str:
        return f"Balance(coin={self.coin}, free={self.free}, used={self.used}, total={self.total})"

class BalanceManager:
    def __init__(self, exchange, symbol):
        self.exchange = exchange
        self.symbol = symbol
        self.balances = []

    def get_balances(self):
        balance_dict = self.exchange.fetchBalance()
        coin1, coin2 = symbol.split('/')
        result = []

        for coin in [coin1, coin2]:

            if Balance(coin, 0, 0, 0) in self.balances:
                continue
            
            if coin in balance_dict['free']:
                free = balance_dict['free'][coin]
                used = balance_dict['used'][coin]
                total = balance_dict['total'][coin]
                result.append(Balance(coin, free, used, total))
            else:
                free = used = total = 0
            balance = Balance(coin, free, used, total)
            result.append(balance)
        self.balances = result
        return result

class Order:
    def __init__(self, id, datetime, symbol, price, side, amount, status = "sending"):
        self.id = id
        self.datetime = datetime
        self.symbol = symbol
        self.price = price
        self.side = side
        self.amount = amount
        self.status = status
    
    def __repr__(self) -> str:
        return f"Order(id={self.id}, datetime={self.datetime}, symbol={self.symbol}, price={self.price}, side={self.side}, amount={self.amount}, status={self.status})"

class OrderManager:
    def __init__(self, exchange, symbol):
        self.exchange = exchange
        self.symbol = symbol
        self.orders = []

    def get_open_orders(self):
        orders_dict = self.exchange.fetch_open_orders(self.symbol)
        orders = []
        for order_dict in orders_dict:
            orders.append(Order(
                id=order_dict['clientOrderId'],
                datetime=order_dict['datetime'],
                symbol=order_dict['symbol'],
                price=order_dict['price'],
                side=order_dict['side'],
                amount=order_dict['amount'],
                status=order_dict['status']
            ))
        self.orders = orders
        return orders
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

    def run(self):
        print("Iniciando el bot...")
        while True:
            balances = self.balance_manager.get_balances()
            ticker = self.ticker_manager.get_ticker()
            mid_price = ticker.calculate_mid_price()
            orders = self.order_manager.get_open_orders()
            pprint(orders)

            for i in range(1, self.grid_levels + 1):
                price_buy = round(mid_price * (1 - self.grid_range * i), 2)
                price_sell = round(mid_price * (1 + self.grid_range * i), 2)
                order_buy = Order(id=0, datetime=datetime.datetime.utcnow(), symbol=self.symbol, price=price_buy, side="buy", amount=self.grid_amount)
                order_sell = Order(id=0, datetime=datetime.datetime.utcnow(), symbol=self.symbol, price=price_sell, side="sell", amount=self.grid_amount)
                print(order_buy)
                print(order_sell)



            # # Pasos 5 y 6: gestionar las órdenes según los precios del grid
            # for price in grid_prices:
            #     if not self.order_manager.is_order_in_range(price, self.grid_range):
            #         side = 'buy' if price < current_price else 'sell'
            #         self.order_manager.place_grid_order(price, side, amount=1.0)  # ejemplo de cantidad fija

            # # Paso 7: actualizar el estado de las órdenes
            # self.order_manager.update_order_status()
            time.sleep(60)

KEY = "3DM7tTuySNUyaHXcQq"
SECRET = "YyNse5prCs7CwDARrE4b8HwgKuhnWMAyRHWe"
symbol = "LTC/USDT"
grid_range = 0.01
grid_levels = 5
grid_amount = 0.02

bot = GridBot(KEY, SECRET, symbol, grid_amount=grid_amount, grid_range=grid_range, grid_levels=grid_levels)
bot.run()