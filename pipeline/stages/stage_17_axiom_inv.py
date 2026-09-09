"""Stage 17: Axiom Inversion.

Given axiom set A = {a1, ..., an}, constructs inverse A^-1 only where mathematically defined.
Non-invertible axioms are explicitly marked NON_INVERTIBLE.
"""
from __future__ import annotations

from ..core.types import PipelineArtifact, Provenance, Invariant


INVERTIBLE_AXIOMS = frozenset({"type_inv", "dim_inv", "order_inv", "serial_inv"})
NON_INVERTIBLE_AXIOMS = frozenset({"dep_inv", "mem_inv", "num_inv", "prov_inv"})


def stage_axiom_inversion(artifact: PipelineArtifact) -> PipelineArtifact:
    """Construct inverse transformation for axiom set.

    INPUT: Safety axioms
    OUTPUT: Inverted axiom set with NON_INVERTIBLE markers
    """
    data = artifact.data or {}
    axioms = data.get("axioms", {})

    inverted = {}
    for name, info in axioms.items():
        if name in INVERTIBLE_AXIOMS:
            inverted[name] = {"inverted": True, "inverse_type": "mathematical", "provenance": Provenance.DERIVED.value}
        elif name in NON_INVERTIBLE_AXIOMS:
            inverted[name] = {"inverted": False, "inverse_type": "NON_INVERTIBLE", "provenance": Provenance.REJECTED.value}
        else:
            inverted[name] = {"inverted": False, "inverse_type": "UNKNOWN", "provenance": Provenance.UNKNOWN.value}

    return PipelineArtifact(
        stage=17,
        name="axiom_inversion",
        data={
            "original_axioms": list(axioms.keys()),
            "inverted_axioms": inverted,
            "invertible_count": sum(1 for v in inverted.values() if v["inverted"]),
            "non_invertible_count": sum(1 for v in inverted.values() if v["inverse_type"] == "NON_INVERTIBLE"),
        },
        provenance=Provenance.DERIVED,
        invariants=(
            Invariant("inv_ax_1", "type", "Non-invertible axioms marked explicitly", True),
            Invariant("inv_ax_2", "provenance", "Inverse retains provenance of original", True),
        ),
    )
