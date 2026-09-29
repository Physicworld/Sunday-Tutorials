# Curso Machine Learning

Material de apoyo del curso de Udemy «Ciencia de datos con Python y R» (complementario; el curso es de pago y no se redistribuye aquí). Contiene solo los CSV de la carpeta `datasets/` y un ejemplo ejecutable.

## Ejecutar el ejemplo

```bash
cd 'Curso Machine Learning'
pip install -r requirements.txt      # Python 3.11+
python titanic_baseline.py
```

`titanic_baseline.py` limpia los datos (imputa `Age`, `Fare`, etc. y codifica `Sex`/`Embarked` en one-hot, todo dentro de un `Pipeline` de scikit-learn para evitar fuga de datos) y entrena un `RandomForestClassifier` sobre `train_titanic.csv`. Salida esperada (semilla fija):

```
Filas: 891  |  Referencia (predecir siempre 'no sobrevive'): 0.616
Accuracy (CV 5 particiones): 0.823 ± 0.030
```

## Datasets (`datasets/`)

### Titanic — `train_titanic.csv` (891 filas), `test_titanic.csv` (418 filas)

Origen: competición de Kaggle «[Titanic - Machine Learning from Disaster](https://www.kaggle.com/competitions/titanic)» (`train.csv` / `test.csv` renombrados). `test_titanic.csv` **no trae la columna `Survived`** (es el conjunto de evaluación ciego de Kaggle), por eso el ejemplo valida con validación cruzada sobre el de entrenamiento.

| Columna | Descripción |
| --- | --- |
| `PassengerId` | Identificador del pasajero |
| `Survived` | Objetivo: 0 = no sobrevivió, 1 = sobrevivió (solo en train) |
| `Pclass` | Clase del billete: 1, 2 o 3 |
| `Name` | Nombre |
| `Sex` | `male` / `female` |
| `Age` | Edad en años (faltan 177 en train) |
| `SibSp` | Hermanos/cónyuges a bordo |
| `Parch` | Padres/hijos a bordo |
| `Ticket` | Número de billete |
| `Fare` | Tarifa pagada |
| `Cabin` | Camarote (faltan 687 en train) |
| `Embarked` | Puerto de embarque: C, Q o S (faltan 2 en train) |

> **Licencia / redistribución (pendiente de decisión del dueño):** estos ficheros proceden de una competición de Kaggle, cuyas reglas limitan el uso de los datos a la competición y a fines académicos/no comerciales, y en general no permiten republicarlos fuera de Kaggle. No se ha podido confirmar un permiso explícito para redistribuirlos en un repositorio público. No se han borrado; si prefieres no alojarlos, la alternativa es descargarlos desde Kaggle (`kaggle competitions download -c titanic`) y apuntar `DATA` en `titanic_baseline.py` a esa ruta.

### `dataset_1.csv` y `tratamiento_datos.csv` (100 000 filas cada uno)

Datos **sintéticos** para practicar limpieza de datos (origen: material del curso). Ambos tienen el mismo contenido y columnas; solo difieren en los saltos de línea del archivo. La primera columna (sin nombre) es el índice.

| Columna | Descripción | Problemas de calidad intencionados |
| --- | --- | --- |
| *(índice)* | Número de fila | — |
| `Edad` | Edad en años | Valores imposibles: de −10 a 200 |
| `Género` | `M` / `F` | 10 000 vacíos |
| `Ingresos` | Ingresos anuales | Negativos (mín. −2000) |
| `Altura` | Altura en metros (1.50–2.00) | — |
| `Ciudad` | Chicago, New York, Houston, Phoenix, Los Angeles | 10 000 vacíos |
| `Nivel_Educación` | PhD, Master, Bachelor y variantes | Erratas (`mastre`, `pHd`, `Bachelors`), `no education`, el texto `None` (pandas lo lee como nulo) y ~22 % vacíos |
| `Hijos` | Número de hijos | Negativos (mín. −5) |

Los CSV no se modifican en este repositorio.
