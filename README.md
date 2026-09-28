# luce-obj

An original **Luce Base** Wavefront polygon reader. Public export: `obj.Obj`.
`Obj.load(path)` reads a file; `Obj.decode(text)` decodes text. Both return an
immutable `three.PolygonMesh` with shared positions and polygon corners.

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

Regression coverage is currently integrated into sibling `luced-3d`:
`python3 tests/run.py` there builds the Base library through a Luce consumer.
There is no C/C++ parser, foreign SDK or import subprocess.
