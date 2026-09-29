#!/usr/bin/env python3
"""Transcribe los videos del curso a SRT + TXT con faster-whisper.

Recorre ``--input`` de forma recursiva, y por cada video escribe
``<output>/<subcarpeta>/<nombre>.srt`` y ``.txt`` (misma estructura de grupos).
Las salidas existentes se omiten (usa ``--force`` para regenerarlas).
Nunca modifica los videos ni guarda audio/modelos dentro del repo: el modelo se
descarga a la caché de Hugging Face del usuario.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
COURSE_DIR = REPO_ROOT / "Curso Patrones Diseno Python"
DEFAULT_MEDIA_DIR = Path("/home/sundaythequant/Videos/SundayTheQuant/curso-patrones")
DEFAULT_OUTPUT_DIR = COURSE_DIR / "subtitulos"
VIDEO_EXTENSIONS = {".mkv", ".mp4", ".mov", ".webm", ".m4v", ".avi"}


def default_input_dir() -> Path:
    """``$TUTORIALS_MEDIA_DIR``, o el directorio de masters; si no existe, el del repo."""
    env = os.environ.get("TUTORIALS_MEDIA_DIR")
    if env:
        return Path(env).expanduser()
    if DEFAULT_MEDIA_DIR.is_dir():
        return DEFAULT_MEDIA_DIR
    return COURSE_DIR


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--input", type=Path, default=None,
                   help="directorio con los videos (default: $TUTORIALS_MEDIA_DIR, "
                        f"{DEFAULT_MEDIA_DIR} o, si no existe, el directorio del curso en el repo)")
    p.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_DIR,
                   help=f"directorio de salida (default: {DEFAULT_OUTPUT_DIR.relative_to(REPO_ROOT)})")
    p.add_argument("--model", default="small", help="tiny, base, small, medium, large-v3... (default: small)")
    p.add_argument("--language", default="es", help="código de idioma, 'auto' para detectarlo (default: es)")
    p.add_argument("--limit", type=int, default=None, metavar="N",
                   help="transcribe como máximo N videos pendientes (los ya existentes no cuentan)")
    p.add_argument("--device", default="cpu", help="cpu | cuda | auto (default: cpu)")
    p.add_argument("--compute-type", default="int8",
                   help="int8 (CPU), float16 (GPU), ... (default: int8)")
    p.add_argument("--cpu-threads", type=int, default=0, help="hilos de CPU (0 = valor por defecto de ctranslate2)")
    p.add_argument("--only", default=None, metavar="TEXTO",
                   help="solo videos cuya ruta relativa contenga TEXTO (sin distinguir mayúsculas)")
    p.add_argument("--force", action="store_true", help="regenera aunque existan .srt y .txt")
    return p.parse_args(argv)


def find_videos(root: Path, exclude: Path | None = None) -> list[Path]:
    videos = []
    for path in sorted(root.rglob("*")):
        if path.suffix.lower() not in VIDEO_EXTENSIONS or not path.is_file():
            continue
        if exclude is not None and exclude.resolve() in path.resolve().parents:
            continue
        videos.append(path)
    return videos


def srt_timestamp(seconds: float) -> str:
    ms = max(0, round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def transcribe_video(model, video: Path, srt_path: Path, txt_path: Path, language: str | None) -> tuple[int, float]:
    """Transcribe ``video``; devuelve (nº de segmentos, duración en segundos)."""
    segments, info = model.transcribe(
        str(video),
        language=language,
        beam_size=5,
        vad_filter=True,
        condition_on_previous_text=False,  # evita bucles/alucinaciones encadenadas
    )
    duration = float(info.duration)
    srt_blocks: list[str] = []
    lines: list[str] = []
    last_end = 0.0
    for seg in segments:
        text = seg.text.strip()
        if not text:
            continue
        # Marcas monótonas y dentro de la duración real del video.
        start = min(max(seg.start, last_end), duration)
        end = min(max(seg.end, start), duration)
        last_end = end
        srt_blocks.append(f"{len(srt_blocks) + 1}\n{srt_timestamp(start)} --> {srt_timestamp(end)}\n{text}\n")
        lines.append(text)
        if sys.stdout.isatty():
            print(f"  [{srt_timestamp(end)} / {srt_timestamp(duration)}]", end="\r", flush=True)
    write_atomic(srt_path, "\n".join(srt_blocks))
    write_atomic(txt_path, "\n".join(lines) + "\n")
    return len(srt_blocks), duration


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    input_dir = (args.input or default_input_dir()).expanduser()
    output_dir = args.output.expanduser()
    if not input_dir.is_dir():
        print(f"error: el directorio de entrada no existe: {input_dir}", file=sys.stderr)
        return 2

    videos = find_videos(input_dir, exclude=output_dir)
    if args.only:
        videos = [v for v in videos if args.only.lower() in str(v.relative_to(input_dir)).lower()]
    if not videos:
        print(f"error: no hay videos en {input_dir}", file=sys.stderr)
        return 2

    jobs = []
    for video in videos:
        rel = video.relative_to(input_dir).with_suffix("")
        srt_path, txt_path = output_dir / rel.with_suffix(".srt"), output_dir / rel.with_suffix(".txt")
        if not args.force and srt_path.exists() and txt_path.exists():
            print(f"omitido (ya existe): {rel}")
            continue
        jobs.append((video, rel, srt_path, txt_path))
    if args.limit is not None:
        jobs = jobs[: args.limit]
    if not jobs:
        print("nada que hacer")
        return 0

    from faster_whisper import WhisperModel  # import tardío: --help no requiere la dependencia

    print(f"modelo={args.model} device={args.device} compute_type={args.compute_type} "
          f"videos pendientes={len(jobs)}", flush=True)
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type,
                         cpu_threads=args.cpu_threads)
    language = None if args.language == "auto" else args.language

    failures = 0
    for i, (video, rel, srt_path, txt_path) in enumerate(jobs, 1):
        print(f"[{i}/{len(jobs)}] {rel}", flush=True)
        t0 = time.monotonic()
        try:
            n, duration = transcribe_video(model, video, srt_path, txt_path, language)
        except Exception as exc:  # un video roto no debe abortar el lote
            failures += 1
            print(f"\n  ERROR en {rel}: {exc}", file=sys.stderr, flush=True)
            continue
        elapsed = time.monotonic() - t0
        print(f"  {n} segmentos, {duration:.0f}s de audio en {elapsed:.0f}s "
              f"({duration / max(elapsed, 1e-9):.1f}x tiempo real)", flush=True)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
