import base64
from pathlib import Path

from PIL import Image
from lxml import etree as ET

SVG_NS_URI = "http://www.w3.org/2000/svg"
XLINK_NS_URI = "http://www.w3.org/1999/xlink"

SVG_NS = {"svg": SVG_NS_URI}

PLACEHOLDER_HEIGHT = 81.343002
PLACEHOLDER_WIDTH = 67.721581
PLACEHOLDER_X = 103.38165


def load_svg(path):
    parser = ET.XMLParser(remove_blank_text=True)
    tree = ET.parse(path, parser)
    return tree.getroot()


def find_by_id(root, element_id: str):
    result = root.xpath(f".//*[@id='{element_id}']", namespaces=SVG_NS)
    if not result:
        raise ValueError(f"Elemento '{element_id}' non trovato nello SVG")
    return result[0]


def set_logo(root, element_id, logo_path):
    element = find_by_id(root, element_id)

    logo_file = Path(logo_path)
    if not logo_file.exists():
        raise FileNotFoundError(f"Logo file not found: {logo_path}")

    img = Image.open(logo_file)
    img_width, img_height = img.size
    aspect_ratio = img_width / img_height

    new_height = PLACEHOLDER_HEIGHT
    new_width = new_height * aspect_ratio

    x_offset = (PLACEHOLDER_WIDTH - new_width) / 2
    new_x = PLACEHOLDER_X + x_offset

    element.set("height", str(new_height))
    element.set("width", str(new_width))
    element.set("x", str(new_x))

    with open(logo_file, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    data_uri = f"data:image/png;base64,{image_data}"

    # CairoSVG supporta entrambi
    element.set(f"{{{XLINK_NS_URI}}}href", data_uri)
    element.set("href", data_uri)
