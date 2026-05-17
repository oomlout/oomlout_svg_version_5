# Backward-compatibility shim -- all functionality now lives in oobb.py
def __getattr__(name):
    print(f"WARNING: Accessing {name} from oobb_base.py is deprecated, import from oobb.py instead")
    import oobb
    return getattr(oobb, name)

