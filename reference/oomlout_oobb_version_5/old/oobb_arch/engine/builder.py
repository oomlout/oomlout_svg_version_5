from oobb_arch.domain.models import BuildResult


def build_from_plan(plan) -> BuildResult:
    """Execute a plan.

    Phase 1 scope: returns an empty result container and intentionally
    avoids side effects until Phase 3 wiring.
    """

    return BuildResult(part_id=plan.request.part.identifier)
