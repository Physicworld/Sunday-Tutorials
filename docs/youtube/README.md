# Metadatos de YouTube

Plantillas y utilidad para publicar cada video o short con metadatos consistentes.

| Archivo | Uso |
|---------|-----|
| `plantilla-descripcion-larga.md` | Descripción de video largo (renderizable) |
| `plantilla-descripcion-short.md` | Descripción de short (renderizable) |
| `comentario-fijado.md` | Comentario fijado (renderizable) |
| `disclaimer-trading.md` | Aviso obligatorio de trading; se incluye con `es_trading = true` |
| `formulas-titulo.md` | 5 fórmulas de título con ejemplos |
| `miniatura-spec.md` | Especificación de miniatura |
| `checklist-publicacion.md` | Checklist antes/después de publicar |
| `tags-y-hashtags.md` | Guía de tags y hashtags |
| `enlaces.toml` | Enlaces oficiales; `TODO_OWNER` = pendiente del dueño (STQ-38) |
| `calendario-editorial.md` / `calendario.csv` | Calendario de 12 semanas (desde 2026-10-05): cadencia, supuestos y re-planificación |
| `ejemplo.toml` | Ejemplo completo que renderiza con exit 0 |

## Generar una descripción

```bash
python tools/render_metadata.py \
  --template docs/youtube/plantilla-descripcion-larga.md \
  --data docs/youtube/enlaces.toml --data mi-video.toml > descripcion.txt
```

`--data` es repetible (el último gana). Requiere Python 3.11+ (`tomllib`); sin dependencias.
El comando termina con código 1 y lista todos los problemas si:

- un `{{placeholder}}` no está definido en los datos;
- un valor usado vale `TODO_OWNER` o `TODO_LINK` (usa `--allow-todo` solo para borradores);
- la descripción supera 5000 bytes, contiene `<`/`>`, el título (clave `titulo`) pasa de 100 caracteres, los hashtags son inválidos o más de 15, o los capítulos no empiezan en `0:00`, son menos de 3 o están a menos de 10 s.

## Sintaxis de plantilla

- `{{clave}}`: valor del TOML (`{{tabla.clave}}` para tablas). Las listas se unen con saltos de línea; `{{clave|inline}}` las une con espacios.
- `{{#if clave}}...{{/if}}`: bloque opcional; se elimina si la clave no existe, es `false` o está vacía (sin anidar). Si la clave vale `TODO_OWNER`, el bloque se conserva y el renderizador falla: define el valor real o borra la clave.
- `{{> archivo.md}}`: incluye otro archivo (ruta relativa a la plantilla) en una línea propia.
- `<!-- ... -->`: comentario, se elimina. Cada plantilla documenta sus placeholders en un comentario inicial.

Reglas: nunca inventar enlaces (usa `TODO_OWNER`/`TODO_LINK`); los videos de trading llevan `es_trading = true`; no se cobra ni se vende GridBot ni ninguna estrategia como producto.
