"""Stage 4: Neural Network Mathematics.

Parses available mathematical representation into explicit typed operations.
Only recognizes operations established by supplied artifacts.
"""
from __future__ import annotations

from ..core.types import PipelineArtifact, Provenance, Operation, Invariant


KNOWN_OP_TYPES = frozenset({
    "matrix_mult", "addition", "normalization", "activation",
    "projection", "routing", "aggregation", "attention", "sparse",
})


def stage_neural_math(artifact: PipelineArtifact) -> PipelineArtifact:
    """Parse functor morphisms into explicit neural operations.

    INPUT: Functor structure with morphisms
    OUTPUT: Typed operations with dimensions, precision, dependencies
    """
    data = artifact.data or {}
    morphisms = data.get("morphisms", [])

    typed_ops = []
    for m in morphisms:
        op_type = m.op_type if m.op_type in KNOWN_OP_TYPES else "unknown"
        typed_ops.append(Operation(
            op_id=m.op_id,
            op_type=op_type,
            input_dims=m.input_dims,
            output_dims=m.output_dims,
            precision=m.precision,
            provenance=Provenance.DERIVED,
        ))

    return PipelineArtifact(
        stage=4,
        name="neural_math",
        data={"operations": typed_ops, "op_count": len(typed_ops)},
        provenance=Provenance.DERIVED,
        invariants=(
            Invariant("nn_1", "type", "All ops have recognized types", all(o.op_type in KNOWN_OP_TYPES for o in typed_ops)),
            Invariant("nn_2", "dimensional", "Input/output dims defined", all(o.input_dims and o.output_dims for o in typed_ops)),
        ),
    )
