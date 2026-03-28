import re
import unicodedata
from lxml import etree as ET
from app.renderers.utils.svg import find_by_id, SVG_NS_URI


def _remove_children(element):
    for child in list(element):
        element.remove(child)


def normalize_text(text: str) -> str:
    """Remove accented characters and normalize text"""
    # NFD decomposition (split accents from base characters)
    nfd = unicodedata.normalize('NFD', text)
    # Filter out combining characters (accents)
    return ''.join(c for c in nfd if unicodedata.category(c) != 'Mn')


def set_text(root, element_id, new_text):
    """Set text while preserving tspan structure and positioning"""
    element = find_by_id(root, element_id)
    
    new_text = str(new_text).strip()
    
    # Find existing tspans
    tspans = element.findall(f"{{{SVG_NS_URI}}}tspan")
    
    if tspans:
        # Update the first tspan's text and keep its positioning
        tspans[0].text = new_text
        
        # Remove any additional tspans
        for tspan in tspans[1:]:
            element.remove(tspan)
    else:
        # No tspans, set directly on element
        element.text = new_text


def extract_surnames(scorers: list) -> list[str]:
    """
    Extract surnames from scorer list.
    Returns only surnames without initials or numbers.
    Handles accented characters.
    """
    surnames = []

    for scorer in scorers:
        name = scorer.get("name", "").strip()
        
        if not name:
            continue
        
        # Remove parenthetical content (like match time)
        name = re.sub(r"\(.*?\)", "", name)
        
        # Try to extract surname from patterns like "D. Ferreyra" or "1. Surname"
        # Match initials followed by surname
        match = re.search(r"^[A-Z]\.\s+(.+)$", name.strip())
        
        if match:
            surname = match.group(1).strip()
        else:
            # Fallback: use the whole name if no pattern matches
            surname = name.strip()
        
        # Normalize accented characters
        surname = normalize_text(surname)
        
        if surname:
            surnames.append(surname)

    return surnames


def get_element_coords(el):
    """Helper to find x, y even if they are on a child tspan (standard for Inkscape)."""
    x = el.get("x")
    y = el.get("y")
    
    # If not on parent, check the first tspan child
    if x is None or y is None:
        # Use universal namespace search for tspan
        tspan = el.find(".//{*}tspan")
        if tspan is not None:
            if x is None: x = tspan.get("x")
            if y is None: y = tspan.get("y")
            
    return (float(x) if x else None, float(y) if y else None)


def set_multiline_text(root, element_id, lines, base_font_size=64, line_spacing=80):
    """
    Set multiline text with precise alignment, accounting for Inkscape transforms.
    """
    el = find_by_id(root, element_id)
    if el is None:
        return

    # Helper to find the "true" absolute coordinates in the template
    def get_absolute_coords(target_el):
        # Start with coordinates from the tag or default to 0
        x = float(target_el.get("x") or 0)
        y = float(target_el.get("y") or 0)
        
        # Inkscape often puts actual coordinates on a child tspan
        tspan = target_el.find(".//{*}tspan")
        if tspan is not None:
            if not target_el.get("x"):
                x = float(tspan.get("x") or 0)
            if not target_el.get("y"):
                y = float(tspan.get("y") or 0)
            
        # ACCOUNT FOR TRANSFORMS: This is likely what is pushing your text too far left
        transform = target_el.get("transform")
        if transform and "translate" in transform:
            try:
                # Extract numbers from translate(x, y) or translate(x y)
                parts = transform.split("(")[1].split(")")[0].replace(",", " ").split()
                x += float(parts[0])
                if len(parts) > 1:
                    y += float(parts[1])
            except (IndexError, ValueError):
                pass
        return x, y

    # Calculate the target position based on the template design
    orig_x, orig_y = get_absolute_coords(el)

    # Determine horizontal alignment (Center X)
    league_map = {"scorers_1": "league1", "scorers_2": "league2"}
    league_id = league_map.get(element_id)
    center_x = orig_x
    
    if league_id:
        league_el = find_by_id(root, league_id)
        if league_el is not None:
            lx, _ = get_absolute_coords(league_el)
            center_x = lx

    # CLEANUP: Remove attributes that cause double-offsets or cropping
    _remove_children(el)
    el.text = None
    el.attrib.pop("x", None)
    el.attrib.pop("y", None)
    el.attrib.pop("transform", None) # Crucial: Remove the transform to use absolute coords
    
    # Remove 'shape-inside' from style (it forces text into a box which causes cropping)
    style = el.get("style", "")
    if "shape-inside" in style:
        style_parts = [s.strip() for s in style.split(";") if "shape-inside" not in s]
        el.set("style", ";".join(style_parts))

    # Apply centering and font-size
    el.set("text-anchor", "middle")
    line_count = len(lines)
    if line_count > 6:
        scaled_font = base_font_size * (6 / line_count)
        el.set("font-size", f"{scaled_font}px")

    # Create new tspans using the calculated absolute coordinates
    for i, line in enumerate(lines):
        tspan = ET.SubElement(el, f"{{{SVG_NS_URI}}}tspan")
        tspan.text = normalize_text(line)
        tspan.set("x", str(center_x))
        tspan.set("y", str(orig_y + (i * line_spacing)))
        tspan.set("text-anchor", "middle")
