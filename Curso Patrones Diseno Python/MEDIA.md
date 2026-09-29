# Videos del curso de Patrones de Diseño

Los videos **ya no se versionan en git** (el repo es público y los masters pesan ~346 MB). Viven en un directorio de medios fuera del árbol:

- `MEDIA_DIR` = `$TUTORIALS_MEDIA_DIR`, por defecto `~/Videos/SundayTheQuant/curso-patrones`.
- Convención para scripts: leer la variable de entorno `TUTORIALS_MEDIA_DIR` y, si no existe, usar el valor por defecto.
- Estructura: `MEDIA_DIR/{Creacionales,Estructurales,Comportamiento}/<archivo>`.
- `.gitignore` excluye `*.mkv`, `*.mp4` y `*.mov`.

```python
import os
from pathlib import Path

MEDIA_DIR = Path(os.environ.get("TUTORIALS_MEDIA_DIR", "~/Videos/SundayTheQuant/curso-patrones")).expanduser()
```

## Archivos

| Ubicación en `MEDIA_DIR` | Rol | Duración | Tamaño | sha256 |
| --- | --- | --- | --- | --- |
| `Creacionales/AbstractFactory.mkv` | master editado | 7:53 | 15.2 MB | `10bb2f4c0c639b1896821d5a2c5c17cba5527d764b3e4493ba6d170721090706` |
| `Creacionales/Builder.mkv` | master editado | 11:59 | 22.7 MB | `4b93fe81000911803d5cdef90bb806b2b775cef2fd355678faa5078d7e633546` |
| `Creacionales/FactoryMethod.mp4` | master editado | 13:11 | 50.8 MB | `72e9101cc8bab403b100f9edbc95f05f1e6f83c86499f76e7ba6d906ab7ff5a3` |
| `Creacionales/FactoryMethodsineditar.mkv` | CRUDO (sin editar) — **no publicar** | 18:56 | 33.8 MB | `b650ec633dc9ee5ee333517b4aa10f787aff0378ea83892ca6f7dbf4c68dd14d` |
| `Creacionales/Introduccion.mkv` | master editado — intro del curso | 12:15 | 22.8 MB | `a58de6a21d67191dc63ce49374fbff82e8e423e7edac0e0662530f7d6ef5845d` |
| `Creacionales/Prototype.mkv` | master editado | 6:47 | 12.8 MB | `869f309b4abe23ac59d48a864c41adac40a365a8bb022428b9df0daebb1b2709` |
| `Creacionales/Singleton.mkv` | master editado | 8:22 | 15.5 MB | `653f338c297afd4a606011d20b480efa15410d17e57b900aa4ab31afb024126b` |
| `Estructurales/Adapter.mkv` | master editado | 12:04 | 22.5 MB | `21de99d78209964e13573b0bc1b06b81f534e6681af1b875a83f357368e2ccce` |
| `Estructurales/Bridge.mkv` | master editado | 11:47 | 23.7 MB | `2d103ca0b89494ba9447f20a0ff1b58916d8221b97fb64411e41c336f7b9409c` |
| `Estructurales/Composite.mkv` | master editado | 6:55 | 13.2 MB | `7f1ab28cd9fa4764b3f9e7d62731293c10f2be9b1321684fe6dd4249354b1c39` |
| `Estructurales/Decorator.mkv` | master editado | 7:39 | 14.5 MB | `66cfdf2d0bea4c7967c3656b61e76dbcc42534df38cf1cd580a393f7905391a2` |
| `Estructurales/Facade.mkv` | master editado | 8:55 | 17.4 MB | `139f22c6ac658bfd89a2aac07d10762c3a3736a4d0441d0190a76b7cb84090a6` |
| `Estructurales/Flyweight.mkv` | master editado | 7:48 | 14.6 MB | `aaff636f494fd8ff47cb413b8652a5ac18585a436269c8e911d64b28406135e9` |
| `Comportamiento/ChainOfResponsibility.mkv` | master editado | 8:27 | 17.5 MB | `dbc94ec3306555b0c55c9cdac9ca28a501d6ac7e9f4c317172a16572ee9df296` |
| `Comportamiento/Command.mkv` | master editado | 8:56 | 17.6 MB | `7ce030bc90328dacdb7a59a6b07ca8dd06361f34c256a1fdb626b575274acbda` |
| `Comportamiento/Observer.mkv` | master editado | 7:17 | 14.0 MB | `0eb898d03485072f6ace803481c0fe001d2552d4323bcf07821120146c3f07a4` |
| `Comportamiento/State.mkv` | master editado | 9:35 | 20.0 MB | `ea77fc41b0020cf3b5228a56ac8807f488efe9b6d19d2739505315d31f078942` |
| `Comportamiento/Strategy.mkv` | master editado | 6:10 | 12.0 MB | `6c9d1fb45f442882deff1960be50813c9bd1b53dfabb21bb47f85be38508fedb` |

Total: 18 archivos, 361 MB; 17 publicables (todos menos el crudo).

## Renombrado

- `Comportamiento/ChainOfResponsability.mkv` (nombre antiguo en git, con errata) → `Comportamiento/ChainOfResponsibility.mkv`.

## Verificación de integridad

El sha256 de cada archivo coincide con el del blob que había en git (`git show <commit-anterior>:<ruta> | sha256sum`). Para comprobar la copia local:

```bash
cd "$TUTORIALS_MEDIA_DIR" && sha256sum -c <(awk -F'`' '/^\| `/ {print $4"  "$2}' "Curso Patrones Diseno Python/MEDIA.md")
```

## Respaldo

Los videos siguen presentes en el historial de git (anterior a este cambio). Se recomienda mantener además una copia externa (Nextcloud/Drive) de `MEDIA_DIR`.
