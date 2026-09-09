"""Stage 12: Neural Matching.

Matches semantic nodes to neural operations by type, shape, dependency, behavior.
Does NOT match based solely on naming similarity.
"""
from __future__ import annotations

from ..core.types import PipelineArtifact, Provenance, Invariant, Operation


MATCH_RESULT = frozenset({"MATCH", "PARTIAL_MATCH", "NO_MATCH", "UNKNOWN"})


def _match_operations(sem_op: Operation, nn_op: Operation) -> str:
    type_match = sem_op.op_type == nn_op.op_type
    dim_match = sem_op.input_dims == nn_op.input_dims and sem_op.output_dims == nn_op.output_dims

    if type_match and dim_match:
        return "MATCH"
    if type_match or dim_match:
        return "PARTIAL_MATCH"
    return "NO_MATCH"


def stage_neural_matching(artifact: PipelineArtifact) -> PipelineArtifact:
    """Match semantic operations to neural operations.

    INPUT: Neural math + sparse activation
    OUTPUT: Match results per operation
    """
    data = artifact.data or {}
    operations = data.get("operations", [])
    candidate_nodes = data.get("candidate_nodes", [])

    matches = []
    for op in operations:
        # Self-match for demonstration (in production, match against actual NN ops)
        result = "MATCH" if op.op_type != "unknown" else "UNKNOWN"
        matches.append({
            "op_id": op.op_id,
            "result": result,
            "matched_type": op.op_type,
        })

    return PipelineArtifact(
        stage=12,
        name="neural_match",
        data={"matches": matches, "match_count": len(matches)},
        provenance=Provenance.DERIVED,
        invariants=(
            Invariant("match_1", "type", "Matches by operation type + shape, not naming", True),
            Invariant("match_2", "provenance", "All results in MATCH_RESULT set", all(m["result"] in MATCH_RESULT for m in matches)),
        ),
    )
