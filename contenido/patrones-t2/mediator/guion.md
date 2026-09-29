# Mediator — guion (Temporada 2)

> Outline de video. Duración objetivo: **7-8 min**. Código: `Comportamiento/mediator.py`.
> Tipo: Patrón de comportamiento.

## Tabla de tiempos

| Bloque | Duración | Contenido |
| --- | --- | --- |
| Intro y problema | 1 min | Maraña de dependencias entre objetos |
| Ejemplo cotidiano | 1 min | Torre de control |
| Código paso a paso | 3 min | SalaChat, Usuario, privados |
| Cuándo NO usar | 1 min | Límites y alternativas |
| Comparación | 1 min | Observer, Facade |
| Cierre y CTA | 0.5 min | Resumen y suscripción |

Total: 7.5 min (rango objetivo 6-9 min).

## 1. Problema
Varios objetos se referencian entre sí; añadir uno obliga a modificar a todos. Mostrar el diagrama de flechas N×N.

## 2. Ejemplo cotidiano
Torre de control de un aeropuerto: los aviones no hablan entre sí, hablan con la torre.

## 3. Código paso a paso
1. Usuarios que se referencian directamente (el problema).
2. `SalaChat` como mediador con `unirse` y `enviar`.
3. `Usuario` conoce solo a la sala.
4. Difusión a todos menos al emisor.
5. Mensaje privado y errores (usuario desconocido, nombre duplicado).
6. Tests y `demo()`.

Ejecutar: `python Comportamiento/mediator.py` y `python -m pytest -q` en `Curso Patrones Diseno Python/Temporada2`.

## 4. Cuándo NO usarlo
- Pocos objetos: el mediador es un objeto dios innecesario.
- Si el mediador acumula toda la lógica de negocio.
- Comunicación de difusión simple: Observer.

## 5. Comparación con patrones parecidos
| Patrón | Diferencia |
| --- | --- |
| Observer | Difusión uno-a-muchos sin coordinar; el Mediator centraliza y coordina. |
| Facade | Simplifica el acceso a un subsistema en un sentido; el Mediator es bidireccional. |
| Command | Encapsula peticiones, no la comunicación entre colegas. |

## 6. CTA
Suscríbete para ver los 7 patrones de la Temporada 2, deja en comentarios qué patrón quieres ver aplicado a un proyecto real y el enlace al repositorio en la descripción.

## Borrador de metadatos
- **Título:** Patrón Mediator en Python: adiós a la maraña de dependencias
- **Descripción:** Mediator con una sala de chat y tests.
- **Etiquetas:** patrones de diseño, python, mediator, POO, clean code, GoF
- **Capítulos:** ver tabla de tiempos.
