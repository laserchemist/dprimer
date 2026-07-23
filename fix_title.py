import nbformat
import glob
import re

heading_pattern = re.compile(r'^#{1,2}\s+(.+?)\s*$')

for path in glob.glob("*.ipynb"):
    nb = nbformat.read(path, as_version=4)
    changed = False

    # Try to find a frontmatter title in the first cell (raw YAML block)
    fm_title = None
    if nb.cells and nb.cells[0].cell_type == "raw":
        m = re.search(r'title:\s*(.+)', nb.cells[0].source)
        if m:
            fm_title = m.group(1).strip()

    seen_title = None
    for cell in nb.cells:
        if cell.cell_type != "markdown":
            continue
        lines = cell.source.splitlines()
        new_lines = []
        for line in lines:
            m = heading_pattern.match(line)
            if m:
                heading_text = m.group(1).strip()
                # Drop it if it matches frontmatter title, or if we've
                # already seen this exact heading once before in the notebook
                if (fm_title and heading_text == fm_title) or heading_text == seen_title:
                    changed = True
                    continue
                if seen_title is None:
                    seen_title = heading_text
            new_lines.append(line)
        new_source = "\n".join(new_lines)
        if new_source != cell.source:
            cell.source = new_source

    if changed:
        nbformat.write(nb, path)
        print(f"Fixed: {path}")
    else:
        print(f"No change: {path}")
