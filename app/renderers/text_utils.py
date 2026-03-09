import re
import unicodedata
from lxml import etree as ET
from app.renderers.svg_utils import find_by_id, SVG_NS_URI


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


def set_multiline_text(root, element_id, lines, base_font_size=64):
    """
    Set multiline text aligned with corresponding league element.
    """
    el = find_by_id(root, element_id)

    # Normalize all lines with unaccented characters
    lines = [normalize_text(line) for line in lines]
    
    # Map scorers to their corresponding league elements for alignment
    alignment_map = {
        "scorers_1": "league1",
        "scorers_2": "league2"
    }
    
    league_id = alignment_map.get(element_id)
    league_x = None
    league_y = None
    
    if league_id:
        try:
            league_el = find_by_id(root, league_id)
            league_tspan = league_el.find(f"{{{SVG_NS_URI}}}tspan")
            if league_tspan is not None:
                league_x = float(league_tspan.get("x", "0"))
                league_y = float(league_tspan.get("y", "0"))
        except ValueError:
            pass
    
    # Get original tspans to preserve y positioning
    original_tspans = el.findall(f"{{{SVG_NS_URI}}}tspan")
    
    if not original_tspans:
        # Fallback: create new tspans from scratch
        x = el.get("x", "0") if league_x is None else str(league_x)
        y = el.get("y", "0") if league_y is None else str(league_y)
        
        _remove_children(el)
        el.set("text-anchor", "middle")
        
        for i, line in enumerate(lines):
            tspan = ET.Element(f"{{{SVG_NS_URI}}}tspan")
            tspan.text = line
            tspan.set("x", str(x))
            tspan.set("y", str(float(y) + (i * 80)))
            el.append(tspan)
        return
    
    # Get y positioning from first original tspan
    first_tspan = original_tspans[0]
    base_y = float(first_tspan.get("y", "0"))
    
    # Use league1/league2 x-coordinate if found, otherwise use element's x
    if league_x is not None:
        center_x = league_x
    else:
        center_x = el.get("x", "0")
    
    # Set center alignment
    el.set("text-anchor", "middle")
    
    # Adjust font size if there are many lines
    line_count = len(lines)
    font_size = base_font_size
    
    if line_count > 6:
        font_size = base_font_size * (6 / line_count)
        el.set("font-size", str(font_size))
    
    # Clear old tspans
    _remove_children(el)
    
    # Create new tspans with center x and absolute y positioning
    line_spacing = 80  # pixels between lines
    
    for i, line in enumerate(lines):
        tspan = ET.Element(f"{{{SVG_NS_URI}}}tspan")
        tspan.text = line
        tspan.set("x", str(center_x))
        tspan.set("y", str(base_y + (i * line_spacing)))
        el.append(tspan)
    """
    Set multiline text with center alignment.
    Preserves original y positioning and uses element's x for center alignment.
    """
    el = find_by_id(root, element_id)

    # Normalize all lines with unaccented characters
    lines = [normalize_text(line) for line in lines]
    
    # Get original tspans to preserve y positioning
    original_tspans = el.findall(f"{{{SVG_NS_URI}}}tspan")
    
    # Use the element's x coordinate for center alignment (not the tspan's x)
    center_x = el.get("x", "0")
    
    if not original_tspans:
        # Fallback: create new tspans from scratch
        y = el.get("y", "0")
        
        _remove_children(el)
        el.set("text-anchor", "middle")
        
        for i, line in enumerate(lines):
            tspan = ET.Element(f"{{{SVG_NS_URI}}}tspan")
            tspan.text = line
            tspan.set("x", str(center_x))
            tspan.set("y", str(float(y) + (i * 80)))
            el.append(tspan)
        return
    
    # Get y positioning from first original tspan
    first_tspan = original_tspans[0]
    base_y = float(first_tspan.get("y", "0"))
    
    # Set center alignment
    el.set("text-anchor", "middle")
    
    # Adjust font size if there are many lines
    line_count = len(lines)
    font_size = base_font_size
    
    if line_count > 6:
        font_size = base_font_size * (6 / line_count)
        el.set("font-size", str(font_size))
    
    # Clear old tspans
    _remove_children(el)
    
    # Create new tspans with center x and absolute y positioning
    line_spacing = 80  # pixels between lines
    
    for i, line in enumerate(lines):
        tspan = ET.Element(f"{{{SVG_NS_URI}}}tspan")
        tspan.text = line
        tspan.set("x", str(center_x))  # Use element's x for center alignment
        tspan.set("y", str(base_y + (i * line_spacing)))
        el.append(tspan)