from __future__ import annotations

import argparse
import ast
import html
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

# oobb_arch lives in old/ after the restructure; add it to the path so the
# import below works regardless of the working directory.
sys.path.insert(0, str(Path(__file__).parent.parent / "old"))
sys.path.insert(0, str(Path(__file__).parent.parent))

from oobb_arch.catalog.object_discovery import discover_objects
from oobb_arch.catalog.part_set_discovery import discover_part_sets
import oobb


def _coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _read_text_if_exists(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return ""


def _parse_literal(value: str) -> Any:
    if not value:
        return ""
    try:
        return json.loads(value)
    except Exception:
        pass
    try:
        return ast.literal_eval(value)
    except Exception:
        return value


def _normalize_variables(raw_variables: Any) -> list[dict[str, Any]]:
    if not isinstance(raw_variables, list):
        return []

    normalized: list[dict[str, Any]] = []
    for item in raw_variables:
        if isinstance(item, dict):
            name = _coerce_text(item.get("name"))
            if not name:
                continue
            normalized.append(
                {
                    "name": name,
                    "description": _coerce_text(item.get("description", "")),
                    "type": _coerce_text(item.get("type", "")),
                    "default": item.get("default", ""),
                }
            )
        elif isinstance(item, str):
            name = item.strip()
            if not name:
                continue
            normalized.append({"name": name, "description": "", "type": "", "default": ""})
    return normalized


def _build_summary(description: str, variable_names: list[str], returns_text: str) -> str:
    if description:
        first_sentence = description.split(".")[0].strip()
        if first_sentence:
            return first_sentence + ("." if not first_sentence.endswith(".") else "")
    if variable_names:
        return f"Inputs: {', '.join(variable_names)}"
    if returns_text:
        return f"Returns: {returns_text}"
    return "No summary available."


def _build_default_values(variables: list[dict[str, Any]]) -> dict[str, Any]:
    defaults: dict[str, Any] = {}
    for variable in variables:
        name = variable.get("name", "")
        if not name:
            continue
        default = variable.get("default", "")
        defaults[name] = default if default not in ("", None) else "undocumented"
    return defaults


def _build_set_values(sample: dict[str, Any]) -> Any:
    if sample.get("kwargs"):
        return sample["kwargs"]

    set_values: dict[str, Any] = {}
    if sample.get("helper_kwargs"):
        set_values["helper_kwargs"] = sample["helper_kwargs"]
    if sample.get("companion_geometry_kwargs"):
        set_values["companion_geometry_kwargs"] = sample["companion_geometry_kwargs"]
    return set_values or None


def _extract_bullet_value(block: str, label: str) -> str:
    pattern = rf"^- {re.escape(label)}:\s*(.*)$"
    match = re.search(pattern, block, flags=re.M)
    return match.group(1).strip() if match else ""


def _parse_test_samples(samples_path: Path, component_name: str) -> dict[str, Any]:
    text = _read_text_if_exists(samples_path)
    if not text:
        return {"samples": [], "notes": "", "output_files": []}

    sample_entries: list[dict[str, Any]] = []
    sample_pattern = re.compile(
        r"^### Sample \d+: `([^`]+)`\s*(.*?)(?=^### Sample \d+:|^## Folder-specific notes|\Z)",
        flags=re.M | re.S,
    )

    for match in sample_pattern.finditer(text):
        filename = match.group(1).strip()
        block = match.group(2)
        preview_rot_raw = _extract_bullet_value(block, "preview_rot").strip("`")

        sample_entry = {
            "filename": filename,
            "intent": _extract_bullet_value(block, "Intent"),
            "preview_rot": _parse_literal(preview_rot_raw) if preview_rot_raw else [0, 0, 0],
            "kwargs": _parse_literal(_extract_bullet_value(block, "kwargs").strip("`")),
            "helper_kwargs": _parse_literal(_extract_bullet_value(block, "helper_kwargs").strip("`")),
            "companion_geometry_kwargs": _parse_literal(
                _extract_bullet_value(block, "companion_geometry_kwargs").strip("`")
            ),
            "implementation_rule": _extract_bullet_value(block, "Implementation rule"),
        }

        if sample_entry["kwargs"] == "":
            sample_entry["kwargs"] = None
        if sample_entry["helper_kwargs"] == "":
            sample_entry["helper_kwargs"] = None
        if sample_entry["companion_geometry_kwargs"] == "":
            sample_entry["companion_geometry_kwargs"] = None
        sample_entries.append(sample_entry)

    folder_notes = ""
    folder_section_match = re.search(
        r"^## Folder-specific notes\s*(.*)$",
        text,
        flags=re.M | re.S,
    )
    if folder_section_match:
        folder_block = folder_section_match.group(1)
        folder_notes = _extract_bullet_value(folder_block, "Notes")

    output_files = [entry["filename"] for entry in sample_entries]
    return {
        "samples": sample_entries,
        "notes": folder_notes,
        "output_files": output_files,
        "has_test_samples_doc": True,
        "component_name": component_name,
    }


def _collect_sample_images(
    folder: Path,
    component_name: str,
    sample_doc: dict[str, Any],
    variables: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    test_dir = folder / "test"
    image_entries: list[dict[str, Any]] = []
    default_values = _build_default_values(variables)

    for sample in sample_doc.get("samples", []):
        sample_id = sample["filename"].replace(".png", "")
        sample_dir = test_dir / sample_id
        iso_400_path = sample_dir / "image_400.png"
        iso_120_path = sample_dir / "image_120.png"
        top_400_path = sample_dir / "image_top_400.png"
        top_120_path = sample_dir / "image_top_120.png"
        side_400_path = sample_dir / "image_side_400.png"
        side_120_path = sample_dir / "image_side_120.png"
        png_path = sample_dir / "image.png"
        scad_path = sample_dir / "working.scad"
        image_exists = iso_400_path.exists() or png_path.exists()
        image_rel = (
            f"{component_name}/test/{sample_id}/image_400.png"
            if iso_400_path.exists()
            else f"{component_name}/test/{sample_id}/image.png"
        )
        detail_image_rel = (
            f"test/{sample_id}/image_400.png"
            if iso_400_path.exists()
            else f"test/{sample_id}/image.png"
        )

        image_entries.append(
            {
                "sample_id": sample_id,
                "filename": sample["filename"],
                "title": sample.get("intent") or sample["filename"],
                "intent": sample.get("intent", ""),
                "preview_rot": sample.get("preview_rot", [0, 0, 0]),
                "kwargs": sample.get("kwargs"),
                "helper_kwargs": sample.get("helper_kwargs"),
                "companion_geometry_kwargs": sample.get("companion_geometry_kwargs"),
                "set_values": _build_set_values(sample),
                "default_values": default_values,
                "implementation_rule": sample.get("implementation_rule", ""),
                "exists": image_exists,
                "image_path": image_rel,
                "detail_image_path": detail_image_rel,
                "full_image_path": f"{component_name}/test/{sample_id}/image.png",
                "detail_full_image_path": f"test/{sample_id}/image.png",
                "detail_iso_400_path": detail_image_rel,
                "detail_iso_120_path": (
                    f"test/{sample_id}/image_120.png"
                    if iso_120_path.exists()
                    else detail_image_rel
                ),
                "detail_top_400_path": (
                    f"test/{sample_id}/image_top_400.png"
                    if top_400_path.exists()
                    else detail_image_rel
                ),
                "detail_top_120_path": (
                    f"test/{sample_id}/image_top_120.png"
                    if top_120_path.exists()
                    else detail_image_rel
                ),
                "detail_side_400_path": (
                    f"test/{sample_id}/image_side_400.png"
                    if side_400_path.exists()
                    else detail_image_rel
                ),
                "detail_side_120_path": (
                    f"test/{sample_id}/image_side_120.png"
                    if side_120_path.exists()
                    else detail_image_rel
                ),
                "scad_exists": scad_path.exists(),
                "scad_path": f"{component_name}/test/{sample_id}/working.scad",
                "detail_scad_path": f"test/{sample_id}/working.scad",
            }
        )

    if image_entries:
        return image_entries

    if not test_dir.exists():
        return []

    for sample_dir in sorted(path for path in test_dir.iterdir() if path.is_dir()):
        iso_400_path = sample_dir / "image_400.png"
        iso_120_path = sample_dir / "image_120.png"
        top_400_path = sample_dir / "image_top_400.png"
        top_120_path = sample_dir / "image_top_120.png"
        side_400_path = sample_dir / "image_side_400.png"
        side_120_path = sample_dir / "image_side_120.png"
        png_path = sample_dir / "image.png"
        scad_path = sample_dir / "working.scad"
        image_exists = iso_400_path.exists() or png_path.exists()
        image_rel = (
            f"{component_name}/test/{sample_dir.name}/image_400.png"
            if iso_400_path.exists()
            else f"{component_name}/test/{sample_dir.name}/image.png"
        )
        detail_image_rel = (
            f"test/{sample_dir.name}/image_400.png"
            if iso_400_path.exists()
            else f"test/{sample_dir.name}/image.png"
        )
        image_entries.append(
            {
                "sample_id": sample_dir.name,
                "filename": sample_dir.name,
                "title": sample_dir.name,
                "intent": "",
                "preview_rot": [0, 0, 0],
                "kwargs": None,
                "helper_kwargs": None,
                "companion_geometry_kwargs": None,
                "set_values": None,
                "default_values": default_values,
                "implementation_rule": "",
                "exists": image_exists,
                "image_path": image_rel,
                "detail_image_path": detail_image_rel,
                "full_image_path": f"{component_name}/test/{sample_dir.name}/image.png",
                "detail_full_image_path": f"test/{sample_dir.name}/image.png",
                "detail_iso_400_path": detail_image_rel,
                "detail_iso_120_path": (
                    f"test/{sample_dir.name}/image_120.png"
                    if iso_120_path.exists()
                    else detail_image_rel
                ),
                "detail_top_400_path": (
                    f"test/{sample_dir.name}/image_top_400.png"
                    if top_400_path.exists()
                    else detail_image_rel
                ),
                "detail_top_120_path": (
                    f"test/{sample_dir.name}/image_top_120.png"
                    if top_120_path.exists()
                    else detail_image_rel
                ),
                "detail_side_400_path": (
                    f"test/{sample_dir.name}/image_side_400.png"
                    if side_400_path.exists()
                    else detail_image_rel
                ),
                "detail_side_120_path": (
                    f"test/{sample_dir.name}/image_side_120.png"
                    if side_120_path.exists()
                    else detail_image_rel
                ),
                "scad_exists": scad_path.exists(),
                "scad_path": f"{component_name}/test/{sample_dir.name}/working.scad",
                "detail_scad_path": f"test/{sample_dir.name}/working.scad",
            }
        )
    return image_entries


def _render_variables_table_markdown(variables: list[dict[str, Any]]) -> list[str]:
    lines = ["| Name | Description | Type | Default |", "|------|-------------|------|---------|"]
    if not variables:
        lines.append("| - | - | - | - |")
        return lines

    for variable in variables:
        name = _coerce_text(variable.get("name"))
        description = _coerce_text(variable.get("description"))
        var_type = _coerce_text(variable.get("type"))
        default = _coerce_text(variable.get("default", ""))
        lines.append(f"| {name} | {description} | {var_type} | {default} |")
    return lines


def _build_default_detail_markdown(entry: dict[str, Any]) -> str:
    lines = [
        f"# {entry['command']}",
        "",
        f"**{entry['name_long']}**",
        "",
        entry.get("description", "") or "No description available.",
        "",
        "## Returns",
        "",
        entry.get("returns", "") or "No return information available.",
        "",
        "## Variables",
        "",
    ]
    lines.extend(_render_variables_table_markdown(entry.get("variables", [])))

    if entry.get("sample_notes"):
        lines.extend(
            [
                "",
                "## Sample Notes",
                "",
                entry["sample_notes"],
            ]
        )

    return "\n".join(lines).strip()


def _markdown_inline_to_html(text: str) -> str:
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    return escaped


def _render_markdown_table(lines: list[str]) -> str:
    if len(lines) < 2:
        return ""
    rows = []
    for line in lines:
        stripped = line.strip().strip("|")
        cells = [_markdown_inline_to_html(cell.strip()) for cell in stripped.split("|")]
        rows.append(cells)

    header = rows[0]
    body = rows[2:] if len(rows) > 2 else []
    header_html = "".join(f"<th>{cell}</th>" for cell in header)
    body_html = "".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
        for row in body
    )
    return (
        '<div class="markdown-table-wrap"><table class="markdown-table">'
        f"<thead><tr>{header_html}</tr></thead>"
        f"<tbody>{body_html}</tbody>"
        "</table></div>"
    )


def _markdown_to_html(markdown_text: str) -> str:
    if not markdown_text.strip():
        return ""

    lines = markdown_text.splitlines()
    html_parts: list[str] = []
    paragraph_lines: list[str] = []
    list_items: list[str] = []
    ordered_items: list[str] = []
    code_lines: list[str] = []
    table_lines: list[str] = []
    in_code = False

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        if paragraph_lines:
            text = " ".join(line.strip() for line in paragraph_lines if line.strip())
            html_parts.append(f"<p>{_markdown_inline_to_html(text)}</p>")
            paragraph_lines = []

    def flush_list() -> None:
        nonlocal list_items
        if list_items:
            html_parts.append("<ul>" + "".join(f"<li>{item}</li>" for item in list_items) + "</ul>")
            list_items = []

    def flush_ordered_list() -> None:
        nonlocal ordered_items
        if ordered_items:
            html_parts.append("<ol>" + "".join(f"<li>{item}</li>" for item in ordered_items) + "</ol>")
            ordered_items = []

    def flush_code() -> None:
        nonlocal code_lines
        if code_lines:
            code_html = html.escape("\n".join(code_lines))
            html_parts.append(f"<pre><code>{code_html}</code></pre>")
            code_lines = []

    def flush_table() -> None:
        nonlocal table_lines
        if table_lines:
            html_parts.append(_render_markdown_table(table_lines))
            table_lines = []

    for raw_line in lines:
        line = raw_line.rstrip("\n")
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            flush_list()
            flush_ordered_list()
            flush_table()
            if in_code:
                flush_code()
                in_code = False
            else:
                in_code = True
                code_lines = []
            continue

        if in_code:
            code_lines.append(line)
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph()
            flush_list()
            flush_ordered_list()
            table_lines.append(stripped)
            continue
        if table_lines:
            flush_table()

        if not stripped:
            flush_paragraph()
            flush_list()
            flush_ordered_list()
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading_match:
            flush_paragraph()
            flush_list()
            flush_ordered_list()
            level = len(heading_match.group(1))
            content = _markdown_inline_to_html(heading_match.group(2))
            html_parts.append(f"<h{level}>{content}</h{level}>")
            continue

        list_match = re.match(r"^[-*]\s+(.*)$", stripped)
        if list_match:
            flush_paragraph()
            flush_ordered_list()
            list_items.append(_markdown_inline_to_html(list_match.group(1)))
            continue

        ordered_match = re.match(r"^\d+\.\s+(.*)$", stripped)
        if ordered_match:
            flush_paragraph()
            flush_list()
            ordered_items.append(_markdown_inline_to_html(ordered_match.group(1)))
            continue

        paragraph_lines.append(stripped)

    flush_paragraph()
    flush_list()
    flush_ordered_list()
    flush_table()
    flush_code()
    return "\n".join(part for part in html_parts if part)


def _serialize_for_display(value: Any) -> str:
    if value in (None, "", []):
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, indent=2, sort_keys=False)


def _build_sample_value_block(title: str, value: Any, empty_text: str) -> str:
    display = _serialize_for_display(value)
    if not display:
        return (
            f'<details><summary>{html.escape(title)}</summary>'
            f'<div class="sample-empty">{html.escape(empty_text)}</div>'
            "</details>"
        )
    return (
        f'<details><summary>{html.escape(title)}</summary>'
        f"<pre><code>{html.escape(display)}</code></pre>"
        "</details>"
    )


def _render_detail_page_html(entry: dict[str, Any]) -> str:
    sample_cards: list[str] = []
    for sample in entry.get("sample_images", []):
        sample_title = html.escape(sample.get("title") or sample["filename"])
        sample_target_id = f"sample-main-{html.escape(sample['sample_id'])}"
        thumbnails_html = ""
        if sample.get("exists"):
            thumb_specs = [
                ("Iso", sample.get("detail_iso_120_path"), sample.get("detail_iso_400_path")),
                ("Top", sample.get("detail_top_120_path"), sample.get("detail_top_400_path")),
                ("Side", sample.get("detail_side_120_path"), sample.get("detail_side_400_path")),
            ]
            thumb_buttons: list[str] = []
            for label, thumb_src, full_src in thumb_specs:
                if not thumb_src or not full_src:
                    continue
                thumb_buttons.append(
                    '<button class="sample-thumb" type="button" '
                    f'data-target="{sample_target_id}" '
                    f'data-full="{html.escape(full_src)}" '
                    f'data-alt="{sample_title} {html.escape(label.lower())} view">'
                    f'<img src="{html.escape(thumb_src)}" alt="{sample_title} {html.escape(label.lower())} thumbnail">'
                    f'<span>{html.escape(label)}</span>'
                    "</button>"
                )
            if thumb_buttons:
                thumbnails_html = f'<div class="sample-thumbs">{"".join(thumb_buttons)}</div>'
        image_html = (
            f'<img id="{sample_target_id}" src="{html.escape(sample["detail_image_path"])}" '
            f'alt="{sample_title}">'
            if sample.get("exists")
            else '<div class="sample-missing">Image not generated yet</div>'
        )

        meta_lines = []
        meta_lines.append(
            f'<div class="sample-link-row"><a class="sample-link" href="{html.escape(sample["detail_scad_path"])}" download>Download SCAD</a></div>'
            if sample.get("scad_exists")
            else '<div class="sample-link-row"><span class="sample-link-disabled">SCAD not generated yet</span></div>'
        )
        meta_lines.append(
            _build_sample_value_block(
                "Set Values",
                sample.get("set_values"),
                "No explicit sample values documented.",
            )
        )
        meta_lines.append(
            _build_sample_value_block(
                "Default Values",
                sample.get("default_values"),
                "No documented defaults for this component.",
            )
        )
        if sample.get("helper_kwargs"):
            meta_lines.append(
                _build_sample_value_block(
                    "Helper Kwargs",
                    sample.get("helper_kwargs"),
                    "No helper kwargs for this sample.",
                )
            )
        if sample.get("companion_geometry_kwargs"):
            meta_lines.append(
                _build_sample_value_block(
                    "Companion Geometry Kwargs",
                    sample.get("companion_geometry_kwargs"),
                    "No companion geometry kwargs for this sample.",
                )
            )
        if sample.get("implementation_rule"):
            meta_lines.append(
                f"<div><strong>rule:</strong> {html.escape(sample['implementation_rule'])}</div>"
            )

        sample_cards.append(
            """
            <article class="sample-card">
              <div class="sample-image-wrap">{image_html}</div>
              {thumbnails_html}
              <div class="sample-body">
                <h3>{title}</h3>
                <p>{intent}</p>
                {meta}
              </div>
            </article>
            """.format(
                image_html=image_html,
                thumbnails_html=thumbnails_html,
                title=sample_title,
                intent=html.escape(sample.get("intent") or "No caption available yet."),
                meta="".join(meta_lines),
            )
        )

    variables = entry.get("variables", [])
    variable_rows = "".join(
        "<tr>"
        f"<td><code>{html.escape(variable['name'])}</code></td>"
        f"<td>{html.escape(_coerce_text(variable.get('description')) or '-')}</td>"
        f"<td>{html.escape(_coerce_text(variable.get('type')) or '-')}</td>"
        f"<td><code>{html.escape(_coerce_text(variable.get('default')) or '-')}</code></td>"
        "</tr>"
        for variable in variables
    )
    if not variable_rows:
        variable_rows = '<tr><td colspan="4">No variables documented.</td></tr>'

    alias_text = ", ".join(entry.get("aliases", [])) or "None"
    detail_section = ""
    if entry.get("detail_html"):
        detail_section = (
            '<section class="panel">'
            '<h2>More Details</h2>'
            f"{entry['detail_html']}"
            "</section>"
        )

    samples_section = ""
    if sample_cards:
        samples_section = (
            '<section class="panel">'
            '<h2>Sample Images</h2>'
            f'<p class="panel-intro">{html.escape(entry.get("sample_notes") or "Representative sample renders for this component.")}</p>'
            f'<div class="sample-grid">{"".join(sample_cards)}</div>'
            "</section>"
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(entry['command'])} Documentation</title>
  <style>
    :root {{
      --bg: #f7f5ff;
      --panel: rgba(255,255,255,0.92);
      --border: #ddd5ff;
      --text: #2f2850;
      --subtle: #635c7e;
      --accent: #7b68ee;
      --accent-soft: #efeaff;
      --shadow: 0 14px 40px rgba(78, 58, 140, 0.12);
      --radius: 22px;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, "Segoe UI", sans-serif;
      background: radial-gradient(circle at top left, #fff9ef, var(--bg) 45%, #eef6ff 100%);
      color: var(--text);
    }}
    .page {{
      max-width: 1080px;
      margin: 0 auto;
      padding: 28px 18px 40px;
    }}
    .hero {{
      background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(244,240,255,0.92));
      border: 1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      padding: 28px;
      margin-bottom: 22px;
    }}
    .eyebrow {{
      display: inline-flex;
      gap: 10px;
      align-items: center;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 10px;
    }}
    h1 {{
      margin: 0 0 6px;
      font-size: 34px;
      line-height: 1.1;
    }}
    .name-long {{
      color: var(--subtle);
      font-size: 15px;
      margin-bottom: 16px;
    }}
    .hero p {{
      margin: 0;
      line-height: 1.7;
      color: var(--subtle);
      font-size: 16px;
    }}
    .meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 18px;
    }}
    .meta-chip {{
      background: var(--accent-soft);
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 8px 12px;
      font-size: 13px;
    }}
    .panel {{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      padding: 24px;
      margin-bottom: 20px;
    }}
    .panel h2 {{
      margin: 0 0 14px;
      font-size: 22px;
    }}
    .panel-intro {{
      margin: 0 0 18px;
      color: var(--subtle);
      line-height: 1.6;
    }}
    .sample-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 18px;
    }}
    .sample-card {{
      border: 1px solid var(--border);
      border-radius: 18px;
      overflow: hidden;
      background: rgba(255,255,255,0.82);
    }}
    .sample-image-wrap {{
      background: linear-gradient(180deg, #faf7ff, #f1ebff);
      min-height: 220px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 14px;
    }}
    .sample-image-wrap img {{
      width: 100%;
      height: auto;
      border-radius: 12px;
      object-fit: contain;
      box-shadow: 0 10px 28px rgba(74, 52, 112, 0.14);
    }}
    .sample-missing {{
      color: var(--subtle);
      font-size: 14px;
      padding: 24px;
      text-align: center;
    }}
    .sample-body {{
      padding: 16px;
      color: var(--subtle);
      line-height: 1.6;
      font-size: 14px;
    }}
    .sample-body h3 {{
      margin: 0 0 8px;
      font-size: 18px;
      color: var(--text);
    }}
    .sample-body p {{
      margin: 0 0 12px;
    }}
    .sample-link-row {{
      margin-bottom: 10px;
    }}
    .sample-link {{
      display: inline-flex;
      align-items: center;
      border-radius: 999px;
      background: #efe8ff;
      color: #4f3ca7;
      text-decoration: none;
      font-weight: 700;
      padding: 8px 12px;
      border: 1px solid #d6c7ff;
    }}
    .sample-link-disabled {{
      display: inline-flex;
      align-items: center;
      border-radius: 999px;
      background: #f3f1f8;
      color: var(--subtle);
      font-weight: 700;
      padding: 8px 12px;
      border: 1px solid var(--border);
    }}
    .sample-thumbs {{
      display: flex;
      gap: 10px;
      padding: 0 14px 12px;
      flex-wrap: wrap;
    }}
    .sample-thumb {{
      border: 1px solid var(--border);
      background: #faf8ff;
      border-radius: 12px;
      padding: 4px;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
      color: var(--subtle);
      font-size: 12px;
    }}
    .sample-thumb img {{
      display: block;
      width: 120px;
      height: 120px;
      object-fit: contain;
      border-radius: 8px;
    }}
    details {{
      margin-top: 10px;
      background: #faf8ff;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 10px 12px;
    }}
    summary {{
      cursor: pointer;
      font-weight: 600;
      color: var(--text);
    }}
    .sample-empty {{
      margin-top: 10px;
      color: var(--subtle);
      line-height: 1.6;
    }}
    pre {{
      margin: 10px 0 0;
      white-space: pre-wrap;
      word-break: break-word;
      background: #261f45;
      color: #f7f4ff;
      padding: 14px;
      border-radius: 14px;
      overflow: auto;
    }}
    code {{
      font-family: Consolas, "Courier New", monospace;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
    }}
    th, td {{
      text-align: left;
      padding: 12px 10px;
      border-bottom: 1px solid var(--border);
      vertical-align: top;
    }}
    th {{
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--subtle);
    }}
    .markdown-table-wrap {{
      overflow-x: auto;
    }}
    .markdown-table {{
      margin-top: 12px;
    }}
    p, ul, ol {{
      line-height: 1.7;
      color: var(--subtle);
    }}
    h3, h4 {{
      margin-top: 1.2em;
      color: var(--text);
    }}
    @media (max-width: 720px) {{
      .page {{ padding: 14px; }}
      .hero, .panel {{ padding: 18px; border-radius: 18px; }}
      h1 {{ font-size: 28px; }}
      .sample-image-wrap {{ min-height: 180px; }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <section class="hero">
      <div class="eyebrow">Component Detail</div>
      <h1>{html.escape(entry['command'])}</h1>
      <div class="name-long">{html.escape(entry.get('name_long', ''))}</div>
      <p>{html.escape(entry.get('description') or entry.get('summary') or 'No description available.')}</p>
      <div class="meta">
        <div class="meta-chip"><strong>Category:</strong> {html.escape(entry.get('category', 'General'))}</div>
        <div class="meta-chip"><strong>Returns:</strong> {html.escape(entry.get('returns', '') or 'Not specified')}</div>
        <div class="meta-chip"><strong>Aliases:</strong> {html.escape(alias_text)}</div>
      </div>
    </section>

    {samples_section}

    <section class="panel">
      <h2>Variables</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Type</th>
            <th>Default</th>
          </tr>
        </thead>
        <tbody>
          {variable_rows}
        </tbody>
      </table>
    </section>

    {detail_section}
  </main>
  <script>
    document.querySelectorAll('.sample-thumb').forEach((button) => {{
      button.addEventListener('click', () => {{
        const targetId = button.getAttribute('data-target');
        const fullSrc = button.getAttribute('data-full');
        const altText = button.getAttribute('data-alt');
        const target = document.getElementById(targetId);
        if (!target || !fullSrc) return;
        target.src = fullSrc;
        if (altText) {{
          target.alt = altText;
        }}
      }});
    }});
  </script>
</body>
</html>
"""


def _augment_doc_entry(command: str, metadata: dict[str, Any], folder: Path | None) -> dict[str, Any]:
    name_long = _coerce_text(metadata.get("name_long") or metadata.get("name") or command)
    description = _coerce_text(metadata.get("description"))
    category = _coerce_text(metadata.get("category") or "General")
    returns_text = _coerce_text(metadata.get("returns"))
    name_short = metadata.get("name_short")

    if isinstance(name_short, str):
        aliases = [name_short.strip()] if name_short.strip() else []
    elif isinstance(name_short, list):
        aliases = [item.strip() for item in name_short if isinstance(item, str) and item.strip()]
    else:
        aliases = []

    variables = _normalize_variables(metadata.get("variables", []))
    variable_names = [item["name"] for item in variables]
    summary = _build_summary(description, variable_names, returns_text)
    default_values = _build_default_values(variables)

    entry: dict[str, Any] = {
        "command": command,
        "name_long": name_long,
        "name_short_options": aliases,
        "description": description,
        "summary": summary,
        "variables": variables,
        "variable_names": variable_names,
        "category": category,
        "returns": returns_text,
        "aliases": aliases,
        "detail_page": "",
        "detail_markdown": "",
        "detail_html": "",
        "sample_images": [],
        "sample_notes": "",
        "has_test_images": False,
        "has_detail_page": False,
        "default_values": default_values,
    }

    if folder is None:
        return entry

    readme_path = folder / "README.md"
    test_samples_path = folder / "TEST_SAMPLES.md"
    component_name = folder.name

    test_sample_doc = _parse_test_samples(test_samples_path, component_name)
    sample_images = _collect_sample_images(folder, component_name, test_sample_doc, variables)
    readme_markdown = _read_text_if_exists(readme_path)
    detail_markdown = readme_markdown
    detail_html = _markdown_to_html(detail_markdown) if detail_markdown else ""

    entry.update(
        {
            "readme_path": f"{component_name}/README.md",
            "test_samples_path": f"{component_name}/TEST_SAMPLES.md" if test_samples_path.exists() else "",
            "detail_page": f"{component_name}/documentation_detail.html",
            "detail_markdown": detail_markdown,
            "detail_html": detail_html,
            "sample_images": sample_images,
            "sample_notes": test_sample_doc.get("notes", ""),
            "has_test_images": any(sample.get("exists") for sample in sample_images),
            "has_detail_page": True,
        }
    )
    return entry


def get_all_objects_documentation(objects_root: str | Path | None = None) -> list[dict[str, Any]]:
    discovered = discover_objects(objects_root=objects_root)
    docs: list[dict[str, Any]] = []
    for object_name in sorted(discovered.keys()):
        discovered_object = discovered[object_name]
        docs.append(_augment_doc_entry(object_name, discovered_object.metadata, discovered_object.path.parent))
    return docs


def get_all_part_sets_documentation(sets_root: str | Path | None = None) -> list[dict[str, Any]]:
    discovered = discover_part_sets(sets_root=sets_root)
    docs: list[dict[str, Any]] = []
    for set_name in sorted(discovered.keys()):
        discovered_set = discovered[set_name]
        docs.append(_augment_doc_entry(set_name, discovered_set.metadata, discovered_set.path.parent))
    return docs


def _build_documentation_payload(
    objects_root: str | Path | None = None,
    sets_root: str | Path | None = None,
) -> dict[str, Any]:
    objects = get_all_objects_documentation(objects_root=objects_root)
    part_sets = get_all_part_sets_documentation(sets_root=sets_root)
    return {
        "objects": objects,
        "part_sets": part_sets,
        "variable_catalog": _build_variable_catalog(),
        "generated_date": str(date.today()),
        "total_objects": len(objects),
        "total_part_sets": len(part_sets),
    }


def _serialize_catalog_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, sort_keys=False)


def _build_variable_catalog() -> list[dict[str, Any]]:
    raw_variables = getattr(oobb, "variables", {}) or {}
    if not isinstance(raw_variables, dict):
        return []

    modes = ("laser", "true", "3dpr")
    grouped: dict[str, dict[str, Any]] = {}

    for name in sorted(raw_variables.keys()):
        base_name = name
        mode_name = ""
        for mode in modes:
            suffix = f"_{mode}"
            if name.endswith(suffix):
                base_name = name[: -len(suffix)]
                mode_name = mode
                break

        entry = grouped.setdefault(
            base_name,
            {
                "name": base_name,
                "value": "",
                "modes": {},
                "has_mode_values": False,
            },
        )

        serialized = _serialize_catalog_value(raw_variables[name])
        if mode_name:
            entry["modes"][mode_name] = serialized
            entry["has_mode_values"] = True
        else:
            entry["value"] = serialized

    catalog: list[dict[str, Any]] = []
    for _, entry in sorted(grouped.items(), key=lambda item: item[0]):
        if entry["has_mode_values"] and not entry["value"]:
            mode_values = entry["modes"]
            ordered_values = [mode_values.get(mode, "") for mode in modes if mode in mode_values]
            if ordered_values and all(value == ordered_values[0] for value in ordered_values):
                entry["value"] = ordered_values[0]
        catalog.append(entry)

    return catalog


def export_documentation_json(
    output_file: str | Path,
    objects_root: str | Path | None = None,
    sets_root: str | Path | None = None,
):
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = _build_documentation_payload(objects_root=objects_root, sets_root=sets_root)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def export_component_detail_pages(
    objects_root: str | Path | None = None,
    sets_root: str | Path | None = None,
):
    objects_map = discover_objects(objects_root=objects_root)
    for name in sorted(objects_map.keys()):
        item = objects_map[name]
        entry = _augment_doc_entry(name, item.metadata, item.path.parent)
        detail_markdown = entry.get("detail_markdown", "")
        if not detail_markdown:
            entry["detail_markdown"] = _build_default_detail_markdown(entry)
            entry["detail_html"] = _markdown_to_html(entry["detail_markdown"])
        detail_html = _render_detail_page_html(entry)
        (item.path.parent / "documentation_detail.html").write_text(detail_html, encoding="utf-8")

    sets_map = discover_part_sets(sets_root=sets_root)
    for name in sorted(sets_map.keys()):
        item = sets_map[name]
        entry = _augment_doc_entry(name, item.metadata, item.path.parent)
        detail_markdown = entry.get("detail_markdown", "")
        if not detail_markdown:
            entry["detail_markdown"] = _build_default_detail_markdown(entry)
            entry["detail_html"] = _markdown_to_html(entry["detail_markdown"])
        detail_html = _render_detail_page_html(entry)
        (item.path.parent / "documentation_detail.html").write_text(detail_html, encoding="utf-8")


def export_documentation_html(
    template_file: str | Path,
    output_file: str | Path,
    objects_root: str | Path | None = None,
    sets_root: str | Path | None = None,
):
    template_path = Path(template_file)
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload = _build_documentation_payload(objects_root=objects_root, sets_root=sets_root)
    template_content = template_path.read_text(encoding="utf-8")

    placeholder = "<!-- DOCUMENTATION_DATA_PLACEHOLDER -->"
    if placeholder in template_content:
        data_block = f"window.DOCUMENTATION_DATA = {json.dumps(payload)};"
        html_content = template_content.replace(placeholder, data_block)
    else:
        data_block = f"<script>window.DOCUMENTATION_DATA = {json.dumps(payload)};</script>"
        html_content = template_content + "\n" + data_block

    output_path.write_text(html_content, encoding="utf-8")
    export_component_detail_pages(objects_root=objects_root, sets_root=sets_root)


def _write_entity_readme(folder: Path, entry: dict[str, Any]):
    readme_path = folder / "README.md"
    if readme_path.exists():
        return

    content = _build_default_detail_markdown(entry)
    readme_path.write_text(content + "\n", encoding="utf-8")


def _write_index_readme(root: Path, title: str, entries: list[dict[str, Any]]):
    lines = [
        f"# {title}",
        "",
        "| Name | Description | Category |",
        "|------|-------------|----------|",
    ]
    for entry in entries:
        lines.append(
            f"| [{entry['command']}]({entry['command']}/) | {entry.get('description', '')} | {entry.get('category', 'General')} |"
        )
    lines.append("")
    (root / "README.md").write_text("\n".join(lines), encoding="utf-8")


def export_documentation_markdown(
    objects_root: str | Path | None = None,
    sets_root: str | Path | None = None,
):
    objects_map = discover_objects(objects_root=objects_root)
    sets_map = discover_part_sets(sets_root=sets_root)

    if not objects_map and not sets_map:
        return

    objects_base = Path(objects_root).resolve() if objects_root is not None else None
    sets_base = Path(sets_root).resolve() if sets_root is not None else None

    object_entries: list[dict[str, Any]] = []
    for name in sorted(objects_map.keys()):
        item = objects_map[name]
        entry = _augment_doc_entry(name, item.metadata, item.path.parent)
        object_entries.append(entry)
        _write_entity_readme(item.path.parent, entry)
        if objects_base is None:
            objects_base = item.path.parent.parent

    set_entries: list[dict[str, Any]] = []
    for name in sorted(sets_map.keys()):
        item = sets_map[name]
        entry = _augment_doc_entry(name, item.metadata, item.path.parent)
        set_entries.append(entry)
        _write_entity_readme(item.path.parent, entry)
        if sets_base is None:
            sets_base = item.path.parent.parent

    if objects_base is not None:
        _write_index_readme(objects_base, "OOBB Objects", object_entries)
    if sets_base is not None:
        _write_index_readme(sets_base, "OOBB Part Sets", set_entries)


def cli() -> int:
    parser = argparse.ArgumentParser(description="OOBB Documentation Generator")
    parser.add_argument("--json", default="", help="Output path for JSON documentation")
    parser.add_argument("--html-template", default="", help="Path to HTML template file")
    parser.add_argument("--html-output", default="", help="Output path for HTML documentation")
    parser.add_argument("--markdown", action="store_true", help="Generate Markdown README files")
    parser.add_argument("--detail-pages", action="store_true", help="Generate standalone component detail pages")
    parser.add_argument("--objects-root", default=None)
    parser.add_argument("--sets-root", default=None)
    args = parser.parse_args()

    if args.json:
        export_documentation_json(args.json, objects_root=args.objects_root, sets_root=args.sets_root)
    if args.html_template and args.html_output:
        export_documentation_html(
            args.html_template,
            args.html_output,
            objects_root=args.objects_root,
            sets_root=args.sets_root,
        )
    elif args.detail_pages:
        export_component_detail_pages(objects_root=args.objects_root, sets_root=args.sets_root)
    if args.markdown:
        export_documentation_markdown(objects_root=args.objects_root, sets_root=args.sets_root)

    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
