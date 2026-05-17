from oobb_arch.catalog.registry import BuilderRegistry


def _register_getters_from_module(registry: BuilderRegistry, module) -> None:
    for attr in dir(module):
        if not attr.startswith("get_"):
            continue
        func = getattr(module, attr)
        if not callable(func):
            continue
        part_type = attr[len("get_") :]
        # Preserve precedence by only registering first-seen implementation.
        if not registry.has(part_type):
            registry.register(part_type, func)


def build_legacy_builder_registry(modules) -> BuilderRegistry:
    """Build registry from module list in precedence order."""

    registry = BuilderRegistry()
    for module in modules:
        _register_getters_from_module(registry, module)
    return registry
