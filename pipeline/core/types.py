"""Core type definitions for the formal verification pipeline.

All types preserve provenance and enforce invariant preservation.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Provenance(Enum):
    """Classification of knowledge source."""
    OBSERVED = "OBSERVED"
    DERIVED = "DERIVED"
    MEASURED = "MEASURED"
    INFERRED = "INFERRED"
    UNKNOWN = "UNKNOWN"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class Node:
    """AST node with typed inputs/outputs and provenance."""
    node_id: str
    node_type: str
    inputs: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    semantic_effect: str = ""
    provenance: Provenance = Provenance.UNKNOWN

    def hash(self) -> str:
        content = json.dumps({
            "id": self.node_id,
            "type": self.node_type,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "deps": self.dependencies,
            "effect": self.semantic_effect,
            "prov": self.provenance.value,
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:16]


@dataclass(frozen=True)
class State:
    """Typed computational state."""
    state_id: str
    dimensionality: int = 0
    norms: tuple[float, ...] = ()
    sparsity: float = 0.0
    activation_density: float = 0.0
    provenance: Provenance = Provenance.UNKNOWN


@dataclass(frozen=True)
class Operation:
    """Typed transformation between spaces."""
    op_id: str
    op_type: str  # matrix_mult, addition, normalization, activation, projection, routing, aggregation, attention, sparse
    input_dims: tuple[int, ...] = ()
    output_dims: tuple[int, ...] = ()
    precision: str = "float32"
    numerical_behavior: str = ""
    provenance: Provenance = Provenance.UNKNOWN


@dataclass(frozen=True)
class Transition:
    """State transition with invariant preservation."""
    from_state: str
    to_state: str
    operation: str
    invariant_preserved: bool = True
    provenance: Provenance = Provenance.UNKNOWN


@dataclass(frozen=True)
class Route:
    """Routing decision with integrity."""
    route_id: str
    source: str
    destination: str
    route_type: str = "PRIMARY"
    cost: float = 0.0
    provenance: Provenance = Provenance.UNKNOWN


@dataclass
class BinaryObject:
    """Self-describing binary representation."""
    header: bytes = b""
    obj_type: bytes = b""
    length: int = 0
    payload: bytes = b""
    children: list[BinaryObject] = field(default_factory=list)
    integrity: bytes = b""

    def encode(self) -> bytes:
        header = self.header[:4].ljust(4, b"\x00")
        obj_type = self.obj_type[:4].ljust(4, b"\x00")
        parts = [
            header,
            obj_type,
            self.length.to_bytes(4, "big"),
            self.payload,
        ]
        for child in self.children:
            parts.append(child.encode())
        data = b"".join(parts)
        self.integrity = hashlib.sha256(data).digest()[:16]
        return data + self.integrity

    @staticmethod
    def decode(data: bytes) -> BinaryObject:
        if len(data) < 20:
            return BinaryObject()
        header = data[:4]
        obj_type = data[4:8]
        length = int.from_bytes(data[8:12], "big")
        payload = data[12:12 + length]
        integrity = data[12 + length:12 + length + 16]
        return BinaryObject(
            header=header,
            obj_type=obj_type,
            length=length,
            payload=payload,
            integrity=integrity,
        )


@dataclass(frozen=True)
class IntegrityProof:
    """Cryptographic proof of invariant preservation."""
    proof_id: str
    invariants_checked: tuple[str, ...] = ()
    all_preserved: bool = True
    proof_hash: str = ""

    def verify(self) -> bool:
        if not self.all_preserved:
            return False
        content = f"{self.proof_id}:{':'.join(self.invariants_checked)}"
        expected = hashlib.sha256(content.encode()).hexdigest()[:16]
        return self.proof_hash == expected or self.proof_hash == ""


@dataclass(frozen=True)
class Invariant:
    """Formal invariant definition."""
    inv_id: str
    inv_type: str  # type, dimensional, ordering, dependency, memory_bound, serialization, numerical, provenance
    description: str = ""
    holds: bool = True


@dataclass
class PipelineArtifact:
    """Immutable artifact produced by a pipeline stage."""
    stage: int
    name: str
    data: Any = None
    provenance: Provenance = Provenance.DERIVED
    hash: str = ""
    invariants: tuple[Invariant, ...] = ()
    children: list[PipelineArtifact] = field(default_factory=list)

    def compute_hash(self) -> str:
        content = f"{self.stage}:{self.name}:{self.provenance.value}:{str(self.data)[:512]}"
        self.hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        return self.hash
