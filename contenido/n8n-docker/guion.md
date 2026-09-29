# Guion de Video: Despliegue de n8n con Docker en tu propio servidor

- **Duración estimada:** 9 minutos 30 segundos (rango objetivo: 7 - 12 minutos).
- **Tema:** Instalación y configuración limpia de n8n usando Docker y Docker Compose moderno, persistencia de datos y creación del primer flujo.
- **Público objetivo:** Desarrolladores, analistas y entusiastas de la automatización que no quieren pagar suscripciones mensuales de Make/Zapier y buscan privacidad total.
- **Material de apoyo en repo:** `N8N Tutorial/instructions.md` y carpeta `contenido/n8n-docker/hallazgos.md`.

---

## Tabla de Tiempos y Estructura

| Bloque | Minuto inicio | Minuto fin | Duración | Descripción |
|---|---|---|---|---|
| 1. Gancho y propuesta de valor | 0:00 | 0:45 | 0:45 | Dejar de pagar Zapier; automatizaciones ilimitadas en tu hardware. |
| 2. Requisitos previos y arquitectura | 0:45 | 1:45 | 1:00 | RAM, CPU, Docker Engine moderno y plugin Compose. |
| 3. Preparación de Docker y repositorio | 1:45 | 3:15 | 1:30 | Verificación de Docker, permisos sin sudo y carpeta del proyecto. |
| 4. El archivo `docker-compose.yml` perfecto | 3:15 | 5:15 | 2:00 | Variables de entorno, puertos y volumen con nombre seguro. |
| 5. Despliegue y Demo en vivo | 5:15 | 7:15 | 2:00 | `docker compose up -d`, acceso a la interfaz web y primer flujo webhook. |
| 6. Errores frecuentes y mantenimiento | 7:15 | 8:45 | 1:30 | Conflictos de puerto, permisos y el peligro de `rm -rf`. |
| 7. Conclusión y Llamada a la Acción (CTA) | 8:45 | 9:30 | 0:45 | Repo de GitHub, curso en Udemy, membresía y pregunta de cierre. |

---

## Tabla de Pantallas y Elementos Visuales

| Bloque | Tipo de plano | Elemento en pantalla | Apoyo gráfico / Texto sobreimpreso |
|---|---|---|---|
| 1 | Cámara + Recorte | Presentador con fondo de estudio oscuro | "n8n en tu servidor: ilimitado y privado" |
| 2 | Esquema / Diapositiva | Diagrama: Tu máquina → Docker → Contenedor n8n → Volumen `n8n_data` | Requisitos: 2 vCPU, 4 GB RAM, Ubuntu/Debian/macOS |
| 3 | Terminal | Terminal pantalla completa (fuente grande, 20pt) | Comandos `docker --version`, `docker compose version` |
| 4 | Editor de código / IDE | `docker-compose.yml` en Neovim o VS Code | Resaltar líneas de volumen persistente y puerto `5678:5678` |
| 5 | Navegador web | Navegador en `http://localhost:5678`, interfaz oscura de n8n | Onboarding de cuenta y canvas de flujo |
| 6 | Terminal + Cuadro rojo | Comandos de diagnóstico `docker compose ps` y `docker compose logs` | Cartel de advertencia: "¡Nunca borres tus datos persistentes a ciegas!" |
| 7 | Cámara + Pantalla final | Presentador + tarjeta con repo y curso | Miniatura del curso de Udemy y botón "Unirme" |

---

## Guion Detallado (Locución y Acciones)

### 1. Gancho y propuesta de valor (0:00 - 0:45)
- **[CÁMARA]**
- *"¿Cuántas veces has querido automatizar una tarea entre APIs, pero Zapier o Make te cobran por cada ejecución o te limitan los pasos a una miseria? Hoy vamos a solucionar eso de raíz: vas a tener tu propia plataforma de automatización profesional, **n8n**, corriendo en tu propia máquina o VPS con Docker, sin límites de ejecuciones y con total privacidad de tus credenciales."*
- *"En menos de 10 minutos la tendrás operativa, persistente y lista para conectar bases de datos, modelos de inteligencia artificial y webhooks."*

### 2. Requisitos previos y arquitectura (0:45 - 1:45)
- **[ESQUEMA EN PANTALLA]**
- *"Para seguir este tutorial solo necesitas una máquina con Linux (como Ubuntu Server o tu propia laptop), macOS o Windows con WSL2. En cuanto a hardware: con 2 núcleos de CPU y 2 a 4 GB de memoria RAM es más que suficiente para miles de ejecuciones diarias."*
- *"Importante: vamos a utilizar **Docker Compose v2** (el comando moderno `docker compose`), que hoy viene integrado en Docker sin necesidad del viejo paquete de Python."*

### 3. Preparación del entorno y permisos (1:45 - 3:15)
- **[TERMINAL COMPLETA]**
- *"Vamos a la terminal. Lo primero es asegurarnos de que Docker está instalado y activo:"*
  ```bash
  docker --version
  docker compose version
  ```
- *"Si no tienes Docker instalado, sigue la guía paso a paso de la documentación oficial instalando `docker-ce` y `docker-compose-plugin`."*
- *"Asegúrate de que tu usuario pueda ejecutar Docker sin anteponer `sudo`:"*
  ```bash
  sudo usermod -aG docker $USER
  ```
  *(Recordar cerrar sesión y volver a entrar si acabas de añadir el grupo).*
- *"Ahora creamos un directorio limpio para nuestro proyecto de automatización:"*
  ```bash
  mkdir -p ~/n8n-docker && cd ~/n8n-docker
  ```

### 4. Creación del archivo `docker-compose.yml` (3:15 - 5:15)
- **[EDITOR DE CÓDIGO]**
- *"Abrimos nuestro editor favorito y creamos el archivo `docker-compose.yml`:"*
  ```bash
  nano docker-compose.yml
  ```
- *"Escribimos la configuración moderna de Compose:"*
  ```yaml
  services:
    n8n:
      image: docker.n8n.io/n8nio/n8n:latest
      container_name: n8n-service
      restart: unless-stopped
      ports:
        - "5678:5678"
      environment:
        - N8N_HOST=localhost
        - N8N_PORT=5678
        - N8N_PROTOCOL=http
        - NODE_ENV=production
        - WEBHOOK_URL=http://localhost:5678/
        - GENERIC_TIMEZONE=Europe/Madrid
        - TZ=Europe/Madrid
      volumes:
        - n8n_data:/home/node/.n8n

  volumes:
    n8n_data:
  ```
- **[PUNTOS CLAVE A RESALTAR EN PANTALLA]:**
  1. *"Fíjate que **no** ponemos `version: '3.8'`; en la especificación actual de Compose esa línea es obsoleta."*
  2. *"Fijamos el volumen nombrado `n8n_data`. Muchas guías antiguas usan carpetas del host directas como `~/.n8n`, pero eso suele provocar errores de permisos (`EACCES`) con el usuario interno `node` del contenedor. Un volumen gestionado por Docker evita todos esos dolores de cabeza."*
  3. *"Configura `GENERIC_TIMEZONE` con tu zona horaria para que los nodos de cron y programación horaria se disparen a tu hora exacta."*

### 5. Despliegue y Demo en vivo (5:15 - 7:15)
- **[TERMINAL]**
- *"Guardamos el archivo y levantamos el servicio en segundo plano:"*
  ```bash
  docker compose up -d
  ```
- *"Vemos cómo descarga la imagen y crea la red y el volumen. Para comprobar que todo marcha perfectamente, miramos los logs:"*
  ```bash
  docker compose logs -f
  ```
- *"Cuando leas `Editor is now accessible via: http://localhost:5678`, salimos de los logs con `Ctrl + C`."*
- **[NAVEGADOR WEB]**
- *"Abrimos el navegador en `http://localhost:5678`."*
- *"Creamos nuestra cuenta de propietario inicial (nombre, email y contraseña). Todo esto se almacena en local, en tu propia base de datos SQLite cifrada."*
- *"Hacemos un flujo de prueba ultra rápido: añadimos un nodo **Manual Trigger** y lo conectamos a un nodo **Code** con JavaScript o un nodo **HTTP Request** para consultar una API meteorológica pública."*
- *"Pulsamos 'Test step' y vemos los datos fluir en tiempo real. ¡Tu plataforma ya está trabajando!"*

### 6. Errores frecuentes y mantenimiento seguro (7:15 - 8:45)
- **[TERMINAL / PANTALLA DIVIDIDA]**
- *"Veamos tres errores habituales y cómo resolverlos:"*
  1. **Puerto ocupado:** *"Si al hacer `up -d` ves `bind: address already in use`, revisa qué proceso tiene el puerto 5678 con `sudo lsof -i :5678`. Puedes cambiar el puerto externo en el compose a `5679:5678` sin tocar el interno."*
  2. **Actualizaciones sin perder datos:** *"Para actualizar a la última versión, nunca borres el volumen. Basta con hacer:"*
     ```bash
     docker compose pull
     docker compose up -d
     ```
     *"Docker recrea el contenedor con la nueva imagen y tus flujos y credenciales se mantienen intactos en el volumen `n8n_data`."*
  3. **¡Cuidado con los comandos destructivos!** *"En algunos foros verás sugerencias de borrar carpetas como `rm -rf ~/.n8n`. Nunca lo hagas a la ligera: ahí reside la clave de cifrado de todas tus contraseñas y flujos. Si necesitas resetear, haz siempre una copia previa con `docker run --rm -v n8n_data:/data -v $(pwd):/backup alpine tar czf /backup/n8n_backup.tar.gz /data`."*

### 7. Conclusión y Llamada a la Acción (CTA) (8:45 - 9:30)
- **[CÁMARA]**
- *"Tienes el archivo `docker-compose.yml` listo para copiar en el repositorio de GitHub que te dejo en la descripción del video."*
- *"Si quieres profundizar en cómo procesar estos datos con Python, machine learning y modelos avanzados, te invito a inscribirte en mi curso de Udemy **Ciencia de datos con Python y R**, cuyo enlace con descuento tienes abajo."*
- *"Y si este tutorial te ha ahorrado tiempo y dolores de cabeza, dale a 'Me gusta', suscríbete y considera unirte como miembro del canal con el botón 'Unirme' para apoyar el contenido técnico independiente."*
- *"Déjame en los comentarios: ¿cuál es la primera automatización que vas a migrar de Make o Zapier a tu nuevo n8n? ¡Nos vemos en el próximo video!"*
