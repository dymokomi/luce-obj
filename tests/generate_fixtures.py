"""Generated OBJ fixtures, written into the test run's scratch fixtures directory."""


def write_fixtures(directory):
    # Regression for the historical 65,536-corner OBJ buffer overrun.
    (directory / "large.obj").write_text(
        "v 0 0 0\nv 1 0 0\nv 0 1 0\nvt 0 0\nvn 0 0 1\n" +
        "f 1/1/1 2/1/1 3/1/1\n" * 22000)
