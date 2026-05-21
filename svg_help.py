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
