<!--
PLANTILLA DE DESCRIPCION DE VIDEO LARGO
Render: python tools/render_metadata.py --template docs/youtube/plantilla-descripcion-larga.md --data docs/youtube/enlaces.toml --data <datos-del-video>.toml
Todo este comentario se elimina al renderizar.

Placeholders (claves del TOML):
  resumen         obligatorio. 1-3 frases con la promesa del video (lo primero que se ve sin expandir: 100-150 caracteres utiles).
  capitulos       obligatorio. Lista "M:SS Titulo"; el primero en 0:00, minimo 3, separados 10 s o mas.
  codigo_url      obligatorio. Enlace directo a la carpeta del codigo en el repo.
  repo_url        obligatorio. URL del repositorio (viene de enlaces.toml).
  udemy_url       obligatorio. Curso de Udemy (viene de enlaces.toml).
  herramientas    obligatorio. Lista de herramientas/versiones usadas, texto plano sin enlaces.
  hashtags        obligatorio. Lista de #hashtags (max. 15; los 3 primeros salen sobre el titulo).
  es_trading      obligatorio (true/false). true agrega el disclaimer de disclaimer-trading.md.
  canal_url       opcional. Si existe (en enlaces.toml vale TODO_OWNER hasta STQ-38) agrega "Suscribete".
  afiliado_vps    opcional. Enlace de afiliado; solo si el dueño lo aporta. Si se define, debe declararse como afiliado.
  video_anterior / video_siguiente  opcionales. URLs de la playlist.
Sintaxis: ver docs/youtube/README.md. Sin '<' ni '>' en el texto (YouTube los rechaza).
-->
{{resumen}}

Capitulos:
{{capitulos}}

Codigo de este video: {{codigo_url}}
Repositorio completo: {{repo_url}}

Curso de Ciencia de datos con Python y R (Udemy): {{udemy_url}}
Apoya el canal: haz clic en el boton "Unirme" en la pagina del canal para ser miembro y acceder a los beneficios de la membresia.
{{#if canal_url}}
Suscribete: {{canal_url}}
{{/if}}
{{#if video_anterior}}
Video anterior: {{video_anterior}}
{{/if}}
{{#if video_siguiente}}
Siguiente video: {{video_siguiente}}
{{/if}}

Herramientas usadas:
{{herramientas}}
{{#if afiliado_vps}}

Servidor VPS que uso (enlace de afiliado: si lo contratas por aqui recibo una comision sin costo extra para ti): {{afiliado_vps}}
{{/if}}
{{#if es_trading}}

{{> disclaimer-trading.md}}
{{/if}}

{{hashtags|inline}}
