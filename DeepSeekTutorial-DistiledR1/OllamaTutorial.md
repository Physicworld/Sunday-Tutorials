Antes de continuar con el tutorial te recomiendo que te inscribas a mi curso de ciencia de datos con python, para poder seguir creando contenido gratuito.

https://www.udemy.com/course/ciencia-de-datos-con-python-r/?referralCode=B9A5A600EEECE5E538C1


### **Guía de Instalación de Ollama en Ubuntu/Mac/Linux**

#### **1. Actualizar los Sistemas de Paquetes**
Antes de proceder, actualiza tus paquetes para asegurarte de tener la Última Versión:

```bash
sudo apt-get update
```

---

#### **2. Instalar Drivers de NVIDIA (Opcional)**
Si el driver de tu GPU no está correctamente instalado, instalalo siguiendo estos pasos:

1. Ejecuta el comando siguiente para ver si los drivers actuales están disponibles:
   ```bash
   nvidia-smi
   ```
2. Si los drivers no están listados o si hay problemas, instalalos desde una fuente confiable (p.e., sitio web 
oficial de NVIDIA):
   - En http://www.nvidia.com/Download/index.aspx
   - Busca el driver correcto para tu tarjeta gráfica.
   
3. Instala los drivers con:
   ```bash
   sudo apt install nvidia-drivers
   ```

---

#### **3. Instalar elToolkit CUDA**
El toolkit CUDA de NVIDIA es necesario para ejecutar aplicaciones que requieren CUDA (paralelismo).

Ejecuta estos comandos para instalar CUDA:

```bash
sudo apt install nvidia-cuda-toolkit
```

Verifica si CUDA está correctamente-installed con:

```bash
nvcc --version
```

---

#### **4. Instalar Ollama**
Ollama es una plataforma que permite ejecutar modelos de IA en tu computadora local.

##### **a) Instalar `curl` para obtener el script de instalacion:**
```bash
sudo apt-get install curl
```

##### **b) Descargar e instalar Ollama:**
Ejecuta los siguientes comandos para descargar y instalar Ollama:

```bash
curl https://ollama.ai/install.sh | sh
```

Otra opción es Instalar directamente desde el sitio web de Ollama:
- Ir al siguiente enlace: [https://ollama.ai](https://ollama.ai)
- Busca el botón para instalar Ollama en tu sistema.

---

#### **5. Ejecutar un Modelo con Ollama**
Después de la Instalación, puedes ejecutar modelos como este:

```bash
ollama run deepseek-r1:1.5b
```

Aquí está un ejemplo completo del comando para ejecutar el modelo "deepseek-r1" con una configuración de 1 
billón de parámetros (1.5B):

```bash
ollama run deepseek-r1:1.5b --task text-generation \
--temperature 0.7 \
--max-length 100 \
--top_p 0.7
```

---

Espero que esta guía te sea útil para instalar y usar Ollama en tu sistema. Si encounteras algún problema, 
revisa los pasos detenidamente o envíame un mensaje para ayudarte más. ¡Buena suerte!

