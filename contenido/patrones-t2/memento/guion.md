# Memento — guion (Temporada 2)

> Outline de video. Duración objetivo: **7-8 min**. Código: `Comportamiento/memento.py`.
> Tipo: Patrón de comportamiento.

## Tabla de tiempos

| Bloque | Duración | Contenido |
| --- | --- | --- |
| Intro y problema | 1 min | Deshacer sin romper encapsulación |
| Ejemplo cotidiano | 1 min | Guardar partida |
| Código paso a paso | 3 min | Editor, Memento, Historial |
| Cuándo NO usar | 1 min | Estados grandes |
| Comparación | 1 min | Command, Prototype |
| Cierre y CTA | 0.5 min | Resumen y suscripción |

Total: 7.5 min (rango objetivo 6-9 min).

## 1. Problema
Queremos deshacer, pero guardar el estado desde fuera obliga a exponer los atributos internos del objeto.

## 2. Ejemplo cotidiano
Guardar partida en un videojuego: el juego sabe qué guardar; tú solo conservas el archivo.

## 3. Código paso a paso
1. `Editor` con texto y cursor.
2. `Memento` como dataclass congelada (inmutable).
3. `Editor.guardar()` y `restaurar()`: solo el originador interpreta el memento.
4. `Historial` como caretaker con una pila.
5. Ejecutar `demo()` y ver los deshacer sucesivos.
6. Tests: restaura texto y cursor, pila vacía, inmutabilidad.

Ejecutar: `python Comportamiento/memento.py` y `python -m pytest -q` en `Curso Patrones Diseno Python/Temporada2`.

## 4. Cuándo NO usarlo
- Si el estado es muy grande o se guarda con mucha frecuencia (consumo de memoria).
- Si basta invertir la operación: usa Command con `undo`.
- Si el estado incluye recursos externos no copiables (ficheros, conexiones).

## 5. Comparación con patrones parecidos
| Patrón | Diferencia |
| --- | --- |
| Command | Guarda operaciones para revertirlas; Memento guarda el estado. |
| Prototype | Clona el objeto entero; Memento guarda una instantánea opaca. |
| Iterator | Ambos pueden usarse juntos para recorrer un historial. |

## 6. CTA
Suscríbete para ver los 7 patrones de la Temporada 2, deja en comentarios qué patrón quieres ver aplicado a un proyecto real y el enlace al repositorio en la descripción.

## Borrador de metadatos
- **Título:** Patrón Memento en Python: deshacer con snapshots
- **Descripción:** Implementa deshacer con el patrón Memento, cuidador y originador, con tests.
- **Etiquetas:** patrones de diseño, python, memento, POO, clean code, GoF
- **Capítulos:** ver tabla de tiempos.
