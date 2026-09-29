# Proxy — guion (Temporada 2)

> Outline de video. Duración objetivo: **7-8 min**. Código: `Estructurales/proxy.py`.
> Tipo: Patrón estructural.

## Tabla de tiempos

| Bloque | Duración | Contenido |
| --- | --- | --- |
| Intro y problema | 1 min | Objeto caro o restringido |
| Ejemplo cotidiano | 1 min | Recepcionista / portero |
| Código paso a paso | 3 min | Informe, proxy virtual, proxy de protección |
| Cuándo NO usar | 1 min | Sobreingeniería |
| Comparación | 1 min | Decorator, Adapter, Facade |
| Cierre y CTA | 0.5 min | Resumen y suscripción |

Total: 7.5 min (rango objetivo 6-9 min).

## 1. Problema
Crear o acceder a un objeto tiene un coste (carga lenta, permisos, red) y no queremos que cada cliente gestione ese coste. Mostrar el código ingenuo donde el cliente decide cuándo cargar y a quién dejar pasar.

## 2. Ejemplo cotidiano
El recepcionista de un edificio: tiene la misma interfaz que ver al director, pero decide si pasas y cuándo se le molesta.

## 3. Código paso a paso
1. La interfaz `Informe` con `leer()`.
2. `InformeReal`: costoso; contador `cargas` para observarlo.
3. `InformeVirtualProxy`: crea el real en la primera lectura y lo reutiliza.
4. `InformeProteccionProxy`: comprueba el rol y lanza `PermissionError`.
5. Componer ambos proxies y ejecutar `demo()`: una sola carga real.
6. Enseñar los tests de carga perezosa y de permisos.

Ejecutar: `python Estructurales/proxy.py` y `python -m pytest -q` en `Curso Patrones Diseno Python/Temporada2`.

## 4. Cuándo NO usarlo
- Si no hay coste ni control de acceso que justifique el intermediario.
- Si el cliente necesita conocer o controlar el ciclo de vida del objeto real.
- Si solo quieres añadir comportamiento: usa Decorator.

## 5. Comparación con patrones parecidos
| Patrón | Diferencia |
| --- | --- |
| Decorator | Añade responsabilidades; el Proxy controla el acceso al mismo objeto. |
| Adapter | Cambia la interfaz; el Proxy mantiene la misma. |
| Facade | Simplifica un subsistema; el Proxy representa un único objeto. |

## 6. CTA
Suscríbete para ver los 7 patrones de la Temporada 2, deja en comentarios qué patrón quieres ver aplicado a un proyecto real y el enlace al repositorio en la descripción.

## Borrador de metadatos
- **Título:** Patrón Proxy en Python: carga perezosa y control de acceso
- **Descripción:** Aprende el patrón Proxy con un ejemplo de proxy virtual y de protección, con tests.
- **Etiquetas:** patrones de diseño, python, proxy, POO, clean code, GoF
- **Capítulos:** ver tabla de tiempos.
