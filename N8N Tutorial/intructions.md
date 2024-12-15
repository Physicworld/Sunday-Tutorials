Antes de seguir el tutorial te invito a formar parte de mi curso de ciencia de datos, de esta forma me ayudas a poder seguir creando contenido.

https://www.udemy.com/course/ciencia-de-datos-con-python-r/?referralCode=B9A5A600EEECE5E538C1

Tambien te invito a que formes parte de los miembros de mi canal de youtube, dando click en el boton unirme desde la pagina de inicio de mi canal.

Ahora si, vamos a comenzar.



# Tutorial: Instalación de n8n con Docker en Ubuntu

Este tutorial te guiará a través del proceso de instalación y configuración de n8n usando Docker en Ubuntu.

## Contenido
- [Preparación del sistema](#preparación-del-sistema)
- [Instalación de Docker](#instalación-de-docker)
- [Instalación de Docker Compose](#instalación-de-docker-compose)
- [Configuración y despliegue de n8n](#configuración-y-despliegue-de-n8n)
- [Acceso a n8n](#acceso-a-n8n)
- [Comandos útiles](#comandos-útiles)
- [Verificación y solución de problemas](#verificación-y-solución-de-problemas)

## Preparación del sistema

Actualiza los repositorios e instala las dependencias necesarias:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
```

## Instalación de Docker

### 1. Agregar el repositorio oficial de Docker

```bash
# Agregar la clave GPG oficial de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Agregar el repositorio de Docker
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### 2. Instalar Docker Engine

```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io
```

### 3. Verificar la instalación

```bash
# Verificar versión de Docker
docker --version

# Verificar estado del servicio
systemctl status docker

# Verificar la instalación con hello-world
docker run hello-world
```

Si la instalación fue exitosa, el comando `docker run hello-world` descargará una imagen de prueba y mostrará un mensaje de confirmación, verificando que Docker puede:
- Descargar imágenes correctamente
- Crear contenedores
- Ejecutarlos
- Producir salida

### 4. Configurar Docker para ejecutarse sin sudo (recomendado)

```bash
sudo usermod -aG docker $USER
# Importante: Cierra sesión y vuelve a iniciarla para que los cambios surtan efecto
```

## Instalación de Docker Compose

```bash
sudo apt update
sudo apt install -y docker-compose
```

## Configuración y despliegue de n8n

### 1. Crear y configurar directorios

```bash
# Crear directorio para el proyecto
mkdir -p ~/n8n

# Crear directorio para datos persistentes y asignar permisos
mkdir -p ~/.n8n
sudo chown -R $USER:$USER ~/.n8n

cd ~/n8n
```

> Nota: 
> - `~/n8n` es el directorio del proyecto donde estará el docker-compose.yml
> - `~/.n8n` es un directorio oculto donde n8n almacenará sus datos persistentes

### 2. Crear el archivo docker-compose.yml

```bash
nano docker-compose.yml
```

Copia y pega el siguiente contenido:

```yaml
version: '3.8'

services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=${N8N_HOST:-localhost}
      - N8N_PORT=5678
      - N8N_PROTOCOL=${N8N_PROTOCOL:-http}
      - NODE_ENV=production
      - WEBHOOK_URL=${N8N_WEBHOOK_URL:-http://localhost:5678/}
    volumes:
      - ~/.n8n:/home/node/.n8n
    user: "${UID}:${GID}"  # Usa tu usuario actual
    restart: unless-stopped
```

### 3. Iniciar n8n

```bash
docker-compose up -d
```

## Acceso a n8n

Una vez que el contenedor esté en ejecución, accede a n8n a través de tu navegador:

```
http://localhost:5678
```

## Comandos útiles

### Ver logs
```bash
docker-compose logs -f
```

### Detener n8n temporalmente
```bash
docker-compose down
```

### Detener n8n y eliminar contenedor/imagen
```bash
# Detener y eliminar contenedor
docker-compose down

# Eliminar imagen
docker rmi n8nio/n8n

# Opcional: eliminar datos persistentes
rm -rf ~/.n8n
```

### Reiniciar n8n
```bash
docker-compose restart
```

## Verificación y solución de problemas

### Verificar estado del contenedor
```bash
docker ps
```

### Ver logs
```bash
docker logs $(docker ps -q --filter "name=n8n")
```

### Problemas comunes y soluciones

#### 1. Error de permisos (EACCES)
```bash
# Verificar propietario del directorio .n8n
ls -la ~/.n8n

# Corregir permisos si es necesario
sudo chown -R $USER:$USER ~/.n8n
```

#### 2. Puerto en uso
```bash
# Verificar si el puerto 5678 está en uso
sudo lsof -i :5678

# Cambiar el puerto en docker-compose.yml si es necesario
ports:
  - "5679:5678"  # Cambia 5679 por el puerto que desees
```

## Notas importantes
- Los datos persistentes se almacenan en `~/.n8n`
- El puerto predeterminado es 5678
- El contenedor se reiniciará automáticamente después de reinicios del sistema, a menos que lo detengas manualmente
- Para acceder desde otra máquina, reemplaza `localhost` con la IP de tu servidor
- Siempre verifica los logs si encuentras problemas: `docker-compose logs -f`

## Contribuir
Si encuentras algún error o tienes sugerencias para mejorar este tutorial, no dudes en abrir un issue o enviar un pull request.

## Licencia
Este tutorial está bajo la licencia MIT. Siéntete libre de usarlo y modificarlo como necesites.
