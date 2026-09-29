# luce-obj

An original **Luce Base** Wavefront polygon reader and writer. Public export:
`obj.Obj`. `Obj.load(path)` reads a file; `Obj.decode(text)` decodes text. Both
return an immutable luce-geocore `Mesh` with shared positions and polygon corners.

The reader scans the file bytes in place, in chunks split at line boundaries
and parsed on luce-geocore's thread pool: a counting pass sizes every array,
a parsing pass writes points, faces, corners and the `vt`/`vn` tables straight
into them, and corner UVs and normals are gathered by index. Numbers take
Clinger's fast path or Eisel-Lemire, bit-identical to `strings.parse_f64`.
A 400k-triangle, 14 MB file loads in under 20 ms on an M-series Mac, the
geocore Mesh build included. `Obj.decode_reference(text)` is the original
single-pass decoder: the reader must match it exactly, and hands it any text
it cannot take, so errors are reported with its wording and order.

`Obj.write(path, mesh, attributes=true)` writes a mesh, replacing the file
atomically; `Obj.encode(mesh, attributes=true)` returns the text. Points become
`v` lines with 17 significant digits, so binary64 positions round-trip exactly.
With `attributes`, corner-domain `uv` and `N` become one `vt` and one `vn` per
corner. Each polygon becomes one `f` line with 1-based indices (`p`, `p/t`,
`p//n` or `p/t/n`). Other attributes, groups and materials are not written.

Supports `v`, `vt`, `vn`, polygon `f`, positive/negative indices, `v/vt/vn` and
`v//vn`. UVs and normals become corner-domain `uv` and `N` attributes. Optional
homogeneous position weights are applied. Point-only files are supported.
Object/group/smoothing/material declarations are accepted but not represented;
MTL files and texture paths are never opened. Curves, freeform surfaces, vertex
color extensions and line continuations are not supported.

Limits: 1 GiB input, 8,388,608 points/faces, 33,554,432 corners or UV/normal
records, 256 corners per face. A preflight sizes all attribute buffers before
decoding. Input is still read in full; these are safety budgets, not a promise
that every device has enough memory. The 4.17M- and 5.58M-triangle Desktop car
fixtures have completed production-importer tests.
Malformed indices, degenerate polygons and unsupported geometry records fail
explicitly. Import preserves source coordinates and units.

`./test.sh` runs the Luce regressions in `tests/` native and through the C
backend: indices, UVs, normals, the 65,536-corner regression, write/read
round trips, and the reader against the reference decoder (number spellings,
n-gons, CRLF, negative and partial references, many-chunk files, malformed
text). `python3 bench/run.py` times both on generated 400k- and 700k-face grids. CI pins the compilers and sibling packages in `bootstrap/PACKAGES`.
There is no C/C++ parser, foreign SDK or import subprocess.
