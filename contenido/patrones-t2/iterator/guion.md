# Iterator — guion (Temporada 2)

> Outline de video. Duración objetivo: **6-7 min**. Código: `Comportamiento/iterator.py`.
> Tipo: Patrón de comportamiento.

## Tabla de tiempos

| Bloque | Duración | Contenido |
| --- | --- | --- |
| Intro y problema | 1 min | Recorrer sin exponer la estructura |
| Ejemplo cotidiano | 1 min | Playlist |
| Código paso a paso | 3 min | `__iter__`, `__next__`, generadores |
| Cuándo NO usar | 0.5 min | Colecciones triviales |
| Comparación | 1 min | Visitor, Composite |
| Cierre y CTA | 0.5 min | Resumen y suscripción |

Total: 7 min (rango objetivo 6-9 min).

## 1. Problema
El cliente indexa la lista interna y depende de cómo está guardada; cambiar la estructura o añadir un orden nuevo rompe el código cliente.

## 2. Ejemplo cotidiano
Una playlist: da igual cómo se guarden las canciones, tú pulsas «siguiente». También reproducción inversa o aleatoria.

## 3. Código paso a paso
1. `Playlist` guarda la lista de forma privada.
2. `IteradorPlaylist` con `__iter__` y `__next__`, y su propia posición.
3. Lanzar `StopIteration` al agotarse.
4. Recorridos alternativos con generadores: `inverso()` y `aleatorio(semilla)`.
5. Mostrar que se puede recorrer varias veces con iteradores independientes.
6. Tests: orden, vacío y semilla determinista.

Ejecutar: `python Comportamiento/iterator.py` y `python -m pytest -q` en `Curso Patrones Diseno Python/Temporada2`.

## 4. Cuándo NO usarlo
- Si una lista o un `for` normal ya basta: en Python ya es el patrón.
- Si el recorrido necesita acceso aleatorio por índice constante.
- Si la colección cambia mientras se itera sin una política definida.

## 5. Comparación con patrones parecidos
| Patrón | Diferencia |
| --- | --- |
| Visitor | Aplica operaciones sobre elementos; Iterator solo recorre. |
| Composite | Estructura en árbol; Iterator ofrece el recorrido de esa estructura. |
| Generator | Es la forma idiomática de Python de implementar un iterador. |

## 6. CTA
Suscríbete para ver los 7 patrones de la Temporada 2, deja en comentarios qué patrón quieres ver aplicado a un proyecto real y el enlace al repositorio en la descripción.

## Borrador de metadatos
- **Título:** Patrón Iterator en Python: iteradores y generadores
- **Descripción:** Cómo funciona el patrón Iterator y su relación con __iter__, __next__ y yield.
- **Etiquetas:** patrones de diseño, python, iterator, POO, clean code, GoF
- **Capítulos:** ver tabla de tiempos.
