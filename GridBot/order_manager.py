import ccxt

# -------------------------------------------------------------------------------------------------
# Clase Order
# Esta clase define el objeto Order, que representa una orden de trading en el exchange.
# -------------------------------------------------------------------------------------------------
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
 
# -------------------------------------------------------------------------------------------------
# Clase OrderManager
# Esta clase administra todas las órdenes de trading del usuario en el exchange.
# -------------------------------------------------------------------------------------------------
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
    
    def place_order(self, price, side, amount):
        order_dict = self.exchange.create_order(self.symbol, 'limit', side, amount, price)
        order = Order(
            id=order_dict['clientOrderId'],
            datetime=order_dict['datetime'],
            symbol=order_dict['symbol'],
            price=order_dict['price'],
            side=order_dict['side'],
            amount=order_dict['amount'],
            status=order_dict['status']
        )
        self.orders.append(order)
        return order

    def cancel_order(self, id):
        return self.exchange.cancel_order(id, self.symbol)

    def update_order_status(self):
        orders = self.get_open_orders()
        for order in orders:
            order.update(self.exchange.fetch_order(order['id']))
    
    def check_grid_level(self, target_price, percentage_range):
        print("Checking grid level...")
        for order in self.orders:
            if (order.price <= target_price * (1 + percentage_range)) and (order.price >= target_price * (1 - percentage_range)):
                return False
        return True
