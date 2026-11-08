"""Rebuild the generic 3MF beds listed in docs/13_print_beds.md."""
from pathlib import Path
import csv
import re
import struct
from xml.etree import ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CORE = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
TYPES = """<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>"""
RELS = """<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="r0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>"""


def mesh(resource, number, name, path):
    data = path.read_bytes()
    count = struct.unpack_from("<I", data, 80)[0]
    triangles = np.ndarray((count, 3, 3), "<f4", data, 96, (50, 12, 4))
    points, indices = np.unique(triangles.reshape(-1, 3), axis=0, return_inverse=True)
    obj = ET.SubElement(resource, "object", id=str(number), type="model", name=name)
    geometry = ET.SubElement(obj, "mesh")
    vertices = ET.SubElement(geometry, "vertices")
    for point in points:
        ET.SubElement(vertices, "vertex", dict(zip("xyz", map(str, point))))
    faces = ET.SubElement(geometry, "triangles")
    for triangle in indices.reshape(-1, 3):
        ET.SubElement(faces, "triangle", dict(zip(("v1", "v2", "v3"), map(str, triangle))))
    return points.min(axis=0), points.max(axis=0)


def main():
    directory = ROOT / "print/09_one_module_plates"
    directory.mkdir(exist_ok=True)
    with (ROOT / "bom/mechanism.csv").open() as f:
        parts = {row["part_id"].split("_")[0]: row for row in csv.DictReader(f)}
    quantities = {name: 0 for name in parts}
    for section in (ROOT / "docs/13_print_beds.md").read_text().split("### ")[1:]:
        label = section.splitlines()[0]
        model = ET.Element("model", xmlns=CORE, unit="millimeter")
        resources = ET.SubElement(model, "resources")
        build = ET.SubElement(model, "build")
        objects = {}
        boxes = []
        for name, x, y in re.findall(r"^\| ([PE]\w+) \| ([\d.]+) \| ([\d.]+) \|", section, re.M):
            if name not in objects:
                number = len(objects) + 1
                low, high = mesh(resources, number, name, ROOT / parts[name]["file"])
                objects[name] = number, low, high
            number, low, high = objects[name]
            x, y = float(x), float(y)
            width, depth, height = high - low
            assert x + width <= 246.02 and y + depth <= 246.02 and height <= 256
            assert all(x + width < a or y + depth < b or x > c or y > d for a,b,c,d in boxes)
            boxes.append((x, y, x + width, y + depth))
            transform = f"1 0 0 0 1 0 0 0 1 {x-low[0]:.6f} {y-low[1]:.6f} {-low[2]:.6f}"
            ET.SubElement(build, "item", objectid=str(number), transform=transform)
            quantities[name] += 1
        filename = label.lower().replace(" - ", "_").replace(" ", "_") + ".3mf"
        with ZipFile(directory / filename, "w", ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml", TYPES)
            z.writestr("_rels/.rels", RELS)
            z.writestr("3D/3dmodel.model", ET.tostring(model, encoding="utf-8", xml_declaration=True))
        print(filename, len(build))
    assert all(quantities[n] == int(p["per_module"]) for n,p in parts.items())


if __name__ == "__main__":
    main()
