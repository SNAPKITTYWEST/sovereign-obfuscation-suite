"""Tests for the 20-stage formal verification pipeline."""
import pytest
from pipeline.core.pipeline import Pipeline
from pipeline.core.types import PipelineArtifact, Provenance, Node, Operation, BinaryObject, Invariant
from pipeline.stages import ALL_STAGES


def _initial():
    return PipelineArtifact(
        stage=0,
        name="initial",
        data={
            "observed_input": "test",
            "activations": [[0.1, 0.2], [0.3, 0.4]],
        },
        provenance=Provenance.OBSERVED,
    )


class TestPipeline:
    def test_all_20_stages_registered(self):
        assert len(ALL_STAGES) == 20

    def test_full_pipeline_runs(self):
        pipe = Pipeline()
        for num, fn in ALL_STAGES.items():
            pipe.register(num, fn)
        report = pipe.execute(_initial())
        assert len(report.stages) == 20
        assert all(sr.success for sr in report.stages)

    def test_full_pipeline_no_rejected(self):
        pipe = Pipeline()
        for num, fn in ALL_STAGES.items():
            pipe.register(num, fn)
        report = pipe.execute(_initial())
        assert len(report.rejected) == 0


class TestStage1:
    def test_observable_boundary(self):
        result = ALL_STAGES[1](_initial())
        assert result.stage == 1
        assert result.name == "observable_boundary"
        assert result.provenance == Provenance.OBSERVED

    def test_observable_boundary_classifies(self):
        art = PipelineArtifact(stage=0, name="test", data={"observed_x": 1, "inferred_y": 2, "z": 3})
        result = ALL_STAGES[1](art)
        data = result.data
        assert data["observed_x"]["provenance"] == Provenance.OBSERVED
        assert data["inferred_y"]["provenance"] == Provenance.INFERRED


class TestStage2:
    def test_latent_with_activations(self):
        result = ALL_STAGES[2](_initial())
        assert result.stage == 2
        state = result.data["state"]
        assert state.dimensionality == 2
        assert state.provenance == Provenance.OBSERVED

    def test_latent_without_activations(self):
        art = PipelineArtifact(stage=0, name="test", data={"activations": None})
        result = ALL_STAGES[2](art)
        assert result.provenance == Provenance.UNKNOWN


class TestStage5:
    def test_ast_has_nodes(self):
        # Chain stages 1-5
        art = _initial()
        for i in range(1, 6):
            art = ALL_STAGES[i](art)
        nodes = art.data["nodes"]
        assert len(nodes) >= 3
        assert nodes[0].node_type == "INPUT"
        assert nodes[-1].node_type == "OUTPUT"


class TestStage7:
    def test_binary_encode_decode(self):
        art = _initial()
        for i in range(1, 8):
            art = ALL_STAGES[i](art)
        binary = art.data["binary"]
        encoded = binary.encode()
        decoded = BinaryObject.decode(encoded)
        assert decoded.header == binary.header
        assert decoded.length == binary.length


class TestStage9:
    def test_agda_source_generated(self):
        art = _initial()
        for i in range(1, 10):
            art = ALL_STAGES[i](art)
        agda = art.data["agda_source"]
        assert "module SovereignPipeline" in agda
        assert "record Node" in agda


class TestStage19:
    def test_async_router_decision(self):
        art = _initial()
        for i in range(1, 20):
            art = ALL_STAGES[i](art)
        decision = art.data["decision"]
        assert decision in {"ROUTE_PRIMARY", "ROUTE_MIRROR", "ROUTE_BOTH", "HOLD", "REJECT"}


class TestStage20:
    def test_orchestration_restrictions(self):
        art = _initial()
        for i in range(1, 21):
            art = ALL_STAGES[i](art)
        restrictions = art.data["restrictions"]
        assert restrictions["redefine_invariants"] is False
        assert restrictions["redefine_agda_proofs"] is False


class TestBinaryObject:
    def test_round_trip(self):
        b = BinaryObject(header=b"\x01\x02", obj_type=b"TEST", length=4, payload=b"ABCD")
        encoded = b.encode()
        decoded = BinaryObject.decode(encoded)
        assert decoded.header == b"\x01\x02\x00\x00"
        assert decoded.payload == b"ABCD"

    def test_integrity_changes_with_payload(self):
        a = BinaryObject(header=b"\x01", obj_type=b"A", length=1, payload=b"X")
        b = BinaryObject(header=b"\x01", obj_type=b"A", length=1, payload=b"Y")
        a.encode()
        b.encode()
        assert a.integrity != b.integrity


class TestTypes:
    def test_node_hash_deterministic(self):
        n = Node(node_id="a", node_type="INPUT")
        h1 = n.hash()
        h2 = n.hash()
        assert h1 == h2

    def test_invariant(self):
        inv = Invariant(inv_id="test", inv_type="type", holds=True)
        assert inv.holds
