# Guiones de Shorts: Algoritmo Genético Visual

Guiones para formato vertical (9:16, hasta 60 segundos) producidos a partir de la animación en tiempo real de `Heuristics/GA.py`.
Para publicar con `plantilla-descripcion-short.md` de `docs/youtube/`.

---

## Short 1: Una población de rectas que aprende sola en Python

- **Título sugerido:** Una población de rectas que aprende sola #Shorts
- **Duración estimada:** 45 segundos
- **Enfoque:** Demostración visual de la selección natural convergiendo desde el caos.
- **Audio de fondo:** Beat synthwave / lo-fi técnico de ritmo creciente.

### Estructura y tabla de tiempos

| Segundo | En pantalla (Formato 9:16 vertical) | Locución / Texto sobreimpreso |
|---|---|---|
| 0:00 - 0:05 | Plano cerrado del Subplot 2 de Matplotlib: puntos azules y rectas verdes disparadas en todas direcciones. | *"¿Puede un puñado de líneas aleatorias aprender geometría sin usar derivadas ni cálculo?"* (Texto: ¿Código que evoluciona?) |
| 0:05 - 0:15 | La línea roja empieza torcida y en 2 segundos gira rápidamente hacia la diagonal de puntos. | *"Generamos 1000 rectas al azar. Medimos su error contra los datos y nos quedamos solo con el mejor 10%."* |
| 0:15 - 0:25 | Zoom en la línea roja ajustándose milimétricamente. El cuadro de texto cambia de `y = 0.4x + 1.2` a `y = 2.01x + 2.98`. | *"Cruzamos sus parámetros, aplicamos una mutación del 50% al azar y repetimos generación tras generación."* |
| 0:25 - 0:35 | Plano general mostrando el Subplot 1 (curva de error cayendo) y el Subplot 3 (nube de puntos convergiendo en el óptimo). | *"En apenas 20 generaciones, el error cae de 14.000 a 100. La población encontró la solución óptima sola."* |
| 0:35 - 0:45 | Pantalla final con flecha apuntando abajo al video largo enlazado. | *"El código completo paso a paso en Python lo tienes en el video largo enlazado aquí abajo. ¡Míralo completo y suscríbete!"* |

---

## Short 2: De 14.000 de error a 100 en 3 segundos (Algoritmo Genético)

- **Título sugerido:** De 14.000 de error a 100 en 3 segundos #Shorts
- **Duración estimada:** 40 segundos
- **Enfoque:** El gráfico de fitness y el mapa de exploración $(m, b)$.
- **Audio de fondo:** Efecto de cuenta regresiva rápida y transición electrónica.

### Estructura y tabla de tiempos

| Segundo | En pantalla (Formato 9:16 vertical) | Locución / Texto sobreimpreso |
|---|---|---|
| 0:00 - 0:04 | Subplot 1 (Fitness): cursor señalando el valor inicial gigante `13690`. | *"Mira lo que pasa cuando dejas que la selección natural resuelva un problema de optimización en Python."* (Texto: 13.690 → 100) |
| 0:04 - 0:15 | Aceleración de la gráfica de pérdida: la curva se desploma en picado vertical. | *"Generación 1: error en 13.000. Generación 3: baja a 600. Generación 6: cae a 103."* |
| 0:15 - 0:28 | Transición rápida al Subplot 3 (Fitness Map): un mapa de calor viridis donde cada punto es un individuo probado en el plano de pendiente ($m$) y corte ($b$). | *"Este mapa de calor registra cada intento de la población. La nube se va concentrando como un embudo exactamente en m=2 y b=3."* |
| 0:28 - 0:40 | El punto rojo se queda fijo en el centro óptimo. Tarjeta con llamada al tutorial completo. | *"El algoritmo no sabe matemáticas: solo sabe qué individuo se equivocó menos. Explicación línea a línea en el video largo enlazado abajo."* |
