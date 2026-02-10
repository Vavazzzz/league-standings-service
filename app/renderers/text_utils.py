import re
from lxml import etree as ET
from app.renderers.svg_utils import find_by_id, SVG_NS_URI


def _remove_children(element):
    for child in list(element):
        element.remove(child)


def set_text(root, element_id, new_text):

    element = find_by_id(root, element_id)

    # NON usare clear()
    _remove_children(element)

    element.text = str(new_text)

    # garantiamo centratura
    element.set("text-anchor", "middle")
    element.set("dominant-baseline", "middle")


def extract_surnames(scorers: list) -> list[str]:

    surnames = []

    for scorer in scorers:

        name = scorer["name"]

        name = re.sub(r"\(.*?\)", "", name)

        match = re.search(r"\d+(?:\+\d+)?\.\s*(.+)", name)

        if match:
            surname = match.group(1)
            surname = re.split(r"[,;]", surname)[0]
            surname = surname.strip()
        else:
            surname = name.strip()

        surnames.append(surname)

    return surnames


def set_multiline_text(root, element_id, lines, base_font_size=48):

    el = find_by_id(root, element_id)

    x = el.get("x")
    y = el.get("y")
    text_anchor = el.get("text-anchor", "middle")

    _remove_children(el)

    line_count = max(len(lines), 1)

    if line_count > 6:
        font_size = base_font_size * (6 / line_count)
    else:
        font_size = base_font_size

    el.set("font-size", str(font_size))
    el.set("text-anchor", text_anchor)

    for i, line in enumerate(lines):

        tspan = ET.Element(f"{{{SVG_NS_URI}}}tspan")
        tspan.text = line
        tspan.set("x", x)

        if i == 0:
            tspan.set("dy", "0")
        else:
            tspan.set("dy", "1.2em")

        el.append(tspan)
