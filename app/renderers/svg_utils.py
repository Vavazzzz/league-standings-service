from pathlib import Path

from lxml import etree


XLINK = "http://www.w3.org/1999/xlink"


def load_svg(path: str):
    parser = etree.XMLParser(remove_blank_text=True)
    return etree.parse(path, parser)


def find_by_id(tree, element_id: str):
    result = tree.xpath(f"//*[@id='{element_id}']")
    if not result:
        raise ValueError(f"Elemento '{element_id}' non trovato nello SVG")
    return result[0]


def set_text(tree, element_id, new_text):
    element = tree.find(f".//*[@id='{element_id}']")

    if element is None:
        raise ValueError(f"Elemento {element_id} non trovato")

    # Rimuove eventuali tspan figli
    for child in list(element):
        element.remove(child)

    element.text = str(new_text)



def set_logo(tree, element_id, logo_path):
    element = tree.find(f".//*[@id='{element_id}']")

    if element is None:
        raise ValueError(f"Elemento {element_id} non trovato")

    element.set(
        "{http://www.w3.org/1999/xlink}href",
        Path(logo_path).resolve().as_uri()
    )


