# Visitor — guion (Temporada 2)

> Outline de video. Duración objetivo: **7-9 min**. Código: `Comportamiento/visitor.py`.
> Tipo: Patrón de comportamiento.

## Tabla de tiempos

| Bloque | Duración | Contenido |
| --- | --- | --- |
| Intro y problema | 1 min | Operaciones nuevas sin tocar las clases |
| Ejemplo cotidiano | 1 min | Inspector que visita edificios |
| Código paso a paso | 3.5 min | Figuras, aceptar, doble despacho |
| Cuándo NO usar | 1 min | Límites y alternativas |
| Comparación | 1 min | Iterator, Strategy, singledispatch |
| Cierre y CTA | 0.5 min | Resumen y suscripción |

Total: 8 min (rango objetivo 6-9 min).

## 1. Problema
Cada operación nueva (área, exportar, dibujar) obliga a modificar todas las clases de la jerarquía y las llena de responsabilidades ajenas.

## 2. Ejemplo cotidiano
Un inspector que visita distintos negocios: la inspección depende del tipo de local, pero los locales no cambian.

## 3. Código paso a paso
1. Jerarquía `Figura`, `Circulo`, `Rectangulo`.
2. `aceptar(visitante)` en cada elemento.
3. `VisitanteFigura` con un método por tipo (doble despacho).
4. `CalculadorArea` y `ExportadorTexto` como operaciones nuevas.
5. Qué pasa al añadir una figura nueva (coste).
6. Alternativa pythónica: `match` / `singledispatch`. Tests.

Ejecutar: `python Comportamiento/visitor.py` y `python -m pytest -q` en `Curso Patrones Diseno Python/Temporada2`.

## 4. Cuándo NO usarlo
- Se añaden clases nuevas con frecuencia.
- Python ya ofrece `match` y `singledispatch`, más ligeros.
- Los elementos deben ocultar su estado interno al visitante.

## 5. Comparación con patrones parecidos
| Patrón | Diferencia |
| --- | --- |
| Iterator | Recorre elementos; el Visitor aplica operaciones sobre ellos. |
| Strategy | Intercambia un algoritmo de un objeto; Visitor añade operaciones a una jerarquía. |
| Composite | Suelen combinarse: el visitante recorre el árbol. |

## 6. CTA
Suscríbete para ver los 7 patrones de la Temporada 2, deja en comentarios qué patrón quieres ver aplicado a un proyecto real y el enlace al repositorio en la descripción.

## Borrador de metadatos
- **Título:** Patrón Visitor en Python: nuevas operaciones sin modificar clases
- **Descripción:** Visitor y doble despacho con figuras geométricas y tests.
- **Etiquetas:** patrones de diseño, python, visitor, POO, clean code, GoF
- **Capítulos:** ver tabla de tiempos.
