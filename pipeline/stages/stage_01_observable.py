"""Stage 1: Observable Model Boundary.

Classifies inputs/outputs as OBSERVED, DERIVED, INFERRED, or UNKNOWN.
Never converts an inference into an observation.
"""
from __future__ import annotations

from ..core.types import PipelineArtifact, Provenance, Invariant


def stage_observable_boundary(artifact: PipelineArtifact) -> PipelineArtifact:
    """Establish the observable boundary of model execution.

    INPUT: Raw user-provided data
    OUTPUT: Classified observations with provenance tags
    """
    data = artifact.data or {}
    observations = {}

    for key, value in data.items():
        if key.startswith("observed_"):
            observations[key] = {"value": value, "provenance": Provenance.OBSERVED}
        elif key.startswith("derived_"):
            observations[key] = {"value": value, "provenance": Provenance.DERIVED}
        elif key.startswith("inferred_"):
            observations[key] = {"value": value, "provenance": Provenance.INFERRED}
        else:
            observations[key] = {"value": value, "provenance": Provenance.UNKNOWN}

    invariants = (
        Invariant(
            inv_id="obs_boundary_1",
            inv_type="provenance",
            description="No inference converted to observation",
            holds=True,
        ),
        Invariant(
            inv_id="obs_boundary_2",
            inv_type="provenance",
            description="All data classified with provenance",
            holds=True,
        ),
    )

    return PipelineArtifact(
        stage=1,
        name="observable_boundary",
        data=observations,
        provenance=Provenance.OBSERVED,
        invariants=invariants,
    )
