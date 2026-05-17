# Post-Migration Cleanup Checklist

These cleanup tasks are intentionally deferred until after the migration has been stable for a while.

## Safe to archive later (do not delete immediately)

- [ ] `oobb_get_items_oobb.py`
- [ ] `oobb_get_items_oobb_old.py`
- [ ] `oobb_get_items_oobb_wire.py`
- [ ] `oobb_get_items_oobb_holder.py`
- [ ] `oobb_get_items_oobb_other.py`
- [ ] `oobb_get_items_oobb_bearing_plate.py`
- [ ] `oobb_get_items_other.py`
- [ ] `oobb_get_items_test.py`
- [ ] `oobb_get_items_test_old.py`
- [ ] `oobb_make_sets_old.py`

## Keep for now

- [ ] `oobb_base.py` (dispatch and core glue)
- [ ] `oobb_make_sets.py` (legacy set list and compatibility flow)
- [ ] `oobb_get_item_common.py` (shared geometry helpers)
- [ ] `oobb_variables.py` (global constants/variables)
- [ ] `oobb.py` (compat import surface)

## Future simplifications after stable period

- [ ] Remove final legacy getattr fallback from `oobb_base.get_thing_from_dict()`
- [ ] Simplify `oobb_make_sets.make_all()` to pure discovery mode
- [ ] Reduce duplicated/legacy migration helper scripts in `part_calls/`

## Generated artifacts expected in VCS

- [ ] `part_calls/documentation_data.json`
- [ ] `part_calls/documentation.html`
- [ ] `part_calls/objects/README.md`
- [ ] `part_calls/sets/README.md`
- [ ] Per-folder `README.md` files under `part_calls/objects/*` and `part_calls/sets/*`
