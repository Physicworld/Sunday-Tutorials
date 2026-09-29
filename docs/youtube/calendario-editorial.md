# Calendario editorial de 12 semanas

Fuente de datos editable: [`calendario.csv`](calendario.csv) (columnas `fecha,tipo,titulo_provisional,fuente_ticket,estado,accion_dueno`). Este documento explica cadencia, supuestos y cómo re-planificar. Rango: **lunes 2026-10-05 a domingo 2026-12-27** (48 filas).

## Cadencia

| Semana tipo | Día | Contenido |
|-------------|-----|-----------|
| Lunes y jueves | largo | Episodio del curso de patrones (`tipo=curso`), 2 por semana |
| Martes y viernes | short | 2 Shorts por semana (`tipo=short`), cada uno enlazado a un video largo **ya publicado** |
| Sábado (cada 14 días) | largo | Episodio pilar (`tipo=pilar`), condicionado a que el dueño lo grabe |

- Nunca hay dos videos largos el mismo día (curso lun/jue, pilares sábado, compilado jueves 2026-12-03).
- **Curso**: los 17 episodios publicables ya están grabados y editados (`Curso Patrones Diseno Python/MEDIA.md`), en el orden Introducción → Creacionales (Factory Method, Abstract Factory, Builder, Prototype, Singleton) → Estructurales (Adapter, Bridge, Composite, Decorator, Facade, Flyweight) → Comportamiento (Chain of Responsibility, Command, Observer, State, Strategy). A 2/semana ocupan las semanas 1-9 (el episodio 17 sale el lunes 2026-11-30). El crudo `FactoryMethodsineditar.mkv` **no se publica**.
- **Compilado** "Curso completo": jueves 2026-12-03, justo después del episodio 17. Duración real: los 17 masters suman 156:00 min = **2 h 36 min** (el ticket mencionaba ≈146 min / 2 h 26 min; se usa la suma de `MEDIA.md`).
- **Pilares** (6, uno cada 14 días, sábados): AgentMCP (17 oct, primero por tendencia), GridBot (31 oct), SpeedUpPython (14 nov), Algoritmo genético (28 nov), Backtesting con Bollinger (12 dic), N8N con Docker (26 dic). Quedan sin fecha como reserva: DeepSeek-R1 local y Ciclos de Bitcoin (guiones en STQ-22 y STQ-26); entran si un pilar se cae o en la siguiente ventana.
- **Shorts**: cada semana, martes = short del largo del lunes y viernes = short del largo del jueves. En las semanas que siguen a un pilar (3, 5, 7, 9) el viernes se dedica al pilar. En las semanas 10-12 (sin episodios del curso) salen de los pilares y del compilado. Los Shorts se producen con Video2Short (plan en STQ-20, ejecución STQ-36).

## Significado de `estado`

| Valor | Significado |
|-------|-------------|
| `master_editado_pendiente_revision` | Video del curso ya grabado; falta la revisión del dueño (STQ-33) y programarlo (STQ-34) |
| `pendiente_de_pipeline` | El compilado se genera con el pipeline de STQ-19 |
| `condicionado_a_grabacion_del_dueno` | Depende de que el dueño grabe/edite (STQ-35, STQ-37); si no ocurre, la fecha se libera |
| `pendiente_de_largo` | El short solo se publica cuando su largo ya está en línea (para poner la URL en la descripción) |

Cuando algo se publique, cambia `estado` a `publicado` (o `omitido`/`movido` si se re-planifica). La columna `accion_dueno` dice qué hace el dueño en cada fila y con qué ticket. Los `fuente_ticket` son: STQ-34 (subir/programar curso), STQ-19 (compilado), STQ-21/22/23/24/25/26 (guion de cada pilar), STQ-36 (Shorts).

## Supuestos (editables)

1. **No se compromete ninguna fecha de grabación.** Las fechas de los pilares son supuestos: cada uno exige grabar y editar antes (aprox. 1-2 semanas antes de su fecha). Si el dueño no graba, no pasa nada con el resto del calendario.
2. Los masters del curso se revisan (STQ-33) antes del 5 de octubre y se suben programados (STQ-34); las plataformas permiten programar toda la tanda en una sesión.
3. Metadatos, miniaturas y comentario fijado salen de las plantillas de esta carpeta (`README.md`, `checklist-publicacion.md`); los videos de trading (GridBot, Backtesting) llevan `disclaimer-trading.md`.
4. Publicación a la misma hora local cada día; el 25 de diciembre (viernes, festivo) se puede adelantar el short al día 24.
5. Los Shorts de los episodios de Singleton, Decorator y Command no tienen slot propio (los viernes de las semanas 3, 5 y 7 se dedican al pilar anterior); se pueden sumar en las semanas 10-12 si hay tiempo.
6. No hay enlaces de monetización en este calendario; los enlaces reales se completan en STQ-38.

## Cómo re-planificar

1. **Un pilar no está listo**: márcalo `omitido` (o cambia su `fecha` al siguiente sábado libre) y mueve el mismo cambio a los Shorts que dependen de él (estado `condicionado_a_grabacion_del_dueno`); sustitúyelos por Shorts del curso o de la reserva.
2. **El curso se retrasa N días**: desplaza toda la columna `fecha` de las filas `curso`, `compilado` y sus Shorts en bloque (mismo N), conservando lunes/jueves; los pilares no se mueven salvo choque de fecha.
3. **Cambio de cadencia** (p. ej. 3 episodios/semana): reasigna fechas solo de `tipo=curso`; el compilado siempre va después del episodio 17.
4. Tras cualquier cambio comprueba las invariantes con el script de abajo.

```python
import csv, collections
rows = list(csv.DictReader(open("docs/youtube/calendario.csv", encoding="utf-8")))
largos = [r["fecha"] for r in rows if r["tipo"] != "short"]
assert len(largos) == len(set(largos)), "dos videos largos el mismo dia"
assert sum(r["tipo"] == "curso" for r in rows) == 17
print(collections.Counter(r["tipo"] for r in rows))
```
