"""
svg_a4.py — A4 presentation sheet generator

Wraps a part SVG in a technical A4 drawing sheet:
  - Double-line border frame
  - Part SVG centred and scaled to fit (scale factor annotated if < 1)
  - Title block at bottom: project / part name, dimensions, scale, date

Outputs:
  working_svg_a4.svg   — always
  working_svg_a4.pdf   — if cairosvg or weasyprint is available
"""

import datetime
import os
import re

# ---------------------------------------------------------------------------
# A4 constants (mm)
# ---------------------------------------------------------------------------
A4_W = 210.0
A4_H = 297.0

MARGIN_OUTER = 8.0      # outer margin before frame outer line
FRAME_GAP    = 2.5      # gap between double-line frame lines
TITLE_H      = 28.0     # height of the bottom title block
TITLE_FRAME_GAP = 2.5   # inner gap inside title-block divider double-line

CONTENT_X  = MARGIN_OUTER + FRAME_GAP
CONTENT_Y  = MARGIN_OUTER + FRAME_GAP
CONTENT_W  = A4_W - 2 * (MARGIN_OUTER + FRAME_GAP)
CONTENT_H  = A4_H - 2 * (MARGIN_OUTER + FRAME_GAP) - TITLE_H

FONT_STACK = "Swis721 Blk BT, comic sans ms"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _parse_viewbox(svg_text):
    """Return (w_mm, h_mm) from the viewBox / width / height of an SVG."""
    # Try width/height attributes first (they carry units)
    m = re.search(r'<svg[^>]+width="([0-9.]+)mm"[^>]+height="([0-9.]+)mm"', svg_text, re.S)
    if m:
        return float(m.group(1)), float(m.group(2))
    # Fall back to viewBox (treated as mm — this pipeline writes viewBox in mm)
    m = re.search(r'viewBox="[0-9.]+ [0-9.]+ ([0-9.]+) ([0-9.]+)"', svg_text)
    if m:
        return float(m.group(1)), float(m.group(2))
    return None, None


def _strip_svg_wrapper(svg_text):
    """Return just the inner content of an SVG (strip xml decl + outer <svg> tags)."""
    # Remove XML declaration
    inner = re.sub(r'<\?xml[^?]*\?>', '', svg_text)
    # Remove the outer <svg ...> opening tag
    inner = re.sub(r'<svg[^>]*>', '', inner, count=1)
    # Remove the closing </svg>
    inner = re.sub(r'</svg>', '', inner, count=1)
    return inner.strip()


def _rect(x, y, w, h, fill="none", stroke="#1A1A1A", stroke_width=0.5):
    return (f'  <rect x="{x:.4f}" y="{y:.4f}" '
            f'width="{w:.4f}" height="{h:.4f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" />\n')


def _line(x1, y1, x2, y2, stroke="#1A1A1A", stroke_width=0.5):
    return (f'  <line x1="{x1:.4f}" y1="{y1:.4f}" '
            f'x2="{x2:.4f}" y2="{y2:.4f}" '
            f'stroke="{stroke}" stroke-width="{stroke_width}" />\n')


def _text(x, y, content, size=3.5, anchor="start", baseline="middle",
          weight="normal", fill="#1A1A1A", max_width=None):
    tl_attr = (f' textLength="{max_width:.4f}" lengthAdjust="spacingAndGlyphs"'
               if max_width is not None else "")
    return (f'  <text x="{x:.4f}" y="{y:.4f}" '
            f'font-family="{FONT_STACK}" font-size="{size:.4f}" '
            f'font-weight="{weight}" '
            f'text-anchor="{anchor}" dominant-baseline="{baseline}" '
            f'fill="{fill}"{tl_attr}>{content}</text>\n')


# ---------------------------------------------------------------------------
# main builder
# ---------------------------------------------------------------------------

def make_a4_sheet(svg_path, folder, part, thing, filename_extra=""):
    """
    Build working_a4.svg (and working_a4.pdf if a renderer is available)
    alongside the part's working_svg.svg.

    Parameters
    ----------
    svg_path : str   path to working_svg.svg (just written)
    folder   : str   output folder (parts/<id>/)
    part     : dict  part metadata dict
    thing    : dict  full thing dict
    """
    # ---- read the part SVG -------------------------------------------------
    try:
        with open(svg_path, "r", encoding="utf-8") as fh:
            part_svg_text = fh.read()
    except FileNotFoundError:
        print(f"  svg_a4: source not found — {svg_path}")
        return

    part_w, part_h = _parse_viewbox(part_svg_text)
    if part_w is None:
        print("  svg_a4: could not parse viewBox — skipping A4 sheet")
        return

    # ---- scale to fit content area -----------------------------------------
    avail_w = CONTENT_W
    avail_h = CONTENT_H

    scale = min(avail_w / part_w, avail_h / part_h, 1.0)
    scale_pct = scale * 100.0

    scaled_w = part_w * scale
    scaled_h = part_h * scale

    # Centre in content area
    ox = CONTENT_X + (avail_w - scaled_w) / 2.0
    oy = CONTENT_Y + (avail_h - scaled_h) / 2.0

    # ---- metadata ----------------------------------------------------------
    kwargs          = part.get("kwargs", {})
    oobb_name       = part.get("oobb_name", "unknown")
    project_raw     = part.get("project_name", "")
    project_name    = os.path.basename(project_raw.rstrip("/\\")) if project_raw else ""
    dims_str        = f"{part_w:.1f} × {part_h:.1f} mm"
    date_str        = datetime.date.today().isoformat()
    scale_str       = f"1:1" if abs(scale - 1.0) < 0.001 else f"{scale:.3f}× ({scale_pct:.1f}%)"

    # ---- build SVG ---------------------------------------------------------
    lines = []
    lines.append('<?xml version="1.0" encoding="utf-8"?>\n')
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg"\n')
    lines.append(f'     width="{A4_W:.4f}mm" height="{A4_H:.4f}mm"\n')
    lines.append(f'     viewBox="0 0 {A4_W:.4f} {A4_H:.4f}">\n')
    lines.append('\n')

    # White background
    lines.append(f'  <rect x="0" y="0" width="{A4_W:.4f}" height="{A4_H:.4f}" '
                 f'fill="white" stroke="none" />\n')

    # --- outer frame line ---
    fo = MARGIN_OUTER
    fw = A4_W - 2 * fo
    fh_val = A4_H - 2 * fo
    lines.append(_rect(fo, fo, fw, fh_val, stroke_width=0.35))

    # --- inner frame line ---
    fi = MARGIN_OUTER + FRAME_GAP
    fiw = A4_W - 2 * fi
    fih = A4_H - 2 * fi
    lines.append(_rect(fi, fi, fiw, fih, stroke_width=0.7))

    # --- title block --------------------------------------------------------
    title_y = A4_H - MARGIN_OUTER - TITLE_H
    # outer horizontal line (top of title block — outer frame)
    lines.append(_line(fo, title_y, fo + fw, title_y, stroke_width=0.35))
    # inner horizontal line (top of title block — inner frame)
    lines.append(_line(fi, title_y + TITLE_FRAME_GAP,
                       fi + fiw, title_y + TITLE_FRAME_GAP, stroke_width=0.7))

    tb_inner_y = title_y + TITLE_FRAME_GAP   # top of usable title area
    tb_inner_h = fih - (tb_inner_y - fi)     # = A4_H - fi - tb_inner_y
    tb_bot     = fi + fih                    # = A4_H - fi

    # Vertical dividers inside title block
    # Layout: | Name (wide) | Dims | Scale | Date |
    col_dims_w  = 38.0
    col_scale_w = 30.0
    col_date_w  = 30.0
    col_name_w  = fiw - col_dims_w - col_scale_w - col_date_w

    x_dims  = fi + col_name_w
    x_scale = x_dims + col_dims_w
    x_date  = x_scale + col_scale_w

    for vx in [x_dims, x_scale, x_date]:
        lines.append(_line(vx, title_y, vx, tb_bot, stroke_width=0.35))
        lines.append(_line(vx, tb_inner_y, vx, tb_bot, stroke_width=0.7))

    # Title block text
    mid_y     = (tb_inner_y + tb_bot) / 2.0
    pad       = 3.0
    name_usable = col_name_w - 2 * pad   # max width for name column text

    # Project name (small label, top of name column)
    if project_name:
        lines.append(_text(fi + pad, mid_y - 4.5, project_name,
                           size=2.8, fill="#555555", anchor="start",
                           max_width=name_usable))

    # Part name (large bold — clamped to column width via textLength)
    lines.append(_text(fi + pad, mid_y + 1.5, oobb_name,
                       size=5.5, weight="bold", anchor="start",
                       max_width=name_usable))

    # Dims column
    lines.append(_text(x_dims + pad, mid_y - 4.0, "Dimensions", size=2.8, anchor="start"))
    lines.append(_text(x_dims + pad, mid_y + 1.0, dims_str, size=3.5,
                       weight="bold", anchor="start"))

    # Scale column
    lines.append(_text(x_scale + pad, mid_y - 4.0, "Scale", size=2.8, anchor="start"))
    lines.append(_text(x_scale + pad, mid_y + 1.0, scale_str, size=3.5,
                       weight="bold", anchor="start"))

    # Date column
    lines.append(_text(x_date + pad, mid_y - 4.0, "Date", size=2.8, anchor="start"))
    lines.append(_text(x_date + pad, mid_y + 1.0, date_str, size=3.5,
                       weight="bold", anchor="start"))

    # --- scale-reduction annotation -----------------------------------------
    if scale < 0.999:
        ann_x = CONTENT_X + avail_w / 2.0
        ann_y = oy - 5.0
        lines.append(_text(ann_x, ann_y,
                           f"SCALE {scale_pct:.1f}%  ({part_w:.1f}×{part_h:.1f} mm original)",
                           size=2.8, anchor="middle", fill="#AA4400"))

    # --- embedded part SVG --------------------------------------------------
    inner = _strip_svg_wrapper(part_svg_text)
    lines.append(f'  <g transform="translate({ox:.4f},{oy:.4f}) scale({scale:.6f})">\n')
    # Indent inner content by two spaces for readability
    for src_line in inner.splitlines():
        lines.append('    ' + src_line + '\n')
    lines.append('  </g>\n')

    lines.append('</svg>\n')

    import os as _os
    stem        = _os.path.splitext(_os.path.basename(svg_path))[0]
    suffix      = f"_{filename_extra}" if filename_extra else ""
    a4_svg_path = os.path.join(folder, f"{stem}_a4{suffix}.svg")
    with open(a4_svg_path, "w", encoding="utf-8") as fh:
        fh.writelines(lines)
    print(f"  svg_a4: wrote {a4_svg_path}")

    # ---- optional PDF ------------------------------------------------------
    _try_write_pdf(a4_svg_path, folder, filename_extra=filename_extra)


def make_pdf(svg_path, folder):
    """Convert any SVG file directly to PDF without the A4 wrapper."""
    _try_write_pdf(svg_path, folder)


def _try_write_pdf(a4_svg_path, folder, filename_extra=""):
    """Try cairosvg then weasyprint to emit a PDF."""
    import os as _os
    stem     = _os.path.splitext(_os.path.basename(a4_svg_path))[0]
    pdf_path = os.path.join(folder, f"{stem}.pdf")

    # cairosvg
    try:
        import cairosvg
        cairosvg.svg2pdf(url=a4_svg_path, write_to=pdf_path)
        print(f"  svg_a4: wrote {pdf_path}  (cairosvg)")
        return
    except ImportError:
        pass
    except Exception as exc:
        print(f"  svg_a4: cairosvg failed — {exc}")

    # weasyprint
    try:
        from weasyprint import HTML
        HTML(filename=a4_svg_path).write_pdf(pdf_path)
        print(f"  svg_a4: wrote {pdf_path}  (weasyprint)")
        return
    except ImportError:
        pass
    except Exception as exc:
        print(f"  svg_a4: weasyprint failed — {exc}")

    print("  svg_a4: no PDF renderer found (install cairosvg or weasyprint for PDF output)")
