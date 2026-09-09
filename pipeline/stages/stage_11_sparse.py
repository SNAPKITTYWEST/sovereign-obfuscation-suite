"""Stage 11: Sparse Activation.

Represents sparse activation as a routing problem.
Preserves: selected computation == declared computation.
"""
from __future__ import annotations

from ..core.types import PipelineArtifact, Provenance, Invariant


def stage_sparse_activation(artifact: PipelineArtifact) -> PipelineArtifact:
    """Model sparse activation as routing.

    INPUT: Neural math operations
    OUTPUT: Candidate/active/inactive nodes + routing probability
    """
    data = artifact.data or {}
    operations = data.get("operations", [])

    candidate_nodes = [op.op_id for op in operations]
    # Without evidence of sparsity, mark all as active
    active_nodes = candidate_nodes
    inactive_nodes = []

    return PipelineArtifact(
        stage=11,
        name="sparse_activation",
        data={
            "candidate_nodes": candidate_nodes,
            "active_nodes": active_nodes,
            "inactive_nodes": inactive_nodes,
            "activation_condition": "no_sparsity_evidence",
            "routing_probability": 1.0,
            "routing_cost": len(candidate_nodes),
            "invariant": "selected == declared (no sparse behavior assumed)",
        },
        provenance=Provenance.DERIVED,
        invariants=(
            Invariant("sparse_1", "type", "No sparsity assumed without evidence", True),
            Invariant("sparse_2", "dependency", "selected computation == declared computation", True),
        ),
    )
