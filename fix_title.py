import nbformat, glob, re

heading_re = re.compile(r'^(#{1,6})\s+(.*)$', re.MULTILINE)

for path in glob.glob("*.ipynb"):
    nb = nbformat.read(path, as_version=4)
    for cell in nb.cells:
        if cell.cell_type == "markdown" and cell.source.strip():
            m = heading_re.search(cell.source)
            if m:
                level = len(m.group(1))
                if level > 1:
                    new_line = "# " + m.group(2)
                    cell.source = cell.source[:m.start()] + new_line + cell.source[m.end():]
                    nbformat.write(nb, path)
                    print(f"{path}: promoted {m.group(0)!r} -> {new_line!r}")
                else:
                    print(f"{path}: already H1, no change")
            break  # only look at the first heading in the first markdown cell