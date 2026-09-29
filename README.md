# Sunday-Tutorials

Repositorio oficial de tutoriales y proyectos prácticos del canal **SundayTheQuant**. Cubre temas de **Trading Cuantitativo**, **Inteligencia Artificial local y LLMs**, **Heurísticas y Optimización**, **Métodos Numéricos** e **Ingeniería de Software / C++**.

## Requisitos Globales

Cada módulo especifica sus dependencias en su propia carpeta (vía `requirements.txt` o documentación). A nivel general, el entorno de trabajo utiliza:

- **Python 3.11+** (recomendado crear un entorno virtual por módulo con `python3 -m venv .venv`).
- **Docker y Docker Compose** para la automatización autoalojada en [N8N Tutorial](N8N%20Tutorial/).
- **CMake 3.15+**, **compilador C++17** (`g++` o `clang++`), **pybind11** y **libtbb-dev** (Intel oneTBB) para extensiones de alto rendimiento en [SpeedUpPython](SpeedUpPython/).
- **Ollama** para agentes locales y modelos abiertos en [AgentMCP](AgentMCP/) y [DeepSeekTutorial-DistiledR1](DeepSeekTutorial-DistiledR1/).
- **LM Studio** para ejecución local de LLMs compatibles con OpenAI en [LLMStudio](LLMStudio/).

## Catálogo de Módulos

| Módulo | Qué enseña | Estado | Requisitos | Comando de arranque |
| --- | --- | --- | --- | --- |
| [AgentMCP](AgentMCP/) | Agente autónomo local con Ollama conectado a herramientas vía servidor FastMCP | Listo | Python 3.11+, Ollama | `cd AgentMCP && pip install -r requirements.txt && python agent.py` |
| [AlgorithmicTrading](AlgorithmicTrading/) | Backtesting de medias móviles, análisis de ciclos de Bitcoin y cadenas de Markov | Listo | Python 3.11+, Jupyter, pandas, yfinance | `cd AlgorithmicTrading/Backtesting && jupyter notebook backtesting.ipynb` |
| [SpeedUpPython](SpeedUpPython/) | Aceleración de cómputo en Python mediante C++, pybind11 y paralelismo con Intel TBB | Listo | CMake 3.15+, C++17, TBB, pybind11 | `cd SpeedUpPython && cmake -B build && cmake --build build && python compare.py` |
| [DeepSeekTutorial-DistiledR1](DeepSeekTutorial-DistiledR1/) | Guía de despliegue y uso local de modelos DeepSeek R1 destilados con Ollama | Listo | Ollama | `ollama run deepseek-r1:8b` (ver [guía](DeepSeekTutorial-DistiledR1/OllamaTutorial.md)) |
| [GridBot](GridBot/) | Bot de trading en cuadrícula (grid) para Bybit spot usando `ccxt` con credenciales por entorno | Listo | Python 3.11+, ccxt, python-dotenv | `cd GridBot && pip install -r requirements.txt && python main.py` |
| [Heuristics](Heuristics/) | Optimización mediante Algoritmos Genéticos (GA) para maximización de funciones | Listo | Python 3.11+, numpy, matplotlib | `cd Heuristics && python GA.py` |
| [N8N Tutorial](N8N%20Tutorial/) | Automatización de flujos de trabajo sin código con n8n autoalojado en contenedor Docker | Listo | Docker | `docker run -it --rm --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n docker.n8n.io/n8nio/n8n` |
| [Curso Patrones Diseno Python](Curso%20Patrones%20Diseno%20Python/) | Curso completo de Patrones de Diseño GoF (16 patrones implementados con tests) | Pendiente de publicar | Python 3.11+, pytest | `pytest "Curso Patrones Diseno Python"` |
| [ChatGPT3Test](ChatGPT3Test/) | Generación y backtesting experimental de estrategias de trading en Bitcoin con OpenAI | Incompleto / Experimental | Python 3.11+, openai, OPENAI_API_KEY | `cd ChatGPT3Test && python bitcoinstrategy.py` |
| [Curso Machine Learning](Curso%20Machine%20Learning/) | Datasets clásicos (Titanic) y análisis exploratorio inicial | Incompleto / Experimental | Python 3.11+, pandas, scikit-learn | `cd "Curso Machine Learning/datasets" && python titanic_baseline.py` |
| [Fourier Transform](Fourier%20Transform/) | Transformada Rápida de Fourier (FFT) y descomposición espectral de series temporales | Incompleto / Experimental | Python 3.11+, numpy, scipy, matplotlib | `cd "Fourier Transform" && python fft.py` |
| [LLMStudio](LLMStudio/) | Integración programática con servidor local LM Studio mediante API compatible con OpenAI | Incompleto / Experimental | Python 3.11+, LM Studio | `cd LLMStudio && pip install -r requirements.txt && python main.py` |
| [MachineLearning](MachineLearning/) | Implementaciones desde cero de algoritmos de ML (k-NN, K-Means, Perceptrón, Redes Neuronales) | Incompleto / Experimental | Python 3.11+, numpy, matplotlib | `cd MachineLearning` (ver subcarpetas) |
| [NumericalMethods](NumericalMethods/) | Métodos numéricos para cálculo científico (método de bisección con tests) | Incompleto / Experimental | Python 3.11+, pytest | `cd NumericalMethods/Bisection && python Bisection.py` |
| [OpenAIPythonAPI](OpenAIPythonAPI/) | Ejemplos de uso de la API de OpenAI (generación de texto y síntesis de voz Text-to-Speech) | Incompleto / Experimental | Python 3.11+, openai, OPENAI_API_KEY | `cd OpenAIPythonAPI && jupyter notebook openaipython.ipynb` |

## Curso de Patrones de Diseño en Python

Ubicado en [Curso Patrones Diseno Python](Curso%20Patrones%20Diseno%20Python/), el curso cubre **16 patrones de diseño GoF** organizados en los tres grupos clásicos, con un total de **17 videos publicables** (de entre 6 y 13 minutos) y suites de tests automatizados:

- **Creacionales** (5 patrones, 6 videos publicables + 1 video crudo de referencia):
  - *Introducción al curso* (video introductorio)
  - Abstract Factory
  - Builder
  - Factory Method (más `FactoryMethodsineditar.mkv`, versión cruda sin editar de 18 min conservada fuera del repo)
  - Prototype
  - Singleton
- **Estructurales** (6 patrones, 6 videos publicables):
  - Adapter, Bridge, Composite, Decorator, Facade, Flyweight.
- **Comportamiento** (5 patrones, 5 videos publicables):
  - Chain of Responsibility, Command, Observer, State, Strategy.

> **Nota sobre los videos:** De acuerdo con la política de higiene del repositorio, los masters de video (`.mkv`, `.mp4`) no se versionan en Git para mantener el repo ligero. Los archivos de video viven en el directorio local de medios configurado por la variable de entorno `TUTORIALS_MEDIA_DIR` (por defecto `~/Videos/SundayTheQuant/curso-patrones`). Para consultar la tabla completa de checksums sha256, roles y duraciones, revisa [Curso Patrones Diseno Python/MEDIA.md](Curso%20Patrones%20Diseno%20Python/MEDIA.md).

## Aviso Legal / No Asesoría Financiera

> **Aviso:** El código, las estrategias y los análisis contenidos en este repositorio (incluyendo [GridBot](GridBot/), [AlgorithmicTrading](AlgorithmicTrading/) y [ChatGPT3Test](ChatGPT3Test/)) tienen fines estrictamente **educativos y demostrativos**. **No constituyen asesoramiento financiero, recomendación de inversión ni solicitud de compra/venta de ningún activo o instrumento financiero.** El trading cuantitativo y las criptomonedas conllevan un riesgo sustancial de pérdida de capital. Opera siempre bajo tu propia responsabilidad.

## Cursos Recomendados

- [Ciencia de Datos con Python y R](https://www.udemy.com/course/ciencia-de-datos-con-python-r/?referralCode=B9A5A600EEECE5E538C1) en Udemy.
