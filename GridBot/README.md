# GridBot

Bot de trading en cuadrícula (grid) para Bybit, construido con `ccxt`. Proyecto educativo: **opera con dinero real**, úsalo bajo tu responsabilidad.

## Quickstart

```bash
cd GridBot
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # y edita .env con tus credenciales
python main.py
```

- Las credenciales se leen de las variables de entorno `BYBIT_API_KEY` y `BYBIT_API_SECRET` (o del archivo `GridBot/.env`, que git ignora). Nunca las escribas en el código ni las subas al repositorio.
- Crea la clave API en Bybit con **permisos mínimos**: solo trading spot y **SIN permiso de retiro**. Si es posible, restríngela por IP.
- Si falta alguna variable, `main.py` termina con un mensaje que indica cuáles faltan.
- Parámetros de la estrategia (símbolo, rango, niveles, cantidad): al inicio de `main()` en `main.py`.
