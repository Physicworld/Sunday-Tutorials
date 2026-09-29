<!--
PLANTILLA DEL COMENTARIO FIJADO (publicarlo y fijarlo justo despues de publicar el video)
Render: python tools/render_metadata.py --template docs/youtube/comentario-fijado.md --data docs/youtube/enlaces.toml --data <datos-del-video>.toml

Placeholders:
  pregunta     obligatorio. Pregunta concreta que invite a responder (p. ej. "Que patron te cuesta mas aplicar?").
  codigo_url   obligatorio. Carpeta del codigo en el repo.
  udemy_url    obligatorio. Curso de Udemy (de enlaces.toml).
  es_trading   obligatorio (true/false). true agrega el aviso de no asesoria financiera.
-->
{{pregunta}}

Codigo del video: {{codigo_url}}
Curso completo en Udemy: {{udemy_url}}
Si el contenido te sirve, suscribete y activa la campana para no perderte el siguiente.
{{#if es_trading}}

Aviso: contenido educativo, no es asesoria financiera.
{{/if}}
