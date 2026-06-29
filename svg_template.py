import copy
import math
import opsvg
import svg_styles


def mech_drawing_page(thing, draw_fn=None, **kwargs):
    """A4 mechanical drawing sheet layout.

    Draws background, border, header, view labels, and summary/footer.
    Calls draw_fn(thing, **layout) to render the actual hardware item
    in the view area.

    kwargs
    ------
    pos             : [x, y, z]  page centre position
    hardware_type   : 'nut' | 'bolt' | 'set_screw'
    part_title      : large identifier, e.g. 'M6'
    part_series     : series/spec string
    part_category   : header category string
    id_mm           : thread bore diameter mm
    af_mm           : across-flats width mm
    height_mm       : nut thickness mm
    head_height_mm  : bolt head height mm  (defaults to height_mm)
    length_mm       : bolt shank length mm (defaults to height_mm)
    thread_length_mm: threaded portion mm  (defaults to length_mm)
    part_code       : standard code string
    part_name       : full part identifier
    view_scale      : drawing scale (auto-computed when None)
    """
    pos              = kwargs.get("pos",              [0, 0, 0])
    hardware_type    = kwargs.get("hardware_type",    "nut")
    part_title       = str(kwargs.get("part_title",       "M6"))
    part_id          = thing.get("id", "")
    part_series      = str(kwargs.get("part_series",      "METRIC HEX NUT"))
    part_category    = str(kwargs.get("part_category",    "HARDWARE / NUT"))
    id_mm            = float(kwargs.get("id_mm",        6.0))
    af_mm            = float(kwargs.get("af_mm",       10.0))
    height_mm        = float(kwargs.get("height_mm",    5.0))
    head_height_mm   = float(kwargs.get("head_height_mm",  height_mm))
    length_mm        = float(kwargs.get("length_mm",       height_mm))
    thread_length_mm = float(kwargs.get("thread_length_mm", length_mm))
    part_code        = str(kwargs.get("part_code",      ""))
    part_name        = str(kwargs.get("part_name",      ""))
    view_scale       = kwargs.get("view_scale", None)

    W, H = 210.0, 297.0

    brand_y      =  H / 2 - 14.0
    title_y      =  H / 2 - 40.0 + 3
    part_name_y  =  H / 2 - 57.0 + 8
    series_y     =  H / 2 - 67.0
    rule1_y      =  H / 2 - 76.0
    dim_head_y   =  H / 2 - 83.0
    view_label_y =  H / 2 - 97.0
    rule2_y      = -H / 2 + 72.0

    # Auto-scale to fit views between view_label_y and rule2_y
    if view_scale is None:
        r_c   = af_mm / math.sqrt(3)
        avail = view_label_y - rule2_y
        scale_front = (avail - 37.0) / (3.5 * r_c)
        if hardware_type == "nut":
            scale_side = scale_front
        else:
            total_mm = length_mm + head_height_mm
            scale_side = (avail - 30.0) / total_mm
        scale_w = (W / 4.0 - 10.0) / r_c
        s_raw  = min(scale_front, scale_side, scale_w)
        view_scale = max(1, int(s_raw)) if s_raw >= 1.0 else 0.5

    r_c_d        = (af_mm / math.sqrt(3)) * view_scale
    af_d         = af_mm * view_scale
    bore_r_d     = (id_mm / 2.0) * view_scale
    height_d     = height_mm * view_scale
    upper_vert_y = r_c_d / 2
    ann_ts       = 3.8

    if hardware_type == "nut":
        above_vc = upper_vert_y + 8 + ann_ts + 3
        below_vc = r_c_d + 8 + ann_ts + 3
    else:
        total_d_raw = (length_mm + head_height_mm) * view_scale
        above_vc = total_d_raw / 2 + 15
        below_vc = total_d_raw / 2 + 15

    content_top = view_label_y - 8
    content_bot = rule2_y
    content_mid = (content_top + content_bot) / 2
    view_cy = content_mid + (below_vc - above_vc) / 2

    front_cx = -W / 4
    side_cx  =  W / 4

    # ── Stylesheet ────────────────────────────────────────────────────────────
    thing["styles"] = svg_styles.get_stylesheet("project_bolt")
    _st = thing["styles"]

    _plate_c  = _st.get("plate",         {}).get("color",        "#FAFAFA")
    _plate_sk = _st.get("plate.outline", {}).get("stroke",       "#1A1A1A")
    _plate_sw = _st.get("plate.outline", {}).get("stroke_width", 0.8)
    _cut_c    = _st.get("hole.cut",      {}).get("color",        "#FFFFFF")
    _cut_sk   = _st.get("hole.cut",      {}).get("stroke",       "#444444")
    _cut_sw   = _st.get("hole.cut",      {}).get("stroke_width", 0.3)
    _dim_sk   = _st.get("outline",       {}).get("stroke",       "#1A1A1A")
    _dim_sw   = _st.get("outline",       {}).get("stroke_width", 0.5)
    _lbl_c    = _st.get("label",         {}).get("color",        "#1A1A1A")
    _mut_c    = _st.get("label.muted",   {}).get("color",        "#888888")
    _tit_c    = _st.get("label.title",   {}).get("color",        "#111111")
    _hdr_c    = _st.get("header",        {}).get("color",        "#1C1C1C")
    _light_sk = _st.get("outline.light", {}).get("stroke",       "#AAAAAA")
    _light_sw = _st.get("outline.light", {}).get("stroke_width", 0.3)

    # ── Layout helpers ────────────────────────────────────────────────────────
    def _abs_pos(x_off, y_off):
        p = copy.deepcopy(pos)
        p[0] += x_off
        p[1] += y_off
        return p

    def _hline(y_coord, x1=-W / 2 + 10, x2=W / 2 - 10, sw=None):
        lpos = _abs_pos(0, y_coord)
        opsvg.se(thing, shape="line",
                 p1=[x1, 0], p2=[x2, 0],
                 color=_dim_sk, stroke_width=(sw if sw is not None else _dim_sw),
                 pos=lpos)

    def _text_at(x_off, y_off, text, size=4.0, halign="center",
                 color=None, bold=False, muted=False):
        tpos = _abs_pos(x_off, y_off)
        col  = _mut_c if muted else (color or _lbl_c)
        fw   = "bold" if bold else ""
        opsvg.se(thing, shape="text",
                 text=text, size=size, halign=halign, valign="center",
                 color=col, font_weight=fw, pos=tpos)

    def _dim(cx_off, cy_off, p1, p2, offset, text, direction="auto"):
        dpos = _abs_pos(cx_off, cy_off)
        opsvg.se(thing, shape="dimension_line",
                 p1=p1, p2=p2, offset=offset, direction=direction,
                 text=text, text_size=ann_ts,
                 color=_dim_sk, stroke_width=_dim_sw, pos=dpos)

    def _hex_pts(r):
        return [[r * math.cos(math.radians(90 + 60 * i)),
                 r * math.sin(math.radians(90 + 60 * i))]
                for i in range(6)]

    # ── Background + border ───────────────────────────────────────────────────
    opsvg.se(thing, shape="rect", color="#ffffff",
             size=[W, H, 0], pos=_abs_pos(0, 0))
    opsvg.se(thing, shape="rounded_rectangle",
             color="none", stroke=_plate_sk, stroke_width=_plate_sw,
             size=[W - 8, H - 8, 0], r=3.5, pos=_abs_pos(0, 0))

    # ── Header ────────────────────────────────────────────────────────────────
    _text_at(-W / 2 + 14, brand_y,     part_id,        size=3.2,  halign="left", muted=True)
    _text_at(-W / 2 + 14, title_y,     part_title,     size=18.0, halign="left", bold=True, color=_hdr_c)
    _text_at(-W / 2 + 14, part_name_y, part_category,  size=4.5,  halign="left", muted=True)
    _text_at(-W / 2 + 14, series_y,    part_series,    size=4.0,  halign="left", muted=True)
    _hline(rule1_y)
    _text_at(-W / 2 + 14, dim_head_y, "DIMENSIONS", size=5.2, halign="left", bold=True, color=_tit_c)
    scale_label = f"{int(view_scale)}:1" if view_scale >= 1 else f"1:{int(round(1 / view_scale))}"
    _text_at(W / 2 - 14, dim_head_y, f"{scale_label} RATIO  —  PRINT AT 100%",
             size=3.2, halign="right", muted=True)

    # ── Hardware item (draw_fn also writes its own view labels) ──────────────
    if draw_fn is not None:
        draw_fn(thing,
                pos=pos,
                front_cx=front_cx, side_cx=side_cx, view_cy=view_cy,
                view_label_y=view_label_y,
                view_area_top=content_top, view_area_bot=content_bot,
                r_c_d=r_c_d, af_d=af_d, bore_r_d=bore_r_d,
                height_d=height_d, view_scale=view_scale, ann_ts=ann_ts,
                upper_vert_y=upper_vert_y,
                _plate_c=_plate_c, _plate_sk=_plate_sk, _plate_sw=_plate_sw,
                _cut_c=_cut_c,     _cut_sk=_cut_sk,     _cut_sw=_cut_sw,
                _dim_sk=_dim_sk,   _dim_sw=_dim_sw,
                _lbl_c=_lbl_c,     _mut_c=_mut_c,       _tit_c=_tit_c,
                _light_sk=_light_sk, _light_sw=_light_sw,
                abs_pos_fn=_abs_pos, text_at_fn=_text_at,
                dim_fn=_dim, hex_pts_fn=_hex_pts,
                **kwargs)

    # ── Summary / footer ──────────────────────────────────────────────────────
    val_y   = -H / 2 + 61.0
    lbl_y   = -H / 2 + 53.5
    rule3_y = -H / 2 + 46.0
    code_y  = -H / 2 + 38.0
    name_y  = -H / 2 + 29.0
    rule4_y = -H / 2 + 20.0
    foot_y  = -H / 2 + 12.0

    _hline(rule2_y)

    margin    = -W / 2 + 14
    content_w = W - 28

    cols = kwargs.get("summary_cols", [])

    step = content_w / len(cols) if cols else content_w
    for i, (val, lbl) in enumerate(cols):
        x = margin + i * step
        _text_at(x, val_y, val, size=5.5, halign="left", bold=True, color=_tit_c)
        _text_at(x, lbl_y, lbl, size=3.0, halign="left", muted=True)

    _hline(rule3_y, sw=0.3)
    if part_code:
        _text_at(margin, code_y, part_code, size=3.2, halign="left", muted=True)
    _text_at(margin, name_y,
             part_name if part_name else part_title,
             size=3.0, halign="left", color="#aaaaaa")
    _hline(rule4_y, sw=0.3)
    md5_6    = thing.get("md5_6", "")
    foot_url = f"oom.lt/{md5_6}" if md5_6 else "oomlout.com"
    _text_at(margin,      foot_y, "OOMLOUT", size=2.8, halign="left",  muted=True)
    _text_at(W / 2 - 14, foot_y, foot_url,  size=2.8, halign="right", muted=True)
