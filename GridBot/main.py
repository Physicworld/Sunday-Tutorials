from grid_bot import GridBot


# -------------------------------------------------------------------------------------------------
# Configuración y ejecución del bot
# Aquí es donde se configura y se ejecuta el bot. Los parámetros se definen aquí y luego se pasan
# a la instancia del bot antes de ejecutarlo.
# -------------------------------------------------------------------------------------------------

def main():
    KEY = "3DM7tTuySNUyaHXcQq"
    SECRET = "YyNse5prCs7CwDARrE4b8HwgKuhnWMAyRHWe"
    symbol = "LTC/USDT"
    grid_range = 0.01
    grid_levels = 2
    grid_amount = 0.02

    bot = GridBot(KEY, SECRET, symbol, grid_amount=grid_amount, grid_range=grid_range, grid_levels=grid_levels)
    bot.run()


if __name__ == "__main__":
    main()