#!/usr/bin/env python3
"""OBJ import benchmark: generates triangle and quad grids (positions only and
with vt/vn), builds bench/main.lucb with --native --release and prints the
fast reader's and the reference decoder's times for each."""
import math
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXE = ".exe" if os.name == "nt" else ""


def grid(path, n, quads, attributes, digits):
    """An n x n point grid of triangles or quads; `digits` 6 writes %.6f, 17 repr."""
    number = (lambda value: "%.6f" % value) if digits == 6 else repr
    with open(path, "w") as out:
        for z in range(n):
            out.write("".join("v %s %s %s\n" % (number(x / (n - 1) - 0.5), number(0.02 * math.sin((x + z) * 0.1)), number(z / (n - 1) - 0.5)) for x in range(n)))
        if attributes:
            for z in range(n):
                out.write("".join("vt %s %s\n" % (number(x / (n - 1)), number(z / (n - 1))) for x in range(n)))
            out.write("vn 0 1 0\n")
        for z in range(n - 1):
            rows = []
            for x in range(n - 1):
                a = z * n + x + 1
                ring = [a, a + n, a + n + 1, a + 1]
                corner = (lambda p: "%d/%d/1" % (p, p)) if attributes else str
                if quads:
                    rows.append("f " + " ".join(corner(p) for p in ring) + "\n")
                else:
                    rows.append("f " + " ".join(corner(p) for p in ring[:3]) + "\n")
                    rows.append("f " + " ".join(corner(p) for p in (ring[0], ring[2], ring[3])) + "\n")
            out.write("".join(rows))


def main():
    base = Path(os.environ.get("LUCE_BASE", ROOT.parent / f"luce-base/build/luce-base{EXE}"))
    with tempfile.TemporaryDirectory(prefix="luce-obj-bench-") as temporary:
        work = Path(temporary)
        files = [(work / "tri400k.obj", 448, False, False, 6), (work / "tri400k_uv_n.obj", 448, False, True, 6),
                 (work / "tri400k_repr.obj", 448, False, False, 17), (work / "quad700k.obj", 838, True, False, 17)]
        for path, n, quads, attributes, digits in files:
            grid(path, n, quads, attributes, digits)
        binary = work / f"bench{EXE}"
        subprocess.run([str(base), "build", str(ROOT / "bench/main.lucb"), "--native", "--release", "-o", str(binary)],
                       check=True, env=dict(os.environ, LUCE_CACHE=str(work / "cache")))
        subprocess.run([str(binary)] + [path.name for path, *_ in files], check=True, cwd=work)


if __name__ == "__main__":
    main()
