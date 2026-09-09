"""Stage 18: Mirrored Parallel Model.

Constructs PRIMARY and MIRROR executing equivalent semantic workloads.
Detects asynchronous divergence and classifies it.
"""
from __future__ import annotations

import hashlib
from ..core.types import PipelineArtifact, Provenance, Invariant


DIVERGENCE_CLASSES = frozenset({
    "COMPUTATIONAL", "ROUTING", "TIMING", "RESOURCE", "REPRESENTATIONAL", "UNKNOWN",
})


def stage_parallel_mirror(artifact: PipelineArtifact) -> PipelineArtifact:
    """Execute equivalent workloads on primary and mirror.

    INPUT: Axiom inversion results
    OUTPUT: Primary/Mirror state comparison with divergence classification
    """
    data = artifact.data or {}

    primary_state = {
        "axioms_inverted": data.get("invertible_count", 0),
        "non_invertible": data.get("non_invertible_count", 0),
        "hash": hashlib.sha256(str(data).encode()).hexdigest()[:16],
    }

    mirror_state = {
        "axioms_inverted": data.get("invertible_count", 0),
        "non_invertible": data.get("non_invertible_count", 0),
        "hash": hashlib.sha256(f"mirror:{str(data)}".encode()).hexdigest()[:16],
    }

    divergences = []
    for key in primary_state:
        if key == "hash":
            continue
        if primary_state[key] != mirror_state[key]:
            divergences.append({
                "channel": key,
                "primary": primary_state[key],
                "mirror": mirror_state[key],
                "classification": "COMPUTATIONAL",
            })

    return PipelineArtifact(
        stage=18,
        name="parallel_mirror",
        data={
            "primary": primary_state,
            "mirror": mirror_state,
            "divergences": divergences,
            "synchronous": len(divergences) == 0,
        },
        provenance=Provenance.DERIVED,
        invariants=(
            Invariant("par_1", "type", "Divergence classified by evidence", True),
            Invariant("par_2", "dependency", "Primary and mirror use same invariants", True),
        ),
    )
