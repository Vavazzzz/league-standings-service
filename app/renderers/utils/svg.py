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
    """
    Set logo image. Works with both <image> and <circle> elements.
    For circles, replaces them with embedded image elements.
    """
    element = find_by_id(root, element_id)

    logo_file = Path(logo_path)
    if not logo_file.exists():
        raise FileNotFoundError(f"Logo file not found: {logo_path}")

    # Check if element is a circle or image
    if element.tag.endswith("circle"):
        # Handle circle element
        cx = float(element.get("cx", "0"))
        cy = float(element.get("cy", "0"))
        r = float(element.get("r", "125"))
        
        # Convert circle to image element
        img = Image.open(logo_file)
        img_width, img_height = img.size
        aspect_ratio = img_width / img_height
        
        # Size image to fit in circle
        new_height = r * 2
        new_width = new_height * aspect_ratio
        
        x = cx - (new_width / 2)
        y = cy - (new_height / 2)
        
        # Create image element to replace circle
        image_elem = ET.Element(f"{{{SVG_NS_URI}}}image")
        image_elem.set("id", element.get("id"))
        image_elem.set("x", str(x))
        image_elem.set("y", str(y))
        image_elem.set("width", str(new_width))
        image_elem.set("height", str(new_height))
        image_elem.set("preserveAspectRatio", "xMidYMid slice")
        
        # Embed image as base64
        with open(logo_file, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
        
        data_uri = f"data:image/png;base64,{image_data}"
        image_elem.set(f"{{{XLINK_NS_URI}}}href", data_uri)
        image_elem.set("href", data_uri)
        
        # Replace circle with image in parent
        parent = element.getparent()
        if parent is not None:
            index = list(parent).index(element)
            parent.remove(element)
            parent.insert(index, image_elem)
    else:
        # Handle existing image element
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

        element.set(f"{{{XLINK_NS_URI}}}href", data_uri)
        element.set("href", data_uri)