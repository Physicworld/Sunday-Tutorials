
import ccxt

# -------------------------------------------------------------------------------------------------
# Clase Balance
# Esta clase define el objeto Balance, que representa el balance de una moneda específica en
# la cuenta del usuario en el exchange.
# -------------------------------------------------------------------------------------------------
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

# -------------------------------------------------------------------------------------------------
# Clase BalanceManager
# Esta clase administra el balance de todas las monedas en la cuenta del usuario en el exchange.
# -------------------------------------------------------------------------------------------------
class BalanceManager:
    def __init__(self, exchange, symbol):
        self.exchange = exchange
        self.symbol = symbol
        self.balances = []
    
    def update_balances(self, order):
        coin1, coin2 = self.symbol.split('/')
        if order.side == "buy":
            needed_coin = coin2
            needed_amount = order.amount * order.price
        else:
            needed_coin = coin1
            needed_amount = order.amount
        
        for balance in self.balances:
            if balance.coin == needed_coin:
                balance.free -= needed_amount
                balance.used += needed_amount
                balance.total -= needed_amount
                return

    def get_balances(self):
        balance_dict = self.exchange.fetchBalance()
        coin1, coin2 = self.symbol.split('/')
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

    def check_balance(self, order):
        needed_coin = self.symbol.split("/")[1] if order.side == "buy" else self.symbol.split("/")[0]
        needed_amount = order.amount * order.price if order.side == "buy" else order.amount

        for balance in self.balances:
            if balance.coin == needed_coin and balance.free >= needed_amount:
                return True
        return False


