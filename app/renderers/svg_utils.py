import base64
from pathlib import Path

from PIL import Image
from lxml import etree

XLINK = "http://www.w3.org/1999/xlink"
PLACEHOLDER_HEIGHT = 81.343002
PLACEHOLDER_WIDTH = 67.721581
PLACEHOLDER_X = 103.38165


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

    # Read the PNG and convert to base64 data URI
    logo_file = Path(logo_path)
    if not logo_file.exists():
        raise FileNotFoundError(f"Logo file not found: {logo_path}")
    
    # Get image dimensions to calculate aspect ratio
    img = Image.open(logo_file)
    img_width, img_height = img.size
    aspect_ratio = img_width / img_height
    
    # Set height to match placeholder and calculate width to maintain aspect ratio
    new_height = PLACEHOLDER_HEIGHT
    new_width = new_height * aspect_ratio
    
    # Center the logo horizontally within the placeholder
    x_offset = (PLACEHOLDER_WIDTH - new_width) / 2
    new_x = PLACEHOLDER_X + x_offset
    
    element.set("height", str(new_height))
    element.set("width", str(new_width))
    element.set("x", str(new_x))
    
    with open(logo_file, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    
    data_uri = f"data:image/png;base64,{image_data}"
    element.set("{http://www.w3.org/1999/xlink}href", data_uri)


