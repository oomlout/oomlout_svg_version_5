
import math

def describe():
    """
    Describe the component.
    """
    return {
        "name": "circle_slice",
        "description": "A slice of a circle, can be an arc or a pie slice.",
        "inputs": {
            "r": {"type": "number", "description": "Radius of the circle."},
            "start_angle": {"type": "number", "description": "Start angle in degrees."},
            "end_angle": {"type": "number", "description": "End angle in degrees."},
            "slice_type": {"type": "string", "description": "'pie' for a closed slice, 'arc' for just the line.", "default": "pie"},
            "pos": {"type": "list", "description": "Position of the center of the circle."},
            "color": {"type": "string", "description": "Fill color for 'pie', stroke color for 'arc'."},
            "stroke": {"type": "string", "description": "Stroke color."},
            "stroke_width": {"type": "number", "description": "Stroke width."}
        }
    }

def define():
    """
    Define the component's shape and properties.
    """
    return {
        "shape_name": "circle_slice",
        "shape_aliases": ["arc_slice", "pie_slice"],
    }

def action(**kwargs):
    """
    Generate the SVG path for the circle slice.
    """
    p3 = kwargs
    r = p3.get("r", 10)
    start_angle_deg = p3.get("start_angle", 0)
    end_angle_deg = p3.get("end_angle", 90)
    slice_type = p3.get("slice_type", "pie")
    
    # Convert angles to radians for math functions
    start_angle_rad = math.radians(start_angle_deg)
    end_angle_rad = math.radians(end_angle_deg)

    # Calculate start and end points
    start_x = r * math.cos(start_angle_rad)
    start_y = r * math.sin(start_angle_rad)
    end_x = r * math.cos(end_angle_rad)
    end_y = r * math.sin(end_angle_rad)

    # Determine large arc flag
    angle_diff = end_angle_deg - start_angle_deg
    if angle_diff < 0:
        angle_diff += 360
    large_arc_flag = 1 if angle_diff > 180 else 0

    # Construct the path data
    path_data = f"M {start_x} {start_y} A {r} {r} 0 {large_arc_flag} 1 {end_x} {end_y}"

    if slice_type == "pie":
        path_data += " L 0 0 Z"
        shape_dict = {
            "shape": "path",
            "d": path_data,
            "pos": p3.get("pos", [0, 0, 0]),
            "color": p3.get("color", "black"),
            "stroke": p3.get("stroke", "none"),
            "stroke_width": p3.get("stroke_width", 0)
        }
    else: # arc
        shape_dict = {
            "shape": "path",
            "d": path_data,
            "pos": p3.get("pos", [0, 0, 0]),
            "color": "none", # Arcs have no fill
            "stroke": p3.get("color", p3.get("stroke", "black")), # Use color as stroke for arc
            "stroke_width": p3.get("stroke_width", 1)
        }

    return [shape_dict]
