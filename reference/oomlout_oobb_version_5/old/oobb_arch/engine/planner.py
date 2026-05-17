from oobb_arch.domain.models import BuildPlan, BuildRequest


def plan_build(request: BuildRequest) -> BuildPlan:
    """Create a deterministic internal plan from a build request."""

    return BuildPlan(request=request)
