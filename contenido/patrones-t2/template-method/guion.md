# Template Method — guion (Temporada 2)

> Outline de video. Duración objetivo: **7-8 min**. Código: `Comportamiento/template_method.py`.
> Tipo: Patrón de comportamiento.

## Tabla de tiempos

| Bloque | Duración | Contenido |
| --- | --- | --- |
| Intro y problema | 1 min | Código duplicado con pasos casi iguales |
| Ejemplo cotidiano | 1 min | Receta |
| Código paso a paso | 3 min | Plantilla, pasos abstractos, hook |
| Cuándo NO usar | 1 min | Herencia rígida |
| Comparación | 1 min | Strategy, Factory Method |
| Cierre y CTA | 0.5 min | Resumen y suscripción |

Total: 7.5 min (rango objetivo 6-9 min).

## 1. Problema
Dos clases repiten el mismo algoritmo y solo difieren en un par de pasos; copiar y pegar genera divergencias.

## 2. Ejemplo cotidiano
Una receta: mismos pasos y mismo orden, cambian los ingredientes (té o café).

## 3. Código paso a paso
1. Mostrar `Te` y `Cafe` duplicando la secuencia.
2. `Bebida.preparar()`: el método plantilla con el orden fijo.
3. Pasos abstractos `infusionar` y `extras`.
4. El hook `quiere_extras` con valor por defecto.
5. Subclases `Te` y `Cafe(con_azucar)`.
6. Tests: orden fijo, hook y clase abstracta.

Ejecutar: `python Comportamiento/template_method.py` y `python -m pytest -q` en `Curso Patrones Diseno Python/Temporada2`.

## 4. Cuándo NO usarlo
- Si hay más de dos o tres puntos de variación: la herencia se vuelve rígida.
- Si necesitas cambiar el algoritmo en tiempo de ejecución: usa Strategy.
- Si la plantilla se rompe al añadir una subclase nueva.

## 5. Comparación con patrones parecidos
| Patrón | Diferencia |
| --- | --- |
| Strategy | Composición y cambio en runtime; Template Method usa herencia y es estático. |
| Factory Method | Es un Template Method especializado en crear objetos. |
| Decorator | Envuelve comportamiento; no fija un esqueleto. |

## 6. CTA
Suscríbete para ver los 7 patrones de la Temporada 2, deja en comentarios qué patrón quieres ver aplicado a un proyecto real y el enlace al repositorio en la descripción.

## Borrador de metadatos
- **Título:** Patrón Template Method en Python: el esqueleto de un algoritmo
- **Descripción:** Template Method con un ejemplo de bebidas, hooks y tests.
- **Etiquetas:** patrones de diseño, python, template method, POO, clean code, GoF
- **Capítulos:** ver tabla de tiempos.
