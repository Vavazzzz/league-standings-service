import re
from lxml import etree as ET



def extract_surnames(scorers: list) -> list[str]:

    surnames = []

    for scorer in scorers:

        clean = re.sub(r"\(.*?\)", "", scorer["name"]).strip()
        surname = clean.split()[-1]

        surnames.append(surname)

    return surnames


def set_multiline_text(tree, element_id, lines, base_font_size=48):

    el = tree.find(f".//*[@id='{element_id}']")
    if el is None:
        raise ValueError(f"Elemento {element_id} non trovato")

    # pulizia contenuto
    el.text = ""
    for child in list(el):
        el.remove(child)

    # scaling font
    line_count = max(len(lines), 1)

    if line_count > 6:
        font_size = base_font_size * (6 / line_count)
    else:
        font_size = base_font_size

    el.set("font-size", str(font_size))

    # namespace SVG (IMPORTANTISSIMO con lxml)
    nsmap = el.nsmap
    svg_ns = nsmap.get(None)

    for i, line in enumerate(lines):

        tspan = ET.Element(f"{{{svg_ns}}}tspan")

        tspan.text = line

        if i > 0:
            tspan.set("x", el.get("x"))
            tspan.set("dy", "1.2em")

        el.append(tspan)
