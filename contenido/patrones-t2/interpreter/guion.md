# Interpreter — guion (Temporada 2)

> Outline de video. Duración objetivo: **8-9 min**. Código: `Comportamiento/interpreter.py`.
> Tipo: Patrón de comportamiento.

## Tabla de tiempos

| Bloque | Duración | Contenido |
| --- | --- | --- |
| Intro y problema | 1 min | Evaluar un mini-lenguaje |
| Ejemplo cotidiano | 1 min | Calculadora / reglas de negocio |
| Código paso a paso | 4 min | Expresiones, parser, evaluación |
| Cuándo NO usar | 1 min | eval, gramáticas grandes |
| Comparación | 1 min | Composite, Visitor |
| Cierre y CTA | 0.5 min | Resumen y suscripción |

Total: 8.5 min (rango objetivo 6-9 min).

## 1. Problema
Una regla o fórmula llega como texto ("x * (y - 1)") y hay que evaluarla. Una cadena de if/split se desmorona y `eval` es un riesgo de seguridad.

## 2. Ejemplo cotidiano
Una calculadora: cada símbolo y regla de la gramática se corresponde con una clase.

## 3. Código paso a paso
1. Gramática en BNF sencilla (comentario del `Parser`).
2. `Expresion` abstracta con `interpretar(contexto)`.
3. Terminales `Numero` y `Variable`; no terminal `Binaria`.
4. Parser de descenso recursivo: precedencia `*`/`/` sobre `+`/`-`.
5. `evaluar(texto, **vars)`; errores de sintaxis y variables no definidas.
6. Por qué no `eval`. Tests parametrizados.

Ejecutar: `python Comportamiento/interpreter.py` y `python -m pytest -q` en `Curso Patrones Diseno Python/Temporada2`.

## 4. Cuándo NO usarlo
- Gramáticas grandes o cambiantes: usar un generador de parsers.
- Cuando `ast.literal_eval` o una función bastan.
- Nunca `eval` con entrada de usuarios.

## 5. Comparación con patrones parecidos
| Patrón | Diferencia |
| --- | --- |
| Composite | El árbol de expresiones es un Composite cuyo método es `interpretar`. |
| Visitor | Permite añadir operaciones al árbol (imprimir, optimizar) sin tocar las clases. |
| Strategy | Elige un algoritmo; Interpreter evalúa un lenguaje. |

## 6. CTA
Suscríbete para ver los 7 patrones de la Temporada 2, deja en comentarios qué patrón quieres ver aplicado a un proyecto real y el enlace al repositorio en la descripción.

## Borrador de metadatos
- **Título:** Patrón Interpreter en Python: tu propio mini-lenguaje sin eval
- **Descripción:** Interpreter con parser recursivo y evaluación de expresiones aritméticas, con tests.
- **Etiquetas:** patrones de diseño, python, interpreter, POO, clean code, GoF
- **Capítulos:** ver tabla de tiempos.
