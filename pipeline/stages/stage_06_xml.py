"""Stage 6: XML Routing Structure.

Serializes AST into deterministic XML for routing.
Preserves node identity, ordering, dependencies, operation type, integrity metadata.
"""
from __future__ import annotations

import xml.etree.ElementTree as ET
from ..core.types import PipelineArtifact, Provenance, Invariant


def _node_to_xml(node) -> ET.Element:
    elem = ET.Element("node", {
        "id": node.node_id,
        "type": node.node_type,
        "provenance": node.provenance.value,
    })
    if node.inputs:
        inputs = ET.SubElement(elem, "inputs")
        for inp in node.inputs:
            ET.SubElement(inputs, "input").text = inp
    if node.outputs:
        outputs = ET.SubElement(elem, "outputs")
        for out in node.outputs:
            ET.SubElement(outputs, "output").text = out
    if node.dependencies:
        deps = ET.SubElement(elem, "dependencies")
        for dep in node.dependencies:
            ET.SubElement(deps, "dep").text = dep
    if node.semantic_effect:
        ET.SubElement(elem, "semantic_effect").text = node.semantic_effect
    return elem


def stage_xml_routing(artifact: PipelineArtifact) -> PipelineArtifact:
    """Serialize AST to deterministic XML.

    INPUT: AST nodes
    OUTPUT: XML tree + hash
    """
    data = artifact.data or {}
    nodes = data.get("nodes", [])

    root = ET.Element("model")
    for node in nodes:
        root.append(_node_to_xml(node))

    xml_str = ET.tostring(root, encoding="unicode")
    xml_hash = __import__("hashlib").sha256(xml_str.encode()).hexdigest()[:16]

    return PipelineArtifact(
        stage=6,
        name="xml_routing",
        data={"xml": xml_str, "hash": xml_hash, "node_count": len(nodes)},
        provenance=Provenance.DERIVED,
        invariants=(
            Invariant("xml_1", "serialization", "XML is deterministic", True),
            Invariant("xml_2", "ordering", "Node order preserved", True),
        ),
    )
