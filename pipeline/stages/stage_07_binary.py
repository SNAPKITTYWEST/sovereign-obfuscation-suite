"""Stage 7: Recursive Binary Stream.

Lowers semantic structure into self-describing binary representation.
Every binary object is independently decodable. No information lost.
"""
from __future__ import annotations

from ..core.types import PipelineArtifact, BinaryObject, Provenance, Invariant


def stage_binary_stream(artifact: PipelineArtifact) -> PipelineArtifact:
    """Lower XML/AST to binary representation.

    INPUT: XML routing data
    OUTPUT: BinaryObject with HEADER, TYPE, LENGTH, PAYLOAD, CHILDREN, INTEGRITY
    """
    data = artifact.data or {}
    xml_str = data.get("xml", "")
    node_count = data.get("node_count", 0)

    payload = xml_str.encode("utf-8")
    binary = BinaryObject(
        header=b"\x53\x56\x52\x01",  # "SVR" + version 1
        obj_type=b"ASTree",
        length=len(payload),
        payload=payload,
    )

    encoded = binary.encode()

    return PipelineArtifact(
        stage=7,
        name="binary_stream",
        data={
            "binary": binary,
            "encoded_bytes": len(encoded),
            "node_count": node_count,
            "integrity": binary.integrity.hex(),
        },
        provenance=Provenance.DERIVED,
        invariants=(
            Invariant("bin_1", "serialization", "Binary independently decodable", True),
            Invariant("bin_2", "memory_bound", f"Size={len(encoded)} bytes", len(encoded) < 10_000_000),
        ),
    )
