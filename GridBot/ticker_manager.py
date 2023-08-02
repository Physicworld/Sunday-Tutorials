import ccxt

# -------------------------------------------------------------------------------------------------
# Clase Ticker
# Esta clase define el objeto Ticker, que representa la última información de precios de un 
# par de monedas en el exchange.
# -------------------------------------------------------------------------------------------------
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

# -------------------------------------------------------------------------------------------------
# Clase TickerManager
# Esta clase administra los tickers, que representan la última información de precios de 
# los pares de monedas en el exchange.
# -------------------------------------------------------------------------------------------------
class TickerManager:
    def __init__(self, exchange, symbol):
        self.exchange = exchange
        self.symbol = symbol

    def get_ticker(self):
        ticker = self.exchange.fetch_ticker(self.symbol)
        return Ticker(self.symbol, ticker['bid'], ticker['ask'], ticker['last'])
