# Checklist de publicación

## Antes de publicar

- [ ] Título según `formulas-titulo.md` (máx. 100 caracteres) y miniatura según `miniatura-spec.md`.
- [ ] Datos del video en un `.toml` propio; descripción generada con `tools/render_metadata.py` (exit 0, sin `TODO_OWNER`/`TODO_LINK`).
- [ ] Capítulos: el primero en `0:00`, mínimo 3, cada uno de 10 s o más.
- [ ] Subtítulos: subir el archivo **SRT** revisado a mano (nombres propios, términos técnicos, comandos).
- [ ] Videos de trading: disclaimer en pantalla al inicio y en la descripción (`es_trading = true`).
- [ ] Sin datos sensibles en pantalla (claves API, tokens, correos, rutas personales, `.env`).
- [ ] Código del video subido al repo y `codigo_url` verificado (abre la carpeta correcta).
- [ ] **Tarjetas** (cards): 1-2 hacia el video anterior/siguiente o la lista de reproducción.
- [ ] **Pantalla final** (últimos 5-20 s): un video recomendado y el botón de suscripción.
- [ ] Lista de reproducción asignada y categoría/idioma (español) configurados.
- [ ] Etiquetas y hashtags según `tags-y-hashtags.md`.
- [ ] Marcar "no es para niños" y, si aplica, declaración de contenido alterado/generado por IA.

## Después de publicar

- [ ] Publicar y **fijar** el comentario de `comentario-fijado.md` (generarlo con el renderizador).
- [ ] Reproducir los primeros 30 s y verificar capítulos, tarjetas y pantalla final en la página pública.
- [ ] Añadir la URL del video largo a los datos de sus Shorts y publicarlos (`plantilla-descripcion-short.md`).
- [ ] Actualizar `estado` en `calendario.csv`.
- [ ] Responder los primeros comentarios durante las primeras 2 horas.
- [ ] A los 7 días: revisar retención y CTR en YouTube Studio y anotar aprendizajes para el siguiente video.
