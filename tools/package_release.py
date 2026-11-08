"""Build the complete download and the smaller original-building download."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "local_releases"
EXCLUDED = {".git", ".pio", "tmp", "local_releases", "__pycache__", "archive", "historical"}


def write_archive(target, members):
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED, compresslevel=4) as archive:
        for path, name in members:
            with path.open("rb") as source:
                if source.read(42).startswith(b"version https://git-lfs.github.com/spec/"):
                    raise ValueError(f"Run git lfs pull before packaging {path.name}")
            archive.write(path, name)
    with zipfile.ZipFile(target) as archive:
        damaged = archive.testzip()
        if damaged:
            raise ValueError(f"ZIP integrity failure in {damaged}")


def main():
    OUTPUT.mkdir(exist_ok=True)
    complete = OUTPUT / "SOLARSKIN_ESSENTIAL.zip"
    files = sorted(p for p in ROOT.rglob("*") if p.is_file()
                   and not EXCLUDED.intersection(p.relative_to(ROOT).parts)
                   and p.name not in {"solarskin_config.h", "secrets.h", ".env"})
    write_archive(complete, [(p, "SolarSkin/" + p.relative_to(ROOT).as_posix()) for p in files])

    original = OUTPUT / "SOLARSKIN_ORIGINAL_OFFICE_20.zip"
    building = ROOT / "cad/original_20_module_building"
    members = [(building / name, name) for name in
               ("COMPLETE_BUILDING_20.blend", "COMPLETE_BUILDING_R6.FCStd")]
    members += [(ROOT / "LICENSE_STATUS.md", "LICENSE_STATUS.md"),
                (building / "OPEN_FIRST.txt", "OPEN_FIRST.txt")]
    write_archive(original, members)

    records = []
    for path in [complete, original, *sorted((ROOT / "docs/pdf").glob("*.pdf"))]:
        with path.open("rb") as source:
            digest = hashlib.file_digest(source, "sha256").hexdigest()
        records.append(dict(file=path.name, bytes=path.stat().st_size, sha256=digest))
    (OUTPUT / "SHA256SUMS.txt").write_text("".join(
        f"{row['sha256']}  {row['file']}\n" for row in records))
    (OUTPUT / "release_assets.json").write_text(json.dumps(records, indent=2) + "\n")


if __name__ == "__main__":
    main()
