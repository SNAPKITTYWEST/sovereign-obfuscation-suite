"""Tests for the Sovereign Obfuscation Suite Python core."""
import hmac
import hashlib
import pytest
from cryptography.fernet import Fernet

from python.sovereign.quantum_collapse import QuantumCollapseSystem
from python.sovereign.ghost_mirror import GhostMirrorSystem
from python.sovereign.rag_mix_column import QuantumRAGMixColumn
from python.sovereign.spiral_stripper import NighthawkSpiralStripper
from python.sovereign.sparse_rbg import (
    rbg_sparse_dispatch,
    strip_mix_columns_to_sparse_rbg,
    MASTER_COEFFS,
    PRIME,
)


S_KEY = "Sovereign_OS_2026"
E_KEY = "Entanglement_Secret_99"


class TestQuantumCollapse:
    def test_secure_bind_sets_intact(self):
        sys = QuantumCollapseSystem(S_KEY, E_KEY)
        sys.secure_bind("t1", "hello")
        assert sys.fuse_state["t1"] == "INTACT"
        assert sys.server_storage["t1"] == "hello"

    def test_valid_access_returns_text(self):
        sys = QuantumCollapseSystem(S_KEY, E_KEY)
        sys.secure_bind("t1", "secret")
        challenge = "ch_123"
        proof = hmac.new(E_KEY.encode(), challenge.encode(), hashlib.sha256).hexdigest()
        result = sys.request_access("t1", proof, challenge)
        assert result == "secret"

    def test_invalid_access_raises(self):
        sys = QuantumCollapseSystem(S_KEY, E_KEY)
        sys.secure_bind("t1", "secret")
        with pytest.raises(NotImplementedError):
            sys.request_access("t1", "wrong", "ch")


class TestGhostMirror:
    @pytest.fixture
    def system(self):
        key = Fernet.generate_key()
        return GhostMirrorSystem(S_KEY, E_KEY, key)

    def test_collapse_moves_to_mirror(self, system):
        system.secure_bind("t1", "data")
        system.request_access("t1", "wrong", "ch")
        assert system.fuse_state["t1"] == "COLLAPSED"
        assert "t1" in system.ghost_mirror

    def test_sovereign_recovery_restores(self, system):
        system.secure_bind("t1", "data")
        system.request_access("t1", "wrong", "ch")
        assert system.sovereign_recovery("t1")
        assert system.fuse_state["t1"] == "INTACT"
        assert system.server_storage["t1"] == "data"
        assert "t1" not in system.ghost_mirror

    def test_recovery_without_ghost_fails(self, system):
        system.secure_bind("t1", "data")
        assert not system.sovereign_recovery("nonexistent")


class TestRAGMixColumn:
    def test_output_length(self):
        mixer = QuantumRAGMixColumn()
        result = mixer.mix_column([0x57, 0x83, 0xE4, 0x1F])
        assert len(result) == 4

    def test_with_context_vector(self):
        mixer = QuantumRAGMixColumn()
        result = mixer.mix_column([0x57, 0x83, 0xE4, 0x1F], [0.12, 0.45, 0.89, 0.33])
        assert len(result) == 4

    def test_invalid_length_raises(self):
        mixer = QuantumRAGMixColumn()
        with pytest.raises(ValueError):
            mixer.mix_column([1, 2, 3])


class TestSpiralStripper:
    def test_braid_preserves_word_count(self):
        s = NighthawkSpiralStripper()
        text = "The quantum state is teleported"
        result = s.execute_sovereign_braid(text)
        assert len(result.split()) == len(text.split())

    def test_empty_text(self):
        s = NighthawkSpiralStripper()
        assert s.execute_sovereign_braid("") == ""


class TestSparseRBG:
    def test_dispatch_returns_bytes(self):
        result = rbg_sparse_dispatch(b"test", MASTER_COEFFS, PRIME)
        assert isinstance(result, bytes)

    def test_dispatch_deterministic(self):
        a = rbg_sparse_dispatch(b"hello world", MASTER_COEFFS, PRIME)
        b = rbg_sparse_dispatch(b"hello world", MASTER_COEFFS, PRIME)
        assert a == b

    def test_strip_returns_tuple(self):
        rows, cols, payload = strip_mix_columns_to_sparse_rbg(
            b"test data here", MASTER_COEFFS, PRIME
        )
        assert len(rows) == len(cols)
        assert isinstance(payload, bytes)
