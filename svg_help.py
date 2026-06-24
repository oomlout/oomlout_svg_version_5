import copy
import os
import sys
import yaml

import opsvg
import svg_variables as _sv
import svg_styles as _ss
import svg_a4


###### utilities


def get_typ(**kwargs):
    typ = kwargs.get("typ", "")

    if typ == "":
        #setup
        #typ = "all"
        typ = "fast"
        #typ = "manual"

    return typ


def get_build_variables(typ, filter=""):
    if typ == "all":
        return {
            "filter": "",
            "save_type": "all",
            "navigation": True,
            "overwrite": True,
        }

    if typ == "fast":
        return {
            "filter": "",
            "save_type": "all",
            "navigation": False,
            "overwrite": True,
        }

    if typ == "manual":
        return {
            "filter": "",
            #"filter": "label"
            "save_type": "none",
            #"save_type": "all"
            "navigation": True,
            #"navigation": False
            "overwrite": True,
        }

    raise ValueError(f"Unknown typ: {typ}")


def get_navigation_sort(oobb_style=False):
    sort = []
    #sort.append("extra")
    sort.append("oobb_name")
    sort.append("width")
    sort.append("height")
    return sort


def prepare_base_for_print(thing, pos, **kwargs):
    # SVG is a flat 2-D format — there is no Z axis to flip for printing.
    # This stub exists so builder functions that call it remain compatible
    # with the working_scad.py pattern.
    pass


def make_parts(**kwargs):
    parts          = kwargs.get("parts", [])
    filter         = kwargs.get("filter", "")

    #make the parts
    if True:
        for part in parts:
            oobb_name = part.get("oobb_name", "default")
            extra = part["kwargs"].get("extra", "")
            if filter in oobb_name or filter in extra:
                print(f"making {part['oobb_name']}")
                make_svg_generic(part)
            else:
                print(f"skipping {part['oobb_name']}")


def make_svg_generic(part):
    # Keys in an svg_details entry that control pipeline meta / routing,
    # not layout data — they are NOT merged into kwargs for the builder.
    _SVG_DETAILS_META = {
        "svg_name", "filename_extra",
        "width", "height", "depth", "extra", "radius_name",
    }

    oobb_name    = part.get("oobb_name", "default")
    project_name = part.get("project_name", "default")

    # kwargs_base is the live part["kwargs"] reference so that oomp_description_*
    # written below survive into the working.yaml write-back.
    kwargs_base              = part.get("kwargs", {})
    save_type                = kwargs_base.get("save_type", "all")
    overwrite                = kwargs_base.get("overwrite",  True)
    kwargs_base["type"]      = f"{project_name}_{oobb_name}"

    # Build a scratch thing (no svg_details layout keys) to drive oomp_id.
    thing_base = get_default_thing(**kwargs_base)
    thing_base.update(part)

    # oomp_mode — writes back to kwargs_base so values round-trip through YAML.
    oomp_mode = kwargs_base.get("oomp_mode", "project")
    if oomp_mode == "project":
        current_size  = thing_base.get("size", "default")
        new_size      = current_size.replace(f"{project_name}_", "")
        kwargs_base["oomp_description_main"]  = f"{new_size}_{thing_base.get('description_main', 'default')}"
        kwargs_base["oomp_description_extra"] = thing_base.get("description_extra", "")
    elif oomp_mode == "oobb":
        descextra = thing_base.get("extra", "")
        if descextra:
            descextra = f"{descextra}_extra"
        kwargs_base["oomp_description_main"]  = thing_base.get("description_main", "default")
        kwargs_base["oomp_description_extra"] = descextra
        kwargs_base["oomp_size"]              = part["oobb_name"]

    # Build oomp_id / folder (once, independent of svg_details entries).
    oomp_id = part.get("id", "")
    if not oomp_id:
        for key in ["classification", "type", "size", "color", "description_main", "description_extra"]:
            deet = part.get(key, "").replace(".", "_")
            if deet:
                oomp_id += f"{deet}_"
        oomp_id = oomp_id.rstrip("_")
    if not oomp_id:
        oomp_id = oobb_name
    part["id"] = oomp_id
    folder = f"parts/{oomp_id}"

    if save_type != "all":
        print(f"  dry-run — would write to {folder}/")
        return thing_base

    if not os.path.isdir(folder):
        os.makedirs(folder)

    # Normalise svg_details → list so we can loop over it uniformly.
    # A single dict is treated as a one-element list.
    raw_svg_details = part.get("svg_details", {})
    svg_details_list = raw_svg_details if isinstance(raw_svg_details, list) else [raw_svg_details]

    # Collect all layout keys used across every svg_details entry (for write-back cleanup).
    all_svg_detail_layout_keys = set()
    for sd in svg_details_list:
        all_svg_detail_layout_keys.update(k for k in sd if k not in _SVG_DETAILS_META)

    import working_svg
    last_thing = thing_base

    for svg_detail in svg_details_list:
        # Per-entry kwargs: start from base, merge this entry's layout keys.
        kwargs = copy.deepcopy(kwargs_base)
        for k, v in svg_detail.items():
            if k not in _SVG_DETAILS_META:
                kwargs.setdefault(k, v)

        thing = get_default_thing(**kwargs)
        thing.update(part)

        svg_name = svg_detail.get("svg_name", oobb_name)
        func = getattr(working_svg, f"get_{svg_name}", None)
        if callable(func):
            func(thing, **kwargs)
        else:
            working_svg.get_base(thing, **kwargs)

        filename_extra = svg_detail.get("filename_extra", "")
        suffix         = f"_{filename_extra}" if filename_extra else ""

        svg_path = os.path.join(folder, f"working_svg{suffix}.svg")
        opsvg.opsvg_make_object(svg_path, thing["svg_components"], overwrite=overwrite)
        svg_a4.make_a4_sheet(svg_path, folder, part, thing, filename_extra=filename_extra)

        last_thing = thing

    # working.yaml — partial dump
    yaml_file = f"{folder}/working.yaml"
    with open(yaml_file, "w", encoding="utf-8") as file:
        part_new    = copy.deepcopy(part)
        kwargs_new  = part_new.get("kwargs", {})
        kwargs_new.pop("save_type", "")
        # Strip all svg_details keys (both meta and layout) so they don't
        # duplicate in kwargs — they live exclusively in svg_details.
        for k in all_svg_detail_layout_keys | _SVG_DETAILS_META:
            kwargs_new.pop(k, None)
        part_new["kwargs"]      = kwargs_new
        part_new["project_name"] = os.getcwd()
        part_new["id_svg"]      = last_thing.get("id", oomp_id)
        # Preserve svg_details exactly as loaded (list or dict).
        part_new["svg_details"] = copy.deepcopy(part.get("svg_details", {}))
        part_new.pop("thing", "")
        yaml.dump(part_new, file, allow_unicode=True)

    # thing.yaml — full dump
    yaml_file = f"{folder}/thing.yaml"
    with open(yaml_file, "w", encoding="utf-8") as file:
        part_new    = copy.deepcopy(part)
        kwargs_new  = part_new.get("kwargs", {})
        kwargs_new.pop("save_type", "")
        part_new["kwargs"]       = kwargs_new
        part_new["project_name"] = os.getcwd()
        part_new["id_svg"]       = last_thing.get("id", oomp_id)
        part_new["thing"]        = _serialisable(last_thing)
        yaml.dump(part_new, file, allow_unicode=True)

    print(f"done {oomp_id}")
    return last_thing


def generate_navigation(folder="parts", sort=["oobb_name", "width", "height"]):
    #crawl through all directories in parts/ and load all working.yaml files
    parts = {}
    for root, dirs, files in os.walk(folder):
        if "working.yaml" in files:
            yaml_file = os.path.join(root, "working.yaml")
            if root != folder:
                with open(yaml_file, "r", encoding="utf-8") as file:
                    part = yaml.safe_load(file)
                    part["folder"] = root
                    part_name = root.replace(f"{folder}", "")
                    part_name = part_name.replace("/", "").replace("\\", "")
                    parts[part_name] = part
                    print(f"Loaded {yaml_file}")

    for part_id in parts:
        if part_id != "":
            part = parts[part_id]

            if "kwargs" in part:
                kwarg_copy = copy.deepcopy(part["kwargs"])
                folder_navigation = "navigation_svg"
                folder_source = part["folder"]
                folder_extra = ""
                for s in sort:
                    if s == "oobb_name":
                        ex = part.get("oobb_name", "default")
                    else:
                        ex = kwarg_copy.get(s, "default")
                        if isinstance(ex, list):
                            ex_string = ""
                            for e in ex:
                                ex_string += f"{e}_"
                            ex = ex_string[:-1]
                            ex = ex.replace(".", "d")
                    folder_extra += f"{s}_{ex}/"

                folder_extra = folder_extra.replace(".", "d")
                folder_destination = f"{folder_navigation}/{folder_extra}"
                if not os.path.exists(folder_destination):
                    os.makedirs(folder_destination)
                if os.name == "nt":
                    command = f'xcopy "{folder_source}" "{folder_destination}" /E /I /Y'
                    print(command)
                    os.system(command)
                else:
                    os.system(f"cp -r {folder_source}/. {folder_destination}")


def get_default_thing(**kwargs):
    # Resolve stylesheet: kwargs may carry "stylesheet" name or a full "styles" dict
    sheet_name = kwargs.get("stylesheet", "default")
    styles     = kwargs.get("styles", None)
    if styles is None:
        styles = _ss.get_stylesheet(sheet_name)
    else:
        styles = copy.deepcopy(styles)

    # Apply any per-part style overrides passed as part_styles
    part_styles = kwargs.get("part_styles", {})
    if part_styles:
        styles = _ss.merge(styles, part_styles)

    thing = {
        "oobb_name":         kwargs.get("oobb_name",         ""),
        "type":              kwargs.get("type",              ""),
        "description":       kwargs.get("description",       ""),
        "classification":    kwargs.get("classification",    "svg"),
        "size":              kwargs.get("size",              ""),
        "color":             kwargs.get("color",             ""),
        "description_main":  kwargs.get("description_main",  ""),
        "description_extra": kwargs.get("description_extra", ""),
        "width":             kwargs.get("width",  1),
        "height":            kwargs.get("height", 1),
        "depth":             kwargs.get("depth",  3),
        "extra":             kwargs.get("extra",  ""),
        "width_mm":          (kwargs.get("width",  1) if isinstance(kwargs.get("width",  1), (int, float)) else 1) * _sv.OSP - _sv.OSP_MINUS,
        "height_mm":         (kwargs.get("height", 1) if isinstance(kwargs.get("height", 1), (int, float)) else 1) * _sv.OSP - _sv.OSP_MINUS,
        "depth_mm":          kwargs.get("depth",  3),
        "svg_components":    [],
        "styles":            styles,
    }
    return thing


def id_from_part(part):
    oomp_keys = ["classification", "type", "size", "color", "description_main", "description_extra"]
    oomp_id = part.get("id", "")
    if not oomp_id:
        for key in oomp_keys:
            val = str(part.get(key, "")).replace(".", "_").strip()
            if val:
                oomp_id += f"{val}_"
        oomp_id = oomp_id.rstrip("_")
    if not oomp_id:
        oomp_id = part.get("oobb_name", "unnamed")
    return oomp_id


def _serialisable(obj, _depth=0):
    if _depth > 10:
        return str(obj)
    if isinstance(obj, dict):
        return {k: _serialisable(v, _depth + 1) for k, v in obj.items()
                if not callable(v)}
    if isinstance(obj, (list, tuple)):
        return [_serialisable(i, _depth + 1) for i in obj]
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    return str(obj)


def _split_title(title):
    """Split a title string into two display lines for the fill-in-the-blanks card.

    Splits on the first '\\n' if present, otherwise at the space closest to the
    midpoint.  Returns (line1, line2) — line2 is empty if the title is a single word.
    """
    if "\n" in title:
        parts = title.split("\n", 1)
        return parts[0].strip(), parts[1].strip()
    words = title.split()
    if len(words) <= 1:
        return title, ""
    mid = len(words) // 2
    return " ".join(words[:mid]), " ".join(words[mid:])


def get_fill_in_the_blanks(thing, **kwargs):
    """100 × 159 mm fill-in card — Project Bolt tin label style.

    Layout
    ------
    ┌─────────────────────────────────────────┐  ← single thick outer border (r=8)
    │                                         │
    │              Prototyping                │  ← title line 1 (bold)
    │                  Tin                    │  ← title line 2 (bold)
    │                                         │
    │  _______________________________________│  ← 4 ruled blank lines
    │  _______________________________________│
    │  _______________________________________│
    │  _______________________________________│
    │                                         │
    ├────────────────────────┬────────────────┤  ← table row 1 (edge to edge)
    │  (category / label)    │    Contents    │     2 cols: light | dark
    ├─────────┬──────────────┼────────────────┤  ← table rows 2-3 (edge to edge)
    │         │              │                │     3 equal cols
    ├─────────┼──────────────┼────────────────┤
    │         │              │                │
    └─────────┴──────────────┴────────────────┘

    Parameters (all optional kwargs)
    ----------------------------------
    title         : str   — card title, split to 2 lines automatically
                           (default "Prototyping Tin")
    table_label   : str   — text in the dark right-hand header cell
                           (default "Contents")
    title_size    : float — font size for the title in mm (default 14.0)
    num_lines     : int   — number of ruled blank lines (default 4)
        stylesheet    : str | list[str]
                                                 — stylesheet name or merge list applied to the part
                                                     before any local overrides (default "project_bolt")
        styles        : dict  — per-part named style overrides such as plate,
                                                     header, or label.title; merged on top of the
                                                     resolved stylesheet before rendering
    """
    prepare_print  = kwargs.get("prepare_print", False)
    pos            = kwargs.get("pos", [0, 0, 0])
    title          = kwargs.get("title", "Prototyping Tin")
    table_label    = kwargs.get("table_label", "Contents")
    title_size     = kwargs.get("title_size", 14.0)
    num_lines      = kwargs.get("num_lines", 4)

    # ── Stylesheet ────────────────────────────────────────────────────────────
    if "styles" not in thing or not thing.get("styles"):
        sheet_name = kwargs.get("stylesheet", "project_bolt")
        thing["styles"] = _ss.get_stylesheet(sheet_name)

    # ── Card geometry ─────────────────────────────────────────────────────────
    card_w  = 100.0
    card_h  = 159.0
    r_outer = 8.0    # corner radius

    # ── Card fill only (border is drawn last so it sits on top) ──────────────
    pos1 = copy.deepcopy(pos)
    opsvg.se(thing, shape="rounded_rectangle", style="plate",
             size=[card_w, card_h, 0], r=r_outer, pos=pos1,
             stroke="none", stroke_width=0)

    # ── Title (1 or 2 lines, bold display font) ───────────────────────────────
    line1, line2 = _split_title(title)
    line_spacing = title_size * 1.25   # comfortable inter-line gap

    if line2:
        # Two-line: centre the pair vertically in the title zone
        title1_y = 61.0
        title2_y = title1_y - line_spacing
    else:
        # Single line: sit higher in the title zone
        title1_y = 53.0
        title2_y = None

    pos1 = copy.deepcopy(pos)
    pos1[1] += title1_y
    opsvg.se(thing, shape="text", style="label.title",
             text=line1, size=title_size,
             halign="center", valign="center", pos=pos1)

    if title2_y is not None:
        pos1 = copy.deepcopy(pos)
        pos1[1] += title2_y
        opsvg.se(thing, shape="text", style="label.title",
                 text=line2, size=title_size,
                 halign="center", valign="center", pos=pos1)

    # ── Ruled blank lines ─────────────────────────────────────────────────────
    rule_line_w  = 86.0   # width of each ruled line
    rule_line_h  = 0.35   # thickness (rendered as a thin filled rect)
    rule_top_y   = 20.0   # y of first line (from centre, Y-up)
    rule_spacing = 11.0   # gap between consecutive lines

    for i in range(num_lines):
        pos1 = copy.deepcopy(pos)
        pos1[1] += rule_top_y - i * rule_spacing
        opsvg.se(thing, shape="rect", style="rule",
                 size=[rule_line_w, rule_line_h, 0], pos=pos1)

    # ── Bottom table (edge-to-edge — lines reach the card border) ─────────────
    table_w        = card_w           # full card width: 100 mm
    table_left     = -card_w / 2     # x = -50
    table_right    = +card_w / 2     # x = +50
    card_bottom_y  = -card_h / 2     # y = -79.5  (card's bottom edge)

    row1_h = 14.0   # header-label row
    row2_h = 18.0   # first data row
    row3_h = 18.0   # second data row

    # Pin the table flush to the card bottom
    table_bottom_y = card_bottom_y                            # -79.5
    table_top_y    = table_bottom_y + row1_h + row2_h + row3_h  # -29.5

    row1_bot_y = table_top_y  - row1_h                       # -43.5
    row2_bot_y = row1_bot_y   - row2_h                       # -61.5

    # y-centres of each row
    row1_cy = (table_top_y + row1_bot_y) / 2                 # -36.5
    row2_cy = (row1_bot_y  + row2_bot_y) / 2                 # -52.5
    row3_cy = (row2_bot_y  + table_bottom_y) / 2             # -70.5

    # Row 1 column geometry
    left_w   = table_w * 0.60                                 # 60 mm
    right_w  = table_w - left_w                              # 40 mm
    left_cx  = table_left  + left_w  / 2                     # -20
    right_cx = table_right - right_w / 2                     # +30

    # Row 1: left cell fill (light grey, no border)
    pos1 = copy.deepcopy(pos)
    pos1[0] += left_cx
    pos1[1] += row1_cy
    opsvg.se(thing, shape="rect", style="plate.light",
             size=[left_w, row1_h, 0], pos=pos1,
             stroke="none", stroke_width=0)

    # Row 1: right "Contents" cell fill (dark, no border)
    pos1 = copy.deepcopy(pos)
    pos1[0] += right_cx
    pos1[1] += row1_cy
    opsvg.se(thing, shape="rect", style="header",
             size=[right_w, row1_h, 0], pos=pos1,
             stroke="none", stroke_width=0)

    # "Contents" label text (white on dark)
    pos1 = copy.deepcopy(pos)
    pos1[0] += right_cx
    pos1[1] += row1_cy
    opsvg.se(thing, shape="text", style="header.label",
             text=table_label, size=7.0,
             halign="center", valign="center", pos=pos1)

    # ── Table grid lines ──────────────────────────────────────────────────────
    line_t   = 0.4      # line thickness in mm
    line_col = "#2E2E2E"

    def hline(y, x1=table_left, x2=table_right):
        """Thin horizontal line from x1 to x2 at y."""
        p = copy.deepcopy(pos)
        p[0] += (x1 + x2) / 2
        p[1] += y
        opsvg.se(thing, shape="rect", color=line_col, stroke="none", stroke_width=0,
                 size=[x2 - x1, line_t, 0], pos=p)

    def vline(x, y_top, y_bot):
        """Thin vertical line from y_top down to y_bot at x (Y-up coords)."""
        p = copy.deepcopy(pos)
        p[0] += x
        p[1] += (y_top + y_bot) / 2
        opsvg.se(thing, shape="rect", color=line_col, stroke="none", stroke_width=0,
                 size=[line_t, y_top - y_bot, 0], pos=p)

    # Horizontal rules: top of table, after row1, after row2
    # (no bottom rule — the card border closes the table at the bottom)
    hline(table_top_y)
    hline(row1_bot_y)
    hline(row2_bot_y)

    # Row 1 vertical divider: left 60 mm / right 40 mm
    row1_div_x = table_left + left_w                          # +10
    vline(row1_div_x, table_top_y, row1_bot_y)

    # Rows 2 & 3 vertical dividers: three equal columns
    # Extended to card_bottom_y so they pierce the border (border drawn last)
    col_w  = table_w / 3                                      # 33.33 mm
    div1_x = table_left + col_w                               # -16.67
    div2_x = table_left + col_w * 2                           # +16.67
    vline(div1_x, row1_bot_y, card_bottom_y)
    vline(div2_x, row1_bot_y, card_bottom_y)

    # ── Card border (drawn last — paints over any fill that bleeds to the edge)
    pos1 = copy.deepcopy(pos)
    opsvg.se(thing, shape="rounded_rectangle", style="plate.outline",
             size=[card_w, card_h, 0], r=r_outer, pos=pos1)

    if prepare_print:
        prepare_base_for_print(thing, pos, **kwargs)


def get_a4_sheet(thing, **kwargs):
    """A4-sized demo sheet — demonstrates every primitive shape component.

    Parameters (all optional kwargs)
    --------------------------------
    depth         : float — nominal depth passed through to emitted shapes
                            (default 3)
    stylesheet    : str | list[str]
                         — stylesheet name or merge list for the part. If not
                           supplied this builder uses "minimal" by default.
    styles        : dict  — per-part named style overrides such as plate,
                           plate.light, header.label, or label.mono; merged on
                           top of the resolved stylesheet before rendering

    Styling notes
    -------------
    This part uses named styles via style= in opsvg.se() calls. Use
    stylesheet to swap the overall look, then styles to override only the
    entries you need for this one part.
    """

    prepare_print = kwargs.get("prepare_print", False)
    depth = kwargs.get("depth", 3)
    pos   = kwargs.get("pos", [0, 0, 0])

    sheet_width  = 210.0
    sheet_height = 297.0
    content_inset  = 10.0
    content_width  = sheet_width  - 2 * content_inset
    content_height = sheet_height - 2 * content_inset

    if "styles" not in thing or not thing.get("styles"):
        sheet_name = kwargs.get("stylesheet", "minimal")
        thing["styles"] = _ss.get_stylesheet(sheet_name)


    # background sheet
    pos1 = copy.deepcopy(pos)
    opsvg.se(thing, shape="rect", style="plate",
             size=[sheet_width, sheet_height, depth], pos=pos1)

    # content area (slightly lighter inset)
    pos1 = copy.deepcopy(pos)
    opsvg.se(thing, shape="rounded_rectangle", style="plate.light",
             size=[content_width, content_height, depth], r=5.0, pos=pos1)

    # title text
    pos1 = copy.deepcopy(pos)
    pos1[1] += sheet_height / 2 - 30.0
    opsvg.se(thing, shape="text", style="header.label",
             text="A4 Demo Sheet", size=14.0, pos=pos1)

    # subtitle
    pos1 = copy.deepcopy(pos)
    pos1[1] += sheet_height / 2 - 48.0
    opsvg.se(thing, shape="text", style="header.label",
             text="oomlout SVG pipeline", size=7.0, pos=pos1)

    # version label (bottom-right, mono)
    pos1 = copy.deepcopy(pos)
    pos1[0] += sheet_width  / 2 - 8.0
    pos1[1] -= sheet_height / 2 - 8.0
    opsvg.se(thing, shape="text", style="label.mono",
             text="v1.0", size=4.0, halign="right", valign="center", pos=pos1)

    # triangle marker (top-right corner)
    pos1 = copy.deepcopy(pos)
    pos1[0] += sheet_width  / 2 - 20.0
    pos1[1] += sheet_height / 2 - 20.0
    opsvg.se(thing, shape="polygon", style="plate.accent",
             points=[[0, 4], [-6, -4], [6, -4]], pos=pos1)

    # corner punch (top-left)
    pos1 = copy.deepcopy(pos)
    pos1[0] -= sheet_width  / 2 - 20.0
    pos1[1] += sheet_height / 2 - 20.0
    opsvg.se(thing, shape="circle", style="hole",
             r=4.0, pos=pos1)

    # adjustment slot (bottom-centre)
    pos1 = copy.deepcopy(pos)
    pos1[1] -= sheet_height / 2 - 20.0
    opsvg.se(thing, shape="slot", style="slot",
             r=3.0, w=40.0, pos=pos1)

    if prepare_print:
        prepare_base_for_print(thing, pos, **kwargs)


def get_label_76x50(thing, **kwargs):
    """76.2 × 50.4 mm adhesive label — demonstrates text, header bar, and bullet.

    Parameters (all optional kwargs)
    --------------------------------
    depth         : float — nominal depth passed through to emitted shapes
                            (default 3)
    stylesheet    : str | list[str]
                         — stylesheet name or merge list applied to the part
                           before any local overrides
    styles        : dict  — per-part named style overrides such as plate,
                           header, plate.accent, label, label.muted, or
                           label.mono; merged on top of the resolved sheet

    Styling notes
    -------------
    The label is built entirely from named styles. Change stylesheet to swap
    the whole label theme, or use styles to override only selected entries for
    this part.
    """

    prepare_print = kwargs.get("prepare_print", False)
    depth = kwargs.get("depth", 3)
    pos   = kwargs.get("pos", [0, 0, 0])

    label_width   = 76.2
    label_height  = 50.4
    header_height = 12.0
    header_y      = label_height / 2 - header_height / 2

    # label body
    pos1 = copy.deepcopy(pos)
    opsvg.se(thing, shape="rounded_rectangle", style="plate",
             size=[label_width, label_height, depth], r=3.0, pos=pos1)

    # header bar
    pos1 = copy.deepcopy(pos)
    pos1[1] += header_y
    opsvg.se(thing, shape="rect", style="header",
             size=[label_width, header_height, depth], pos=pos1)

    # header title
    pos1 = copy.deepcopy(pos)
    pos1[1] += header_y
    opsvg.se(thing, shape="text", style="header.label",
             text="OOMLOUT", size=9.0, pos=pos1)

    # bullet mark (accent dot)
    pos1 = copy.deepcopy(pos)
    pos1[0] -= label_width / 2 - 8.0
    pos1[1] += header_y - header_height - 4.0
    opsvg.se(thing, shape="circle", style="plate.accent",
             r=1.5, pos=pos1)

    # part name
    pos1 = copy.deepcopy(pos)
    pos1[0] -= label_width / 2 - 13.0
    pos1[1] += header_y - header_height - 4.0
    opsvg.se(thing, shape="text", style="label",
             text="Bracket  4 x 2", size=5.0, halign="left", valign="center", pos=pos1)

    # description (muted)
    pos1 = copy.deepcopy(pos)
    pos1[0] -= label_width / 2 - 6.0
    pos1[1] += header_y - header_height - 11.0
    opsvg.se(thing, shape="text", style="label.muted",
             text="L-shaped laser-cut plate", size=4.0, halign="left", valign="center", pos=pos1)

    # part number footer (mono, bottom-right)
    pos1 = copy.deepcopy(pos)
    pos1[0] += label_width  / 2 - 4.0
    pos1[1] -= label_height / 2 - 5.0
    opsvg.se(thing, shape="text", style="label.mono",
             text="OOBB-BKT-4x2-001", size=3.0, halign="right", valign="center", pos=pos1)

    if prepare_print:
        prepare_base_for_print(thing, pos, **kwargs)
