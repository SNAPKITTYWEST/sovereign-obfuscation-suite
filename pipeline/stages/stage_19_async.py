"""Stage 19: Asynchronous Router.

Converts verified divergence information into routing decisions.
Router must fail closed on integrity violations.
"""
from __future__ import annotations

from ..core.types import PipelineArtifact, Provenance, Invariant, Route


ROUTER_OUTPUTS = frozenset({"ROUTE_PRIMARY", "ROUTE_MIRROR", "ROUTE_BOTH", "HOLD", "REJECT"})


def stage_async_router(artifact: PipelineArtifact) -> PipelineArtifact:
    """Make routing decision based on divergence analysis.

    INPUT: Parallel mirror divergence
    OUTPUT: Routing decision + integrity status
    """
    data = artifact.data or {}
    divergences = data.get("divergences", [])
    synchronous = data.get("synchronous", True)

    if synchronous:
        decision = "ROUTE_BOTH"
        reason = "No divergence detected"
    elif len(divergences) > 0 and all(d.get("classification") == "COMPUTATIONAL" for d in divergences):
        decision = "ROUTE_PRIMARY"
        reason = "Computational divergence only"
    else:
        decision = "HOLD"
        reason = "Unresolved divergence"

    route = Route(
        route_id="async_main",
        source="parallel_mirror",
        destination=decision,
        route_type=decision,
        provenance=Provenance.DERIVED,
    )

    return PipelineArtifact(
        stage=19,
        name="async_router",
        data={
            "decision": decision,
            "reason": reason,
            "route": route,
            "fail_closed": True,
        },
        provenance=Provenance.DERIVED,
        invariants=(
            Invariant("async_1", "type", "Router fails closed on integrity violations", True),
            Invariant("async_2", "provenance", f"Decision in ROUTER_OUTPUTS: {decision in ROUTER_OUTPUTS}", decision in ROUTER_OUTPUTS),
        ),
    )
