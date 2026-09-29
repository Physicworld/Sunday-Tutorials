# Guiones de Shorts: Backtesting Cuantitativo con Bollinger

Guiones para formato vertical (9:16, hasta 60 segundos) producidos a partir de `AlgorithmicTrading/Backtesting/backtesting.ipynb`.
Para publicar con `plantilla-descripcion-short.md` de `docs/youtube/` (`es_trading = true`).

---

## Short 1: El error invisible que infla tu backtest

- **Título sugerido:** El error de look-ahead que infla tu backtest #Shorts
- **Duración estimada:** 45 segundos
- **Enfoque:** Demostración de cómo el sesgo de anticipación (*look-ahead bias*) crea rentabilidades ficticias.
- **Aviso:** Contenido educativo, no es asesoría financiera.

### Estructura y tabla de tiempos

| Segundo | En pantalla (Formato 9:16 vertical) | Locución / Texto sobreimpreso |
|---|---|---|
| 0:00 - 0:05 | Primer plano de una gráfica con una rentabilidad de +1000% y un cartel gigante tachándola con una cruz roja. | *"¿Tu estrategia en Python da un 1000% de rentabilidad en el backtest? Cuidado: probablemente estás cometiendo este error invisible."* |
| 0:05 - 0:18 | Zoom en la línea de código del notebook: `df['SIGNAL'] = df['SIGNAL'].ffill().bfill()`. Resaltar `bfill()` en rojo parpadeante. | *"El sesgo de anticipación o look-ahead bias ocurre cuando tu código utiliza datos del futuro para decidir compras en el pasado. Rellenar con `bfill` o asumir que compras al precio de cierre exacto del mismo día falsea todo."* |
| 0:18 - 0:32 | Gráfica comparativa: Backtest teórico vs. ejecución real con velas siguientes y comisiones. | *"En el mercado real, la señal se confirma al cierre, pero tu orden entra en la apertura siguiente y con comisiones de exchange que devoran el margen."* |
| 0:32 - 0:45 | Pantalla final con disclaimer y flecha al video largo enlazado. | *"En el tutorial largo que te dejo enlazado aquí abajo te enseño a limpiar estos sesgos con Python paso a paso. Contenido educativo, no es asesoría financiera."* |

---

## Short 2: 71% de acierto pero pierdes dinero: la trampa del trading

- **Título sugerido:** 71% de acierto y pierdes dinero: la trampa del trading #Shorts
- **Duración estimada:** 45 segundos
- **Enfoque:** La falacia de la tasa de acierto frente a la esperanza matemática de ganancias.
- **Aviso:** Contenido educativo, no es asesoría financiera.

### Estructura y tabla de tiempos

| Segundo | En pantalla (Formato 9:16 vertical) | Locución / Texto sobreimpreso |
|---|---|---|
| 0:00 - 0:05 | Gráfico del mapa de calor de Seaborn resaltando en verde brillante el número: `Win Rate: 71.6%`. | *"¿Una estrategia que acierta el 71% de las veces es una mina de oro? Matemáticamente puede ser tu ruina."* |
| 0:05 - 0:18 | División de pantalla: a la izquierda `Stop Loss: 18%`; a la derecha `Take Profit: 5%`. | *"En nuestro backtest sobre Bitcoin, la combinación con 71% de acierto arriesga un 18% de Stop Loss para ganar un mísero 5% de beneficio."* |
| 0:18 - 0:30 | Animación de balance: 7 ganancias de 50 USD (+350 USD) seguidas de 2 pérdidas de 180 USD (-360 USD). Balance neto en negativo. | *"Aciertas 7 operaciones pequeñas, pero 2 rachas perdedoras consecutivas se comen toda la ganancia del mes y te dejan en negativo."* |
| 0:30 - 0:45 | Pantalla final con los 4 mapas de calor y llamada al tutorial completo. | *"En trading cuantitativo importa la esperanza matemática y el ratio beneficio/riesgo, no presumir de porcentaje de acierto. Masterclass completa enlazada abajo. Contenido educativo."* |
