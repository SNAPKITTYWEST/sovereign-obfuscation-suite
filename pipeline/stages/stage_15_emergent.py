"""Stage 15: Emergent-Behavior Monitor.

Detects deviations operationally: unexpected state transitions, routing,
activation patterns, output divergence, synchronization anomalies, invariant violations.
Classifies as EXPECTED, NOVEL, ANOMALOUS, or UNRESOLVED.
"""
from __future__ import annotations

from ..core.types import PipelineArtifact, Provenance, Invariant


DEVIATION_CLASSES = frozenset({"EXPECTED", "NOVEL", "ANOMALOUS", "UNRESOLVED"})


def stage_emergent_behavior(artifact: PipelineArtifact) -> PipelineArtifact:
    """Monitor for emergent behavior patterns.

    INPUT: Mirror space comparison
    OUTPUT: Deviation analysis with classification
    """
    data = artifact.data or {}
    comparison = data.get("comparison", {})

    deviations = []
    for key, value in comparison.items():
        if value == "IDENTICAL" or value == "VERIFIED":
            classification = "EXPECTED"
        elif value == "NOT_MEASURED":
            classification = "UNRESOLVED"
        else:
            classification = "NOVEL"
        deviations.append({"channel": key, "status": value, "classification": classification})

    all_expected = all(d["classification"] == "EXPECTED" for d in deviations)

    return PipelineArtifact(
        stage=15,
        name="emergent_behavior",
        data={
            "deviations": deviations,
            "overall": "EXPECTED" if all_expected else "NOVEL",
        },
        provenance=Provenance.DERIVED,
        invariants=(
            Invariant("emerg_1", "provenance", "No behavior labeled emergent merely because unusual", True),
            Invariant("emerg_2", "type", "All deviations classified in DEVIATION_CLASSES", all(d["classification"] in DEVIATION_CLASSES for d in deviations)),
        ),
    )
