# gridfinity_tray_raw

**Gridfinity: Tray Raw**

Returns a raw OpenSCAD wrapper around the vendored Gridfinity Extended basic cup, using gridfinity_width, gridfinity_depth, and gridfinity_height as the public size inputs.

## Returns

Raw SCAD geometry component dict.

## Variables

| Name | Description | Type | Default |
|------|-------------|------|---------|
| gridfinity_width | Width in Gridfinity units. | number | 2 |
| gridfinity_depth | Depth in Gridfinity units. | number | 1 |
| gridfinity_height | Height in Gridfinity units. | number | 3 |
| filled_in | Fill the cup into a solid block or fill the lip. | string | "disabled" |
| wall_thickness | Outer wall thickness in mm. Zero uses upstream auto sizing. | number | 0 |
| headroom | Undersize the top by this amount for easier stacking. | number | 0.8 |
| lip_style | Cup lip style. | string | "normal" |
| vertical_chambers | Number of vertical chambers. | number | 1 |
| horizontal_chambers | Number of horizontal chambers. | number | 1 |
| enable_magnets | Enable base magnet holes. | bool | False |
| enable_screws | Enable base screw holes. | bool | False |
| magnet_size | Magnet diameter and height [d,h] in mm. | list | [6.5,2.4] |
| screw_size | Screw diameter and height [d,h] in mm. | list | [3,6] |
| floor_thickness | Minimum thickness above cutouts in the base. | number | 0.7 |
| efficient_floor | Efficient floor mode. | string | "off" |
| sub_pitch | Bottom pad subdivision pitch. | number | 1 |
| flat_base | Internal base style. | string | "off" |
| label_style | Label style. | string | "disabled" |
| label_position | Label position. | string | "left" |
| sliding_lid_enabled | Enable the sliding lid geometry. | bool | False |
| fingerslide | Finger slide style. | string | "none" |
| tapered_corner | Tapered corner style. | string | "none" |
| wallpattern_enabled | Enable wall cutout patterns. | bool | False |
| floorpattern_enabled | Enable floor patterns. | bool | False |
| wallcutout_vertical | Vertical wall cutout mode. | string | "disabled" |
| wallcutout_horizontal | Horizontal wall cutout mode. | string | "disabled" |
| extension_x_enabled | Extendable tab mode on X. | string | "disabled" |
| extension_y_enabled | Extendable tab mode on Y. | string | "disabled" |
| text_1 | Add the bin size to the bottom text. | bool | False |
| text_2 | Enable custom bottom text. | bool | False |
| text_2_text | Custom bottom text value. | string | "Gridfinity Extended" |
| pitch | Gridfinity pitch [x,y,z] in mm. | list | [42,42,7] |
| clearance | Clearance [x,y,z] in mm. | list | [0.5,0.5,0] |
| set_colour | Color handling mode for the upstream renderer. | string | "enable" |
| render_position | Upstream render position mode. | string | "center" |
| fa | OpenSCAD fragment angle. | number | 6 |
| fs | OpenSCAD fragment size. | number | 0.4 |
| fn | OpenSCAD fragment count override. | number | 0 |
| random_seed | Random seed for procedural features. | number | 0 |
| force_render | Force render on costly upstream components. | bool | True |
| pos | 3-element [x,y,z] position. | list | [0,0,0] |
| rot | Rotation [rx,ry,rz] in degrees. | list | [0,0,0] |
| type | Geometry type: positive or negative. | string | "positive" |
