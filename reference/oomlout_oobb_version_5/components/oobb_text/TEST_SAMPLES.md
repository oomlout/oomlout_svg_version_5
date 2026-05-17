# Test Samples

## Exact `samples` block to paste into `working.py`

```python
samples = [
    {
        "filename": "test_1",
        "preview_rot": [65, 0, 25],
        "kwargs": {"type": "positive", "text": "OOBB", "size": 10, "depth": 1.2, "pos": [0, 0, 0]},
    },
    {
        "filename": "test_2",
        "preview_rot": [65, 0, 25],
        "kwargs": {"type": "positive", "text": "bearing_plate_set", "concate": True, "h": 1, "pos": [0, 0, 0]},
    },
]
```

## Sample-by-sample meaning

### Sample 1: `test_1.png`
- Intent: legacy OOBB text using `depth` as the extrusion-height alias.
- preview_rot: `[65, 0, 25]`
- kwargs: `{"type":"positive","text":"OOBB","size":10,"depth":1.2,"pos":[0,0,0]}`
- Implementation rule: preserve the OOBB defaults for font and centered alignment.

### Sample 2: `test_2.png`
- Intent: abbreviated legacy text using `concate`.
- preview_rot: `[65, 0, 25]`
- kwargs: `{"type":"positive","text":"bearing_plate_set","concate":true,"h":1,"pos":[0,0,0]}`
- Implementation rule: convert `bearing_plate_set` to `bps` before rendering.

## Folder-specific notes

- Notes: `oobb_text` is a compatibility wrapper over the OpenSCAD `text` primitive, matching the legacy helper defaults.

