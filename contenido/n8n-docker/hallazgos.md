# Hallazgos técnicos y discrepancias: Guía de n8n con Docker

Revisión técnica de `N8N Tutorial/instructions.md` frente a las versiones y recomendaciones oficiales actuales (n8n v1.x / v2.x, Docker Engine 26+, Docker Compose v2).

> **Nota:** La guía original no se ha modificado directamente (tarea asignada a STQ-7). Este documento detalla cada discrepancia encontrada, su impacto práctico y la recomendación oficial con enlaces verificables.

---

## 1. Discrepancias en Docker Compose y comandos

### 1.1 `docker compose` (v2) vs. `docker-compose` (v1 en desuso)
- **En la guía:** Se indica instalar `sudo apt install -y docker-compose` y ejecutar comandos como `docker-compose up -d`, `docker-compose logs -f`.
- **Estado actual:** Docker Compose v1 (escrito en Python) fue declarado obsoleto (*deprecated*) en julio de 2023. En distribuciones modernas (Ubuntu 22.04 / 24.04), el paquete `docker-compose` del repositorio de Ubuntu puede instalar la versión legacy v1 o un wrapper incompleto. La forma estándar y recomendada es el plugin oficial `docker-compose-plugin`, invocable como subcomando nativo: `docker compose up -d`.
- **Impacto:** Si el usuario no tiene la versión v1 instalada, `docker-compose` arroja `command not found`.
- **Fuente oficial:** [Docker Compose Install Documentation](https://docs.docker.com/compose/install/linux/).

### 1.2 Atributo `version: '3.8'` obsoleto en `docker-compose.yml`
- **En la guía:** El encabezado del archivo especifica `version: '3.8'`.
- **Estado actual:** La especificación moderna de Compose (*Compose Specification*) unificó el formato y declaró obsoleta la clave de nivel superior `version`. Docker Compose emite una advertencia formal al procesarla:
  ```text
  the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion
  ```
- **Recomendación:** Omitir la clave `version` por completo; iniciar el archivo directamente con `services:`.
- **Fuente oficial:** [Compose Specification - Version attribute](https://github.com/compose-spec/compose-spec/blob/master/spec.md#version-top-level-element).

### 1.3 Variables `${UID}` y `${GID}` no exportadas en el entorno
- **En la guía:** En el servicio `n8n` se indica:
  ```yaml
  user: "${UID}:${GID}"  # Usa tu usuario actual
  ```
- **Estado actual:** En entornos Unix típicos (Bash / Zsh), `$UID` es una variable interna de solo lectura que **no está exportada** a las variables de entorno del proceso hijo (`env` no contiene `UID`). `$GID` habitualmente ni siquiera existe (se usa `id -g`). Al ejecutar `docker compose config` o `docker compose up -d`, Compose emite warnings:
  ```text
  The "UID" variable is not set. Defaulting to a blank string.
  The "GID" variable is not set. Defaulting to a blank string.
  ```
  Esto evalúa `user:` a `":"`, lo que en la práctica provoca que el contenedor arranque como usuario `root` (comprobado empíricamente en Docker 29 / Compose v5.5), o bien falle en ciertos sistemas con error de parsing de usuario.
- **Recomendación:**
  1. Si se desea ejecutar como el usuario por defecto del contenedor (`node`, UID 1000), omitir la directiva `user:`.
  2. Si se desea mapear el usuario del host, crear un archivo `.env` local con `UID=$(id -u)` y `GID=$(id -g)`, o pasar explícitamente las variables antes del comando: `UID=$(id -u) GID=$(id -g) docker compose up -d`.
- **Fuente oficial:** [n8n Docker permissions guide](https://docs.n8n.io/hosting/installation/docker/#docker-user).

### 1.4 Bind mount `~/.n8n` vs. Volumen nombrado `n8n_data`
- **En la guía:**
  ```yaml
  volumes:
    - ~/.n8n:/home/node/.n8n
  ```
- **Estado actual:** La documentación oficial de n8n recomienda explícitamente el uso de un volumen con nombre (`n8n_data:/home/node/.n8n`) gestionado por Docker, en lugar de un bind mount directo al directorio home del usuario.
- **Motivos técnicos:**
  - Los bind mounts sufren problemas de permisos (`EACCES: permission denied`) al cambiar de usuario o entre Linux y Docker en macOS/WSL.
  - En instalaciones de Docker mediante Snap (muy comunes en Ubuntu Server), Docker no tiene acceso directo fuera de `$HOME/snap/docker/` sin permisos de confinamiento especial, lo que hace fallar el bind mount silenciosamente o crear carpetas vacías en rutas inesperadas.
- **Recomendación:** Usar volumen con nombre en `docker-compose.yml`:
  ```yaml
  volumes:
    n8n_data:
  ```
  y en el servicio:
  ```yaml
  volumes:
    - n8n_data:/home/node/.n8n
  ```
- **Fuente oficial:** [n8n self-hosting with Docker Compose](https://docs.n8n.io/deploy/host-n8n/install-options/install-using-docker-compose/).

### 1.5 Registro y etiquetado de la imagen Docker
- **En la guía:** `image: n8nio/n8n` (sin tag de versión).
- **Estado actual:** Al no indicar tag, Docker asume `:latest`. Si n8n publica una nueva versión mayor con cambios disruptivos en la base de datos o en nodos, un reinicio puede romper la instancia del usuario. Además, n8n publica sus imágenes primarias en su propio registro `docker.n8n.io/n8nio/n8n`, además de Docker Hub.
- **Recomendación:** En tutoriales reproducibles, indicar siempre una versión estable concreta o documentar explícitamente el uso de variables de entorno para fijarla:
  `image: docker.n8n.io/n8nio/n8n:${N8N_VERSION:-latest}`
- **Fuente oficial:** [n8n Docker releases](https://docs.n8n.io/deploy/host-n8n/install-options/install-with-docker/#updating).

---

## 2. Discrepancias en la instalación de Docker en Ubuntu

### 2.1 Repositorio y claves GPG oficiales de Docker
- **En la guía:**
  ```bash
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
  ```
  y se añade la línea de repositorio tradicional en `/etc/apt/sources.list.d/docker.list`.
- **Estado actual:** Docker actualizó sus instrucciones oficiales para Ubuntu Noble (24.04) y Jammy (22.04):
  - La clave GPG se guarda en `/etc/apt/keyrings/docker.asc` con permisos `0644`.
  - El archivo de fuentes usa el nuevo formato Deb822 en `/etc/apt/sources.list.d/docker.sources` o formato deb con la opción `signed-by=/etc/apt/keyrings/docker.asc`.
  - El paquete `docker-compose` de apt ya no se recomienda; se instala `docker-compose-plugin` (junto con `docker-buildx-plugin`).
- **Fuente oficial:** [Install Docker Engine on Ubuntu (docs.docker.com)](https://docs.docker.com/engine/install/ubuntu/).

### 2.2 Comando destructivo `rm -rf ~/.n8n`
- **En la guía:** En la sección "Detener n8n y eliminar contenedor/imagen" se sugiere como opcional:
  ```bash
  rm -rf ~/.n8n
  ```
- **Riesgo:** Si un usuario ejecuta esto creyendo que es una limpieza rutinaria, borra de forma irrecuperable:
  1. Su base de datos SQLite (`database.sqlite`) con todos los flujos de trabajo.
  2. Sus credenciales cifradas (claves API de servicios externos).
  3. La clave de cifrado maestra (`config` / encryption key).
- **Recomendación para el guion:** Advertir explícitamente al espectador de que **nunca** debe borrar ese directorio a menos que quiera destruir intencionadamente toda su instancia desde cero, y mostrar cómo hacer copia de seguridad antes.

---

## 3. Estado de verificación práctica en este entorno

- **Entorno probado:**
  - Docker 29.8.0 / Docker Compose v5.5.1 en Ubuntu Linux 7.0.0 kernel x86_64.
- **Resultado empírico del docker-compose.yml de la guía:**
  - `docker compose config` emitió:
    - Advertencia `attribute 'version' is obsolete`.
    - Advertencia `"UID" variable is not set`.
    - Advertencia `"GID" variable is not set`.
  - Con un puerto aislado (`15678`), el contenedor descargó e inició correctamente en 42 segundos ejecutando las migraciones internas de base de datos de n8n v1.82+.
  - La directiva `user: ":"` provocó que el proceso arrancara como `root` en lugar del usuario no privilegiado `node`.
  - Al reemplazar por un volumen nombrado y omitir `version` y `user:`, el contenedor arranca limpiamente sin advertencias como usuario `node` (UID 1000).
