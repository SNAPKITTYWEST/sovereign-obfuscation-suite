"""Stage 5: AST Representation.

Converts semantic operation graph into an AST with typed nodes.
Every node contains: node_id, type, inputs, outputs, dependencies, semantic_effect.
"""
from __future__ import annotations

from ..core.types import PipelineArtifact, Provenance, Node, Invariant


def stage_ast_representation(artifact: PipelineArtifact) -> PipelineArtifact:
    """Build AST from neural math operations.

    INPUT: Typed neural operations
    OUTPUT: Tree of AST nodes with dependencies
    """
    data = artifact.data or {}
    operations = data.get("operations", [])

    nodes = [
        Node(
            node_id="root_input",
            node_type="INPUT",
            outputs=("raw_input",),
            provenance=Provenance.OBSERVED,
        ),
    ]

    prev_output = "raw_input"
    for op in operations:
        node = Node(
            node_id=op.op_id,
            node_type="TRANSFORM",
            inputs=(prev_output,),
            outputs=(f"{op.op_id}_out",),
            dependencies=(prev_output,),
            semantic_effect=f"{op.op_type}({','.join(str(d) for d in op.input_dims)})->({','.join(str(d) for d in op.output_dims)})",
            provenance=Provenance.DERIVED,
        )
        nodes.append(node)
        prev_output = f"{op.op_id}_out"

    nodes.append(Node(
        node_id="root_output",
        node_type="OUTPUT",
        inputs=(prev_output,),
        provenance=Provenance.DERIVED,
    ))

    return PipelineArtifact(
        stage=5,
        name="ast",
        data={"nodes": nodes, "root": "root_input", "leaf": "root_output"},
        provenance=Provenance.DERIVED,
        invariants=(
            Invariant("ast_1", "ordering", "DAG has no cycles", True),
            Invariant("ast_2", "dependency", "All deps resolved", True),
        ),
    )
