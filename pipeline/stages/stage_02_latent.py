"""Stage 2: Latent-Space Geometry.

Constructs geometric representation from activation/embedding tensors.
Falls back to UNKNOWN when activations are unavailable.
"""
from __future__ import annotations

import math
from ..core.types import PipelineArtifact, Provenance, State, Invariant


def _safe_norm(values: list[float]) -> float:
    return math.sqrt(sum(v * v for v in values)) if values else 0.0


def _sparsity(values: list[float], threshold: float = 1e-6) -> float:
    if not values:
        return 1.0
    zeros = sum(1 for v in values if abs(v) < threshold)
    return zeros / len(values)


def stage_latent_geometry(artifact: PipelineArtifact) -> PipelineArtifact:
    """Construct geometric representation of latent activations.

    INPUT: Observable boundary data
    OUTPUT: State with dimensionality, norms, distances, sparsity
    """
    data = artifact.data or {}
    activations = data.get("activations")

    if activations is None:
        state = State(
            state_id="latent_unknown",
            provenance=Provenance.UNKNOWN,
        )
        return PipelineArtifact(
            stage=2,
            name="latent_geometry",
            data={"state": state, "note": "LATENT_STATE = UNKNOWN (no activations provided)"},
            provenance=Provenance.UNKNOWN,
            invariants=(Invariant("latent_1", "provenance", "Fallback to UNKNOWN when data absent", True),),
        )

    if isinstance(activations, list):
        flat = [float(x) for row in activations for x in row] if isinstance(activations[0], list) else [float(x) for x in activations]
        dim = len(activations[0]) if isinstance(activations[0], list) else len(activations)
    elif isinstance(activations, (int, float)):
        flat = [float(activations)]
        dim = 1
    else:
        state = State(state_id="latent_unknown", provenance=Provenance.UNKNOWN)
        return PipelineArtifact(
            stage=2, name="latent_geometry",
            data={"state": state, "note": "LATENT_STATE = UNKNOWN (unparseable activations)"},
            provenance=Provenance.UNKNOWN,
            invariants=(Invariant("latent_1", "provenance", "Fallback to UNKNOWN when data absent", True),),
        )

    state = State(
        state_id="latent_observed",
        dimensionality=dim,
        norms=(_safe_norm(flat),),
        sparsity=_sparsity(flat),
        activation_density=1.0 - _sparsity(flat),
        provenance=Provenance.OBSERVED,
    )

    return PipelineArtifact(
        stage=2,
        name="latent_geometry",
        data={"state": state, "flat_values": flat[:256]},
        provenance=Provenance.OBSERVED,
        invariants=(
            Invariant("latent_dim", "dimensional", f"dim={dim}", dim > 0),
            Invariant("latent_norm", "numerical", "norm >= 0", state.norms[0] >= 0),
        ),
    )
