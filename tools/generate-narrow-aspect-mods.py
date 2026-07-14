#!/usr/bin/env python3
"""Generate WIP 3:2 and 4:3 candidates from existing 21:9 pchtxt mods.

This is intentionally conservative: it only rewrites obvious AArch64
mov/movk pairs that load the 3440x1440 21:9.5 aspect float (0x4018e38e).
HUD/layout codecaves and resolution edits are left untouched.
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
import zipfile
from dataclasses import dataclass
from pathlib import Path


SOURCE_FLOAT = "0x4018e38e"
TARGETS = {
    "3-2": {
        "label": "3:2",
        "float": "0x3fc00000",
        "note": "1.5, useful for 1440x960 / 1620x1080 style handheld displays",
        "pairs": {
            "w1": ("01008052", "01F8A772"),
            "w8": ("08008052", "08F8A772"),
            "w9": ("09008052", "09F8A772"),
            "w10": ("0A008052", "0AF8A772"),
            "w20": ("14008052", "14F8A772"),
            "w25": ("19008052", "19F8A772"),
            "w30": ("1E008052", "1EF8A772"),
            "x8": ("080080D2", "08F8A7F2"),
            "x9": ("090080D2", "09F8A7F2"),
        },
    },
    "4-3": {
        "label": "4:3",
        "float": "0x3faaaaab",
        "note": "1.3333334, useful for 1440x1080 / 1280x960 style handheld displays",
        "pairs": {
            "w1": ("61559552", "41F5A772"),
            "w8": ("68559552", "48F5A772"),
            "w9": ("69559552", "49F5A772"),
            "w10": ("6A559552", "4AF5A772"),
            "w20": ("74559552", "54F5A772"),
            "w25": ("79559552", "59F5A772"),
            "w30": ("7E559552", "5EF5A772"),
            "x8": ("685595D2", "48F5A7F2"),
            "x9": ("695595D2", "49F5A7F2"),
        },
    },
}

SOURCE_PAIRS = {
    ("C1719C52", "0103A872"): "w1",
    ("C8719C52", "0803A872"): "w8",
    ("C9719C52", "0903A872"): "w9",
    ("CA719C52", "0A03A872"): "w10",
    ("D4719C52", "1403A872"): "w20",
    ("D9719C52", "1903A872"): "w25",
    ("DE719C52", "1E03A872"): "w30",
    ("C8719CD2", "0803A8F2"): "x8",
    ("C9719CD2", "0903A8F2"): "x9",
}

ASPECT_NAME_RE = re.compile(
    r"(21[.\-:]?9|20[.\-:]?9|2580x1080|3440x1440|5160x2160|6880x2880|ultrawide)",
    re.IGNORECASE,
)
SOURCE_RES_RE = re.compile(
    r"(1920x1080|2560x1440|2580x1080|3440x1440|3840x2160|5160x2160|6880x2880)",
    re.IGNORECASE,
)
PATCH_LINE_RE = re.compile(r"^(\s*[0-9A-Fa-f]{8}\s+)([0-9A-Fa-f]{8})(.*)$")


@dataclass
class GeneratedFile:
    game: str
    source_mod: str
    source_path: str
    target: str
    output_path: str
    replacements: int


def iter_text_files(zip_path: Path):
    with zipfile.ZipFile(zip_path) as archive:
        for info in archive.infolist():
            if info.is_dir() or not info.filename.lower().endswith(".pchtxt"):
                continue
            if not ASPECT_NAME_RE.search(info.filename):
                continue
            yield info.filename, archive.read(info).decode("utf-8", "ignore")


def rewrite_patch(text: str, target: str) -> tuple[str, int]:
    lines = text.splitlines()
    replacements = 0
    target_pairs = TARGETS[target]["pairs"]

    i = 0
    while i < len(lines) - 1:
        first = PATCH_LINE_RE.match(lines[i])
        second = PATCH_LINE_RE.match(lines[i + 1])
        if not first or not second:
            i += 1
            continue

        key = (first.group(2).upper(), second.group(2).upper())
        register = SOURCE_PAIRS.get(key)
        if register is None:
            i += 1
            continue

        new_first, new_second = target_pairs[register]
        label = TARGETS[target]["label"]
        lines[i] = f"{first.group(1)}{new_first} // generated {label} aspect low16 for {register}"
        lines[i + 1] = (
            f"{second.group(1)}{new_second} // generated {label} aspect high16 for {register}"
        )
        replacements += 1
        i += 2

    if replacements:
        label = TARGETS[target]["label"]
        text_out = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
        text_out = re.sub(r"21[.:]?9(?:\.5)?", label, text_out, flags=re.IGNORECASE)
        text_out = re.sub(r"3440x1440|2580x1080|5160x2160|6880x2880", label, text_out, flags=re.IGNORECASE)
        text_out = text_out.replace("Ultrawide", f"{label} WIP")
        text_out = text_out.replace("ultrawide", f"{label} WIP")
        banner = (
            f"// WIP generated narrow-aspect candidate: {label} ({TARGETS[target]['float']}).\n"
            f"// Source aspect float was {SOURCE_FLOAT}; HUD/layout fixes may still need game-specific work.\n"
        )
        text_out = text_out.replace("@enabled", banner + "@enabled", 1)
        return text_out, replacements
    return text, 0


def mod_output_name(source_mod: str, target: str) -> str:
    label = TARGETS[target]["label"]
    source_res = SOURCE_RES_RE.search(source_mod)
    source_suffix = f" from {source_res.group(1)}" if source_res else ""
    out = source_mod
    out = re.sub(
        r"(?:1920x1080|2560x1440|2580x1080|3440x1440|3840x2160|5160x2160|6880x2880)"
        r"\s+(?:21[.\-:]?9\s+)?(?:Ultrawide|ultrawide)",
        f"{label} WIP{source_suffix}",
        out,
    )
    out = re.sub(
        r"(?:21[.\-:]?9|20[.\-:]?9)\s+(?:Ultrawide|ultrawide)",
        f"{label} WIP",
        out,
    )
    out = re.sub(r"\b(?:Ultrawide|ultrawide)\b", f"{label} WIP", out)
    if out == source_mod:
        out = f"[{label} WIP] {source_mod}"
    return out


def generate(root: Path, output: Path, clean: bool) -> list[GeneratedFile]:
    if clean and output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    generated: list[GeneratedFile] = []
    for zip_path in sorted(root.glob("*.zip")):
        game = zip_path.stem
        for source_path, text in iter_text_files(zip_path):
            parts = Path(source_path).parts
            if len(parts) < 2:
                continue
            source_mod = parts[0]
            rest = Path(*parts[1:])
            for target in TARGETS:
                rewritten, replacements = rewrite_patch(text, target)
                if not replacements:
                    continue
                out_mod = mod_output_name(source_mod, target)
                out_path = output / game / out_mod / rest
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(rewritten, encoding="utf-8", newline="\n")
                generated.append(
                    GeneratedFile(
                        game=game,
                        source_mod=source_mod,
                        source_path=source_path,
                        target=target,
                        output_path=str(out_path.relative_to(root)),
                        replacements=replacements,
                    )
                )
    return generated


def write_manifest(root: Path, generated: list[GeneratedFile]) -> None:
    manifest = root / "generated-narrow-aspect" / "MANIFEST.csv"
    with manifest.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "game",
                "source_mod",
                "source_path",
                "target",
                "output_path",
                "replacements",
            ],
        )
        writer.writeheader()
        for item in generated:
            writer.writerow(item.__dict__)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path("generated-narrow-aspect"))
    parser.add_argument("--no-clean", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    output = args.output
    if not output.is_absolute():
        output = root / output

    generated = generate(root, output, clean=not args.no_clean)
    write_manifest(root, generated)
    games = {item.game for item in generated}
    print(
        f"Generated {len(generated)} files for {len(games)} games in "
        f"{output.relative_to(root)}"
    )


if __name__ == "__main__":
    main()
