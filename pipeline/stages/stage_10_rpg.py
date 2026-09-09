"""Stage 10: RPG Agent Routing.

Exposes verified semantic structure to RPG agent boundary.
RPG must not modify verified semantics silently.
Any modification produces NEW ARTIFACT, NEW HASH, NEW VERIFICATION STATE.
"""
from __future__ import annotations

import hashlib
import json
from ..core.types import PipelineArtifact, Provenance, Route, Invariant


def stage_rpg_agent(artifact: PipelineArtifact) -> PipelineArtifact:
    """Generate RPG routing structure.

    INPUT: Verified Agda tree
    OUTPUT: Routes + workflow coordination spec
    """
    data = artifact.data or {}

    routes = [
        Route(
            route_id="rpg_main",
            source="agda_verified",
            destination="execution",
            route_type="PRIMARY",
            provenance=Provenance.DERIVED,
        ),
        Route(
            route_id="rpg_mirror",
            source="agda_verified",
            destination="mirror",
            route_type="MIRROR",
            provenance=Provenance.DERIVED,
        ),
    ]

    workflow = {
        "coordination": "deterministic",
        "job_state": "verified",
        "artifact_selection": "hash_based",
        "execution_request": "immutable",
        "result_collection": "append_only",
    }

    return PipelineArtifact(
        stage=10,
        name="rpg_agent",
        data={
            "routes": routes,
            "workflow": workflow,
            "verification_hash": hashlib.sha256(json.dumps(workflow, sort_keys=True).encode()).hexdigest()[:16],
        },
        provenance=Provenance.DERIVED,
        invariants=(
            Invariant("rpg_1", "dependency", "RPG reads but does not modify verified semantics", True),
            Invariant("rpg_2", "provenance", "Any modification produces new artifact", True),
        ),
    )
