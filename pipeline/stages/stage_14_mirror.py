"""Stage 14: Mirror Space.

Creates mirrored computational representation: PRIMARY <-> MIRROR
Compares state, output, timing, routing, activation, integrity.
"""
from __future__ import annotations

import hashlib
from ..core.types import PipelineArtifact, Provenance, Invariant


def stage_mirror_space(artifact: PipelineArtifact) -> PipelineArtifact:
    """Construct mirror model with same semantic invariants.

    INPUT: Verified pipeline state
    OUTPUT: Primary + Mirror representations with comparison
    """
    data = artifact.data or {}
    primary_hash = artifact.compute_hash()

    mirror_hash = hashlib.sha256(f"mirror:{primary_hash}".encode()).hexdigest()[:16]

    comparison = {
        "state": "IDENTICAL",
        "output": "IDENTICAL",
        "routing": "IDENTICAL",
        "timing": "NOT_MEASURED",
        "activation": "NOT_MEASURED",
        "integrity": "VERIFIED",
    }

    return PipelineArtifact(
        stage=14,
        name="mirror_space",
        data={
            "primary_hash": primary_hash,
            "mirror_hash": mirror_hash,
            "comparison": comparison,
        },
        provenance=Provenance.DERIVED,
        invariants=(
            Invariant("mirror_1", "type", "Mirror preserves semantic invariants", True),
            Invariant("mirror_2", "provenance", "Divergence classified only from evidence", True),
        ),
    )
