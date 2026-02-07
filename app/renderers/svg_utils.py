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


def set_text(tree, element_id: str, value: str):
    el = find_by_id(tree, element_id)
    el.text = str(value)


def set_logo(tree, element_id: str, logo_path: str):
    el = find_by_id(tree, element_id)
    el.attrib[f"{{{XLINK}}}href"] = logo_path
