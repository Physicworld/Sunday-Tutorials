# tools/

## transcribe.py — subtítulos y texto del curso (faster-whisper)

Transcribe los videos del curso a `.srt` (subtítulos para YouTube) y `.txt` (texto plano) con
[faster-whisper](https://github.com/SYSTRAN/faster-whisper), en CPU con cuantización int8.
No modifica los videos y no guarda audio ni modelos en el repo: el modelo se descarga una vez a la
caché de Hugging Face del usuario (`~/.cache/huggingface`).

### Instalación

```bash
uv venv --python 3.12 .venv && . .venv/bin/activate && uv pip install -r tools/requirements.txt
# o con pip: python3.12 -m venv .venv && . .venv/bin/activate && pip install -r tools/requirements.txt
```

Usa Python 3.12 (o 3.11): con el Python 3.14 del sistema `ctranslate2` puede no tener wheels.
`ffmpeg` no hace falta: faster-whisper decodifica el audio con PyAV.

### Uso

```bash
python tools/transcribe.py --limit 1               # prueba rápida (1 video pendiente)
python tools/transcribe.py                         # todos los videos
python tools/transcribe.py --model tiny --only Strategy --output /tmp/prueba   # ensayo sin tocar el repo
python tools/transcribe.py --force --only Singleton  # regenerar un video
```

| Opción | Default | Descripción |
| --- | --- | --- |
| `--input DIR` | `$TUTORIALS_MEDIA_DIR`, si no `/home/sundaythequant/Videos/SundayTheQuant/curso-patrones`, si no existe `Curso Patrones Diseno Python/` del repo | Videos (`.mkv .mp4 .mov .webm .m4v .avi`), búsqueda recursiva |
| `--output DIR` | `Curso Patrones Diseno Python/subtitulos` | Salida: `<DIR>/<Grupo>/<Video>.srt` y `.txt` (misma estructura que la entrada) |
| `--model` | `small` | `tiny`, `base`, `small`, `medium`, `large-v3`... |
| `--language` | `es` | Código de idioma o `auto` |
| `--limit N` | todos | Máximo de videos pendientes a procesar |
| `--only TEXTO` | — | Solo rutas relativas que contengan TEXTO |
| `--force` | — | Regenera aunque existan salidas (por defecto se omiten) |
| `--device`, `--compute-type`, `--cpu-threads` | `cpu`, `int8`, `0` | Con GPU: `--device cuda --compute-type float16` (requiere CUDA/cuDNN) |

Notas:

- Las salidas se escriben de forma atómica (`.tmp` + rename): una ejecución interrumpida se puede
  relanzar y continúa donde se quedó.
- Los SRT corresponden al master indicado en `--input` en el momento de ejecutar. Tras editar o
  reexportar un video hay que regenerarlo (`--force --only <Video>`).
- Las marcas de tiempo son monótonas y nunca superan la duración del video.
- Whisper `small` comete errores con términos técnicos (nombres de patrones, identificadores de
  código): revisa los SRT antes de subirlos a YouTube.
- En un portátil de 16 hilos, `small` int8 transcribe muy por encima del tiempo real.
