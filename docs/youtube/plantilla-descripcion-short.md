<!--
PLANTILLA DE DESCRIPCION DE SHORT (vertical, hasta 60 s)
Render: python tools/render_metadata.py --template docs/youtube/plantilla-descripcion-short.md --data docs/youtube/enlaces.toml --data <datos-del-short>.toml
Titulo del short: max. 100 caracteres incluyendo #Shorts (ver formulas-titulo.md); no se renderiza aqui, pero si defines "titulo" se valida.

Placeholders:
  gancho          obligatorio. Una frase que repite la promesa del short.
  video_largo_url obligatorio. URL del video largo del que sale el short (pegala cuando el largo ya este publicado).
  codigo_url      obligatorio. Carpeta del codigo en el repo.
  es_trading      obligatorio (true/false). true agrega el disclaimer breve.
  hashtags        obligatorio. Lista; incluir #Shorts. Max. 15.
-->
{{gancho}}

Video completo: {{video_largo_url}}
Codigo: {{codigo_url}}
{{#if es_trading}}

Contenido educativo, no es asesoria financiera.
{{/if}}

{{hashtags|inline}}
