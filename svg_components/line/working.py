
def describe():
    """
    Describe the component.
    """
    return {
        "name": "line",
        "description": "A simple line with a start and end point.",
        "inputs": {
            "p1": {"type": "list", "description": "Start point [x, y]."},
            "p2": {"type": "list", "description": "End point [x, y]."},
            "pos": {"type": "list", "description": "Position offset for the line."},
            "color": {"type": "string", "description": "Stroke color for the line."},
            "stroke_width": {"type": "number", "description": "Stroke width."}
        }
    }

def define():
    """
    Define the component's shape and properties.
    """
    return {
        "shape_name": "line",
        "shape_aliases": [],
    }

def action(**kwargs):
    """
    Generate the SVG for the line.
    """
    p3 = kwargs
    p1 = p3.get("p1", [0, 0])
    p2 = p3.get("p2", [10, 10])
    
    shape_dict = {
        "shape": "line",
        "p1": p1,
        "p2": p2,
        "pos": p3.get("pos", [0, 0, 0]),
        "stroke": p3.get("color", "black"),
        "stroke_width": p3.get("stroke_width", 1)
    }

    return [shape_dict]
