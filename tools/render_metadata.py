#!/usr/bin/env python3
"""Renderiza una plantilla de metadatos de YouTube con datos TOML y valida el resultado.

Uso:
    python tools/render_metadata.py --template docs/youtube/plantilla-descripcion-larga.md \\
        --data docs/youtube/enlaces.toml --data mi-video.toml [-o salida.txt] [--allow-todo]

Sintaxis de plantilla (ver docs/youtube/README.md):
    {{clave}}                 valor del TOML (claves con punto: {{seccion.clave}}); las listas se unen con saltos de linea
    {{clave|inline}}          igual, pero las listas se unen con espacios (hashtags)
    {{#if clave}}...{{/if}}   bloque opcional: se elimina si la clave no existe o esta vacia/false (sin anidar)
    {{> archivo.md}}          incluye otro archivo (ruta relativa a la plantilla) en una linea propia
    <!-- ... -->              comentario: se elimina del resultado

Sale con codigo 1 si queda un placeholder sin definir, si un valor usado es un marcador
TODO_OWNER / TODO_LINK (salvo --allow-todo) o si la descripcion incumple los limites de YouTube.
Solo biblioteca estandar (Python >= 3.11 por tomllib).
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path

TODO_MARKERS = ("TODO_OWNER", "TODO_LINK")
MAX_DESCRIPTION_BYTES = 5000
MAX_TITLE_CHARS = 100
MAX_HASHTAGS = 15
MIN_CHAPTERS = 3
MIN_CHAPTER_GAP_SECONDS = 10
MAX_INCLUDE_DEPTH = 5

COMMENT = re.compile(r"<!--.*?-->[ \t]*\n?", re.S)
INCLUDE = re.compile(r"^\{\{>\s*([\w./-]+)\s*\}\}[ \t]*\n?", re.M)
IF_BLOCK = re.compile(r"\{\{#if\s+([\w.]+)\s*\}\}\n?(.*?)\{\{/if\}\}[ \t]*\n?", re.S)
VAR = re.compile(r"\{\{\s*([A-Za-z_][\w.]*)(?:\s*\|\s*(inline))?\s*\}\}")
CHAPTER = re.compile(r"^\s*((?:\d+:)?\d{1,2}:\d{2})\s+\S", re.M)


def lookup(data: dict, dotted: str):
    """Devuelve data[a][b]... o lanza KeyError si falta algun tramo."""
    value = data
    for part in dotted.split("."):
        if not isinstance(value, dict) or part not in value:
            raise KeyError(dotted)
        value = value[part]
    return value


def is_truthy(value) -> bool:
    return bool(value)


def has_todo(text: str) -> str | None:
    return next((m for m in TODO_MARKERS if m in text), None)


def load_template(path: Path, depth: int = 0) -> str:
    """Lee la plantilla, quita comentarios y expande includes."""
    if depth > MAX_INCLUDE_DEPTH:
        raise ValueError(f"includes demasiado anidados en {path}")
    text = COMMENT.sub("", path.read_text(encoding="utf-8"))

    def expand(match: re.Match) -> str:
        target = (path.parent / match.group(1)).resolve()
        if not target.is_file():
            raise ValueError(f"include no encontrado: {match.group(1)} (desde {path})")
        included = load_template(target, depth + 1)
        return included if included.endswith("\n") else included + "\n"

    return INCLUDE.sub(expand, text)


def stringify(value, inline: bool = False) -> str:
    if isinstance(value, list):
        return (" " if inline else "\n").join(str(item) for item in value)
    return str(value)


def render(template: str, data: dict, allow_todo: bool) -> tuple[str, list[str]]:
    errors: list[str] = []

    def keep_block(match: re.Match) -> str:
        try:
            keep = is_truthy(lookup(data, match.group(1)))
        except KeyError:
            keep = False
        return match.group(2) if keep else ""

    template = IF_BLOCK.sub(keep_block, template)

    leftover = VAR.sub("", template)
    for stray in ("{{", "}}"):
        if stray in leftover:
            line = next(n for n, l in enumerate(leftover.splitlines(), 1) if stray in l)
            errors.append(f"sintaxis de plantilla invalida: '{stray}' suelto cerca de la linea {line} (bloques #if sin cerrar o anidados?)")

    missing: list[str] = []
    todos: list[str] = []

    def substitute(match: re.Match) -> str:
        key = match.group(1)
        try:
            value = stringify(lookup(data, key), inline=bool(match.group(2)))
        except KeyError:
            if key not in missing:
                missing.append(key)
            return match.group(0)
        marker = has_todo(value)
        if marker and not allow_todo and key not in todos:
            todos.append(key)
        return value

    output = VAR.sub(substitute, template)
    if missing:
        errors.append("placeholders sin definir en los datos: " + ", ".join(f"{{{{{k}}}}}" for k in missing))
    if todos:
        errors.append(
            "valores pendientes (TODO_OWNER/TODO_LINK) en: " + ", ".join(todos)
            + " -> los aporta el dueño (STQ-38) o usa --allow-todo para un borrador"
        )
    return output, errors


def to_seconds(stamp: str) -> int:
    seconds = 0
    for part in stamp.split(":"):
        seconds = seconds * 60 + int(part)
    return seconds


def validate(output: str, data: dict) -> list[str]:
    errors: list[str] = []

    size = len(output.encode("utf-8"))
    if size > MAX_DESCRIPTION_BYTES:
        errors.append(f"la descripcion ocupa {size} bytes (maximo {MAX_DESCRIPTION_BYTES})")
    if "<" in output or ">" in output:
        errors.append("la descripcion contiene '<' o '>' (YouTube los rechaza)")

    title = data.get("titulo")
    if isinstance(title, str) and len(title) > MAX_TITLE_CHARS:
        errors.append(f"el titulo tiene {len(title)} caracteres (maximo {MAX_TITLE_CHARS})")

    hashtags = data.get("hashtags")
    if isinstance(hashtags, list):
        bad = [h for h in hashtags if not (isinstance(h, str) and re.fullmatch(r"#\w+", h))]
        if bad:
            errors.append(f"hashtags invalidos (deben ser '#palabra' sin espacios): {bad}")
        if len(hashtags) > MAX_HASHTAGS:
            errors.append(f"{len(hashtags)} hashtags (YouTube ignora todos si hay mas de {MAX_HASHTAGS})")

    stamps = [m.group(1) for m in CHAPTER.finditer(output)]
    if stamps:
        seconds = [to_seconds(s) for s in stamps]
        if seconds[0] != 0:
            errors.append(f"el primer capitulo debe empezar en 0:00 (empieza en {stamps[0]})")
        if len(stamps) < MIN_CHAPTERS:
            errors.append(f"YouTube exige al menos {MIN_CHAPTERS} capitulos (hay {len(stamps)})")
        for prev, cur, label in zip(seconds, seconds[1:], stamps[1:]):
            if cur - prev < MIN_CHAPTER_GAP_SECONDS:
                errors.append(f"capitulo {label}: debe haber al menos {MIN_CHAPTER_GAP_SECONDS} s desde el anterior y orden creciente")
    return errors


def load_data(paths: list[Path]) -> dict:
    data: dict = {}
    for path in paths:
        with path.open("rb") as handle:
            data.update(tomllib.load(handle))
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--template", required=True, type=Path, help="plantilla .md con placeholders {{clave}}")
    parser.add_argument("--data", required=True, action="append", type=Path,
                        help="TOML de datos; repetible, el ultimo gana (p. ej. enlaces.toml y luego el del video)")
    parser.add_argument("-o", "--output", type=Path, help="archivo de salida (por defecto stdout)")
    parser.add_argument("--allow-todo", action="store_true", help="permite TODO_OWNER/TODO_LINK (solo borradores)")
    args = parser.parse_args(argv)

    try:
        data = load_data(args.data)
        template = load_template(args.template)
    except (OSError, ValueError, tomllib.TOMLDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    output, errors = render(template, data, args.allow_todo)
    errors += validate(output, data)
    if errors:
        print(f"error: no se pudo generar {args.template.name}:", file=sys.stderr)
        for message in errors:
            print(f"  - {message}", file=sys.stderr)
        return 1

    output = output.strip("\n") + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
