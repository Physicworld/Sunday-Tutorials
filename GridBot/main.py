import os

from dotenv import load_dotenv

from grid_bot import GridBot


# -------------------------------------------------------------------------------------------------
# Configuración y ejecución del bot
# Aquí es donde se configura y se ejecuta el bot. Los parámetros se definen aquí y luego se pasan
# a la instancia del bot antes de ejecutarlo.
# -------------------------------------------------------------------------------------------------

def main():
    load_dotenv()
    KEY = os.getenv("BYBIT_API_KEY")
    SECRET = os.getenv("BYBIT_API_SECRET")
    missing = [name for name, value in (("BYBIT_API_KEY", KEY), ("BYBIT_API_SECRET", SECRET)) if not value]
    if missing:
        raise SystemExit(f"Faltan variables de entorno: {', '.join(missing)}. Defínelas en GridBot/.env (ver .env.example).")
    symbol = "LTC/USDT"
    grid_range = 0.01
    grid_levels = 2
    grid_amount = 0.02

    bot = GridBot(KEY, SECRET, symbol, grid_amount=grid_amount, grid_range=grid_range, grid_levels=grid_levels)
    bot.run()


if __name__ == "__main__":
    main()