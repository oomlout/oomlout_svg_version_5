# Action Migration Inventory

- Canonical action rows: 56
- Source of truth: `old/oomlout_ai_roboclick.py` decorators
- Count note: file contains 57 decorated commands; `continue_chat` is treated as a retired alias to `ai_continue_chat` and moved to alias map below.
- Naming style: `roboclick_action_<verbose_command_name>`

## Canonical Inventory (56)

| Command | Old Function | Source | New Verbose ID | Category | Target Folder | name_long (proposed) | name_short options (proposed) | Notes | TODO |
|---|---|---|---|---|---|---|---|---|---|
| ai_add_image | ai_add_image | old/oomlout_ai_roboclick.py:381 | roboclick_action_ai_add_image | AI | actions/roboclick_action_ai_add_image/working.py | RoboClick Action: AI Add Image | ai_add_image, add_image | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| ai_add_file | ai_add_file | old/oomlout_ai_roboclick.py:434 | roboclick_action_ai_add_file | AI | actions/roboclick_action_ai_add_file/working.py | RoboClick Action: AI Add File | ai_add_file, add_file | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| ai_continue_chat | ai_continue_chat | old/oomlout_ai_roboclick.py:441 | roboclick_action_ai_continue_chat | AI | actions/roboclick_action_ai_continue_chat/working.py | RoboClick Action: AI Continue Chat | ai_continue_chat, continue_chat | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| ai_fix_yaml_copy_paste | ai_fix_yaml_copy_paste | old/oomlout_ai_roboclick.py:487 | roboclick_action_ai_fix_yaml_copy_paste | AI | actions/roboclick_action_ai_fix_yaml_copy_paste/working.py | RoboClick Action: AI Fix Yaml Copy Paste | ai_fix_yaml_copy_paste, fix_yaml_copy_paste | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| ai_new_chat | ai_new_chat | old/oomlout_ai_roboclick.py:564 | roboclick_action_ai_new_chat | AI | actions/roboclick_action_ai_new_chat/working.py | RoboClick Action: AI New Chat | ai_new_chat, new_chat | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| ai_query | ai_query | old/oomlout_ai_roboclick.py:621 | roboclick_action_ai_query | AI | actions/roboclick_action_ai_query/working.py | RoboClick Action: AI Query | ai_query, query | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| ai_save_text | ai_save_text | old/oomlout_ai_roboclick.py:680 | roboclick_action_ai_save_text | AI | actions/roboclick_action_ai_save_text/working.py | RoboClick Action: AI Save Text | ai_save_text, save_text | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| ai_set_mode | ai_set_mode | old/oomlout_ai_roboclick.py:720 | roboclick_action_ai_set_mode | AI | actions/roboclick_action_ai_set_mode/working.py | RoboClick Action: AI Set Mode | ai_set_mode, set_mode | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| ai_skill_image_prompt_full | ai_skill_image_prompt_full | old/oomlout_ai_roboclick.py:742 | roboclick_action_ai_skill_image_prompt_full | AI Skill | actions/roboclick_action_ai_skill_image_prompt_full/working.py | RoboClick Action: AI Skill Image Prompt Full | ai_skill_image_prompt_full, image_prompt_full | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| ai_skill_image_laser_cut_logo_full | ai_skill_image_laser_cut_logo_full | old/oomlout_ai_roboclick.py:750 | roboclick_action_ai_skill_image_laser_cut_logo_full | AI Skill | actions/roboclick_action_ai_skill_image_laser_cut_logo_full/working.py | RoboClick Action: AI Skill Image Laser Cut Logo Full | ai_skill_image_laser_cut_logo_full, image_laser_cut_logo_full | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| ai_skill_text_to_speech | ai_skill_text_to_speech | old/oomlout_ai_roboclick.py:757 | roboclick_action_ai_skill_text_to_speech | AI Skill | actions/roboclick_action_ai_skill_text_to_speech/working.py | RoboClick Action: AI Skill Text To Speech | ai_skill_text_to_speech, text_to_speech | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| ai_skill_validate_json | ai_skill_validate_json | old/oomlout_ai_roboclick.py:775 | roboclick_action_ai_skill_validate_json | AI Skill | actions/roboclick_action_ai_skill_validate_json/working.py | RoboClick Action: AI Skill Validate Json | ai_skill_validate_json, validate_json | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| browser_close_tab | browser_close_tab | old/oomlout_ai_roboclick.py:874 | roboclick_action_browser_close_tab | Browser | actions/roboclick_action_browser_close_tab/working.py | RoboClick Action: Browser Close Tab | browser_close_tab, close_tab | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| browser_open_url | browser_open_url | old/oomlout_ai_roboclick.py:883 | roboclick_action_browser_open_url | Browser | actions/roboclick_action_browser_open_url/working.py | RoboClick Action: Browser Open Url | browser_open_url, open_url | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| browser_save_url | browser_save_url | old/oomlout_ai_roboclick.py:891 | roboclick_action_browser_save_url | Browser | actions/roboclick_action_browser_save_url/working.py | RoboClick Action: Browser Save Url | browser_save_url, save_url | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| convert_svg_to_pdf | convert_svg_to_pdf | old/oomlout_ai_roboclick.py:912 | roboclick_action_convert_svg_to_pdf | Conversion | actions/roboclick_action_convert_svg_to_pdf/working.py | RoboClick Action: Convert Svg To Pdf | convert_svg_to_pdf, svg_to_pdf | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| convert_svg_to_png | convert_svg_to_png | old/oomlout_ai_roboclick.py:929 | roboclick_action_convert_svg_to_png | Conversion | actions/roboclick_action_convert_svg_to_png/working.py | RoboClick Action: Convert Svg To Png | convert_svg_to_png, svg_to_png | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| corel_add_text | corel_add_text | old/oomlout_ai_roboclick.py:951 | roboclick_action_corel_add_text | CorelDRAW | actions/roboclick_action_corel_add_text/working.py | RoboClick Action: Corel Add Text | corel_add_text, add_text | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| corel_add_text_box | corel_add_text_box | old/oomlout_ai_roboclick.py:981 | roboclick_action_corel_add_text_box | CorelDRAW | actions/roboclick_action_corel_add_text_box/working.py | RoboClick Action: Corel Add Text Box | corel_add_text_box, add_text_box | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| corel_close_file | corel_close_file | old/oomlout_ai_roboclick.py:1015 | roboclick_action_corel_close_file | CorelDRAW | actions/roboclick_action_corel_close_file/working.py | RoboClick Action: Corel Close File | corel_close_file, close_file | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| corel_convert_to_curves | corel_convert_to_curves | old/oomlout_ai_roboclick.py:1023 | roboclick_action_corel_convert_to_curves | CorelDRAW | actions/roboclick_action_corel_convert_to_curves/working.py | RoboClick Action: Corel Convert To Curves | corel_convert_to_curves, convert_to_curves | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| corel_copy | corel_copy | old/oomlout_ai_roboclick.py:1038 | roboclick_action_corel_copy | CorelDRAW | actions/roboclick_action_corel_copy/working.py | RoboClick Action: Corel Copy | corel_copy, copy | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| corel_export | corel_export | old/oomlout_ai_roboclick.py:1047 | roboclick_action_corel_export | CorelDRAW | actions/roboclick_action_corel_export/working.py | RoboClick Action: Corel Export | corel_export, export | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| corel_group | corel_group | old/oomlout_ai_roboclick.py:1067 | roboclick_action_corel_group | CorelDRAW | actions/roboclick_action_corel_group/working.py | RoboClick Action: Corel Group | corel_group, group | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| corel_import | corel_import | old/oomlout_ai_roboclick.py:1075 | roboclick_action_corel_import | CorelDRAW | actions/roboclick_action_corel_import/working.py | RoboClick Action: Corel Import | corel_import, import | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| corel_object_order | corel_object_order | old/oomlout_ai_roboclick.py:1110 | roboclick_action_corel_object_order | CorelDRAW | actions/roboclick_action_corel_object_order/working.py | RoboClick Action: Corel Object Order | corel_object_order, object_order | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| corel_open | corel_open | old/oomlout_ai_roboclick.py:1121 | roboclick_action_corel_open | CorelDRAW | actions/roboclick_action_corel_open/working.py | RoboClick Action: Corel Open | corel_open, open | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| corel_page_goto | corel_page_goto | old/oomlout_ai_roboclick.py:1134 | roboclick_action_corel_page_goto | CorelDRAW | actions/roboclick_action_corel_page_goto/working.py | RoboClick Action: Corel Page Goto | corel_page_goto, page_goto | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| corel_paste | corel_paste | old/oomlout_ai_roboclick.py:1145 | roboclick_action_corel_paste | CorelDRAW | actions/roboclick_action_corel_paste/working.py | RoboClick Action: Corel Paste | corel_paste, paste | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| corel_save | corel_save | old/oomlout_ai_roboclick.py:1168 | roboclick_action_corel_save | CorelDRAW | actions/roboclick_action_corel_save/working.py | RoboClick Action: Corel Save | corel_save, save | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| corel_save_as | corel_save_as | old/oomlout_ai_roboclick.py:1177 | roboclick_action_corel_save_as | CorelDRAW | actions/roboclick_action_corel_save_as/working.py | RoboClick Action: Corel Save As | corel_save_as, save_as | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| corel_set_position | corel_set_position | old/oomlout_ai_roboclick.py:1192 | roboclick_action_corel_set_position | CorelDRAW | actions/roboclick_action_corel_set_position/working.py | RoboClick Action: Corel Set Position | corel_set_position, set_position | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| corel_set_rotation | corel_set_rotation | old/oomlout_ai_roboclick.py:1207 | roboclick_action_corel_set_rotation | CorelDRAW | actions/roboclick_action_corel_set_rotation/working.py | RoboClick Action: Corel Set Rotation | corel_set_rotation, set_rotation | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| corel_set_size | corel_set_size | old/oomlout_ai_roboclick.py:1219 | roboclick_action_corel_set_size | CorelDRAW | actions/roboclick_action_corel_set_size/working.py | RoboClick Action: Corel Set Size | corel_set_size, set_size | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| corel_trace | corel_trace | old/oomlout_ai_roboclick.py:1238 | roboclick_action_corel_trace | CorelDRAW | actions/roboclick_action_corel_trace/working.py | RoboClick Action: Corel Trace | corel_trace, trace | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| corel_trace_full | corel_trace_full | old/oomlout_ai_roboclick.py:1273 | roboclick_action_corel_trace_full | CorelDRAW | actions/roboclick_action_corel_trace_full/working.py | RoboClick Action: Corel Trace Full | corel_trace_full, trace_full | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| file_copy | file_copy | old/oomlout_ai_roboclick.py:1402 | roboclick_action_file_copy | File | actions/roboclick_action_file_copy/working.py | RoboClick Action: File Copy | file_copy, copy | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| file_create_text_file | file_create_text_file | old/oomlout_ai_roboclick.py:1429 | roboclick_action_file_create_text_file | File | actions/roboclick_action_file_create_text_file/working.py | RoboClick Action: File Create Text File | file_create_text_file, create_text_file | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| google_doc_new | google_doc_new | old/oomlout_ai_roboclick.py:1447 | roboclick_action_google_doc_new | Google Doc | actions/roboclick_action_google_doc_new/working.py | RoboClick Action: Google Doc New | google_doc_new, new | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| google_doc_add_text | google_doc_add_text | old/oomlout_ai_roboclick.py:1482 | roboclick_action_google_doc_add_text | Google Doc | actions/roboclick_action_google_doc_add_text/working.py | RoboClick Action: Google Doc Add Text | google_doc_add_text, add_text | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| image_crop | image_crop | old/oomlout_ai_roboclick.py:1512 | roboclick_action_image_crop | Image | actions/roboclick_action_image_crop/working.py | RoboClick Action: Image Crop | image_crop, crop | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| image_png_transparent_to_white | image_png_transparent_to_white | old/oomlout_ai_roboclick.py:1607 | roboclick_action_image_png_transparent_to_white | Image | actions/roboclick_action_image_png_transparent_to_white/working.py | RoboClick Action: Image Png Transparent To White | image_png_transparent_to_white, png_transparent_to_white | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| image_quad_swap_for_tile | image_quad_swap_for_tile | old/oomlout_ai_roboclick.py:1649 | roboclick_action_image_quad_swap_for_tile | Image | actions/roboclick_action_image_quad_swap_for_tile/working.py | RoboClick Action: Image Quad Swap For Tile | image_quad_swap_for_tile, quad_swap_for_tile | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| image_upscale | image_upscale | old/oomlout_ai_roboclick.py:1698 | roboclick_action_image_upscale | Image | actions/roboclick_action_image_upscale/working.py | RoboClick Action: Image Upscale | image_upscale, upscale | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| add_image | add_image | old/oomlout_ai_roboclick.py:1748 | roboclick_action_alias_add_image | Legacy Alias | actions/roboclick_action_alias_add_image/working.py | RoboClick Action: Add Image | add_image, legacy_alias | Alias wrapper; delegate to canonical command | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| add_file | add_file | old/oomlout_ai_roboclick.py:1753 | roboclick_action_alias_add_file | Legacy Alias | actions/roboclick_action_alias_add_file/working.py | RoboClick Action: Add File | add_file, legacy_alias | Alias wrapper; delegate to canonical command | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| close_tab | close_tab | old/oomlout_ai_roboclick.py:1758 | roboclick_action_alias_close_tab | Legacy Alias | actions/roboclick_action_alias_close_tab/working.py | RoboClick Action: Close Tab | close_tab, legacy_alias | Alias wrapper; delegate to canonical command | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| new_chat | new_chat | old/oomlout_ai_roboclick.py:1763 | roboclick_action_alias_new_chat | Legacy Alias | actions/roboclick_action_alias_new_chat/working.py | RoboClick Action: New Chat | new_chat, legacy_alias | Alias wrapper; delegate to canonical command | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| query | query | old/oomlout_ai_roboclick.py:1768 | roboclick_action_alias_query | Legacy Alias | actions/roboclick_action_alias_query/working.py | RoboClick Action: Query | query, legacy_alias | Alias wrapper; delegate to canonical command | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| ai_save_image | ai_save_image | old/oomlout_ai_roboclick.py:1773 | roboclick_action_alias_ai_save_image | Legacy Alias | actions/roboclick_action_alias_ai_save_image/working.py | RoboClick Action: AI Save Image | ai_save_image, save_image, legacy_alias | Alias wrapper; delegate to canonical command | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| openscad_render_file | openscad_render_file | old/oomlout_ai_roboclick.py:1778 | roboclick_action_alias_openscad_render_file | Legacy Alias | actions/roboclick_action_alias_openscad_render_file/working.py | RoboClick Action: OpenSCAD Render File | openscad_render_file, render_file, legacy_alias | Alias wrapper; delegate to canonical command | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| save_image_generated | save_image_generated | old/oomlout_ai_roboclick.py:1790 | roboclick_action_save_image_generated | AI Image | actions/roboclick_action_save_image_generated/working.py | RoboClick Action: Save Image Generated | save_image_generated | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| save_image_search_result | save_image_search_result | old/oomlout_ai_roboclick.py:1796 | roboclick_action_save_image_search_result | AI Image | actions/roboclick_action_save_image_search_result/working.py | RoboClick Action: Save Image Search Result | save_image_search_result | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| text_jinja_template | text_jinja_template | old/oomlout_ai_roboclick.py:1825 | roboclick_action_text_jinja_template | Text | actions/roboclick_action_text_jinja_template/working.py | RoboClick Action: Text Jinja Template | text_jinja_template, jinja_template | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| wait_for_file | wait_for_file | old/oomlout_ai_roboclick.py:1853 | roboclick_action_wait_for_file | Utility | actions/roboclick_action_wait_for_file/working.py | RoboClick Action: Wait For File | wait_for_file | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |
| openscad_render | openscad_render | old/oomlout_ai_roboclick.py:1877 | roboclick_action_openscad_render | OpenSCAD | actions/roboclick_action_openscad_render/working.py | RoboClick Action: OpenSCAD Render | openscad_render, render | Direct migration candidate | Extract old logic into old(**kwargs), then wire action(**kwargs) + test() |

## Alias Map

| Alias Command | Canonical Command | Migration Handling |
|---|---|---|
| add_file | ai_add_image | Keep thin wrapper module or route in loader metadata aliases |
| add_image | ai_add_image | Keep thin wrapper module or route in loader metadata aliases |
| ai_save_image | save_image_generated | Keep thin wrapper module or route in loader metadata aliases |
| close_tab | browser_close_tab | Keep thin wrapper module or route in loader metadata aliases |
| continue_chat | ai_continue_chat | Keep thin wrapper module or route in loader metadata aliases |
| new_chat | ai_new_chat | Keep thin wrapper module or route in loader metadata aliases |
| openscad_render_file | openscad_render | Keep thin wrapper module or route in loader metadata aliases |
| query | ai_query | Keep thin wrapper module or route in loader metadata aliases |

## Migration Checklist

| Command | Folder | Done? |
|---|---|---|
| ai_add_image | actions/roboclick_action_ai_add_image/working.py | embedded_legacy_local |
| ai_add_file | actions/roboclick_action_ai_add_file/working.py | embedded_legacy_local |
| ai_continue_chat | actions/roboclick_action_ai_continue_chat/working.py | embedded_legacy_local |
| ai_fix_yaml_copy_paste | actions/roboclick_action_ai_fix_yaml_copy_paste/working.py | embedded_legacy_local |
| ai_new_chat | actions/roboclick_action_ai_new_chat/working.py | embedded_legacy_local |
| ai_query | actions/roboclick_action_ai_query/working.py | embedded_legacy_local |
| ai_save_text | actions/roboclick_action_ai_save_text/working.py | embedded_legacy_local |
| ai_set_mode | actions/roboclick_action_ai_set_mode/working.py | embedded_legacy_local |
| ai_skill_image_prompt_full | actions/roboclick_action_ai_skill_image_prompt_full/working.py | embedded_legacy_local |
| ai_skill_image_laser_cut_logo_full | actions/roboclick_action_ai_skill_image_laser_cut_logo_full/working.py | embedded_legacy_local |
| ai_skill_text_to_speech | actions/roboclick_action_ai_skill_text_to_speech/working.py | embedded_legacy_local |
| ai_skill_validate_json | actions/roboclick_action_ai_skill_validate_json/working.py | embedded_legacy_local |
| browser_close_tab | actions/roboclick_action_browser_close_tab/working.py | embedded_legacy_local |
| browser_open_url | actions/roboclick_action_browser_open_url/working.py | embedded_legacy_local |
| browser_save_url | actions/roboclick_action_browser_save_url/working.py | embedded_legacy_local |
| convert_svg_to_pdf | actions/roboclick_action_convert_svg_to_pdf/working.py | embedded_legacy_local |
| convert_svg_to_png | actions/roboclick_action_convert_svg_to_png/working.py | embedded_legacy_local |
| corel_add_text | actions/roboclick_action_corel_add_text/working.py | embedded_legacy_local |
| corel_add_text_box | actions/roboclick_action_corel_add_text_box/working.py | embedded_legacy_local |
| corel_close_file | actions/roboclick_action_corel_close_file/working.py | embedded_legacy_local |
| corel_convert_to_curves | actions/roboclick_action_corel_convert_to_curves/working.py | embedded_legacy_local |
| corel_copy | actions/roboclick_action_corel_copy/working.py | embedded_legacy_local |
| corel_export | actions/roboclick_action_corel_export/working.py | embedded_legacy_local |
| corel_group | actions/roboclick_action_corel_group/working.py | embedded_legacy_local |
| corel_import | actions/roboclick_action_corel_import/working.py | embedded_legacy_local |
| corel_object_order | actions/roboclick_action_corel_object_order/working.py | embedded_legacy_local |
| corel_open | actions/roboclick_action_corel_open/working.py | embedded_legacy_local |
| corel_page_goto | actions/roboclick_action_corel_page_goto/working.py | embedded_legacy_local |
| corel_paste | actions/roboclick_action_corel_paste/working.py | embedded_legacy_local |
| corel_save | actions/roboclick_action_corel_save/working.py | embedded_legacy_local |
| corel_save_as | actions/roboclick_action_corel_save_as/working.py | embedded_legacy_local |
| corel_set_position | actions/roboclick_action_corel_set_position/working.py | embedded_legacy_local |
| corel_set_rotation | actions/roboclick_action_corel_set_rotation/working.py | embedded_legacy_local |
| corel_set_size | actions/roboclick_action_corel_set_size/working.py | embedded_legacy_local |
| corel_trace | actions/roboclick_action_corel_trace/working.py | embedded_legacy_local |
| corel_trace_full | actions/roboclick_action_corel_trace_full/working.py | embedded_legacy_local |
| file_copy | actions/roboclick_action_file_copy/working.py | embedded_legacy_local |
| file_create_text_file | actions/roboclick_action_file_create_text_file/working.py | embedded_legacy_local |
| google_doc_new | actions/roboclick_action_google_doc_new/working.py | embedded_legacy_local |
| google_doc_add_text | actions/roboclick_action_google_doc_add_text/working.py | embedded_legacy_local |
| image_crop | actions/roboclick_action_image_crop/working.py | embedded_legacy_local |
| image_png_transparent_to_white | actions/roboclick_action_image_png_transparent_to_white/working.py | embedded_legacy_local |
| image_quad_swap_for_tile | actions/roboclick_action_image_quad_swap_for_tile/working.py | embedded_legacy_local |
| image_upscale | actions/roboclick_action_image_upscale/working.py | embedded_legacy_local |
| add_image | actions/roboclick_action_alias_add_image/working.py | embedded_legacy_local |
| add_file | actions/roboclick_action_alias_add_file/working.py | embedded_legacy_local |
| close_tab | actions/roboclick_action_alias_close_tab/working.py | embedded_legacy_local |
| new_chat | actions/roboclick_action_alias_new_chat/working.py | embedded_legacy_local |
| query | actions/roboclick_action_alias_query/working.py | embedded_legacy_local |
| ai_save_image | actions/roboclick_action_alias_ai_save_image/working.py | embedded_legacy_local |
| openscad_render_file | actions/roboclick_action_alias_openscad_render_file/working.py | embedded_legacy_local |
| save_image_generated | actions/roboclick_action_save_image_generated/working.py | embedded_legacy_local |
| save_image_search_result | actions/roboclick_action_save_image_search_result/working.py | embedded_legacy_local |
| text_jinja_template | actions/roboclick_action_text_jinja_template/working.py | embedded_legacy_local |
| wait_for_file | actions/roboclick_action_wait_for_file/working.py | embedded_legacy_local |
| openscad_render | actions/roboclick_action_openscad_render/working.py | embedded_legacy_local |
