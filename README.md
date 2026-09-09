# Sovereign Obfuscation Suite

[![Tests](https://img.shields.io/badge/tests-14%2F14-brightgreen)](tests/)
[![Python](https://img.shields.io/badge/python-%E2%89%A53.11-3776AB?logo=python&logoColor=white)](https://python.org)
[![Q#](https://img.shields.io/badge/Q%23-quantum-512BD4?logo=dotnet&logoColor=white)](qsharp/)
[![OpenQASM](https://img.shields.io/badge/OpenQASM-3.0-6929C4)](openqasm/)
[![JCL](https://img.shields.io/badge/JCL-z%2FOS-E8E8E8)](jcl/)
[![MUMPS](https://img.shields.io/badge/MUMPS-M-444444)](mumps/)
[![Elixir](https://img.shields.io/badge/elixir-plumbline-4B275F?logo=elixir&logoColor=white)](elixir/)
[![MATLAB](https://img.shields.io/badge/MATLAB-manifold-E16737)](matlab/)
[![License](https://img.shields.io/badge/license-GPL--2.0%20%7C%20GPL--3.0%20%7C%20AGPL--3.0-blue)](#license)
[![Copyleft](https://img.shields.io/badge/copyleft-%E2%86%BA-red)](LICENSE)

---

Quantum-inspired cryptographic obfuscation system spanning seven languages and three computational paradigms: classical, quantum-circuit, and mainframe batch. Every module enforces sovereign control — data collapses on unauthorized access, recovers only through sovereign authority, and leaves no cleartext residue in any execution path.

## Modules

| Module | What it does |
|--------|-------------|
| **Quantum Collapse** | HMAC-challenged access gate with fuse-based state destruction. One wrong proof and the fuse blows. |
| **Ghost Mirror** | Encrypted backup in a hidden dimension. On collapse the plaintext is gone; sovereign recovery decrypts the mirror. |
| **Quantum-RAG MixColumn** | AES GF(2^8) matrix diffusion with RAG-weighted phase modulation over the column vector. |
| **Nighthawk Spiral Stripper** | Golden-ratio permutation of token positions filtered through a Fibonacci-word sieve. |
| **Sparse RBG GLUE** | Polynomial-time dispatch over a sparse tensor topology — deterministic, reproducible byte generation. |

## Multi-Language Stack

```
Python ─────── Core obfuscation suite (5 modules, 14 tests)
Q# ─────────── Nighthawk wormhole teleportation circuit
OpenQASM 3.0 ─ MixColumn entanglement + Sparse RBG quantum glue
JCL ────────── z/OS batch pipelines (QASM ingestion, tensor pruning, spiral reduction)
M/MUMPS ────── Blackhole singularity ledger ingestion
Elixir ─────── Recursive z-axis tensor descent (synthetic plumbline)
MATLAB ─────── Holographic Riemannian manifold binding
```

## Quick Start

```bash
pip install -e ".[dev]"
pytest
```

```python
from python.sovereign import GhostMirrorSystem
from cryptography.fernet import Fernet

key = Fernet.generate_key()
system = GhostMirrorSystem("secret", "entangle", key)

system.secure_bind("doc1", "classified data")
system.request_access("doc1", "wrong", "challenge")  # fuse blows -> ghost mirror
system.sovereign_recovery("doc1")                     # sovereign restores from mirror
```

## Architecture

```
User Input
  |
  v
Quantum Collapse ──── HMAC challenge + fuse state
  |
  v
Ghost Mirror ──────── encrypted backup on collapse
  |
  v
Quantum-RAG MixColumn  AES diffusion + RAG phase modulation
  |
  v
Spiral Stripper ───── golden ratio permutation + Fibonacci watermark
  |
  v
Sparse RBG GLUE ───── polynomial dispatch over sparse tensor
  |
  v
Output (obfuscated, sovereign-controlled, provenance-sealed)
```

## Repository Layout

```
sovereign-obfuscation-suite/
├── python/sovereign/          # Core Python modules
│   ├── quantum_collapse.py    # HMAC challenge + fuse state
│   ├── ghost_mirror.py        # Encrypted backup + sovereign recovery
│   ├── rag_mix_column.py      # AES GF(2^8) + RAG phase modulation
│   ├── spiral_stripper.py     # Golden ratio permutation + Fibonacci filter
│   └── sparse_rbg.py          # Polynomial dispatch over sparse tensor
├── qsharp/
│   └── NighthawkWormhole.qs   # Q# wormhole teleportation circuit
├── openqasm/
│   ├── mixcolumn_entanglement.qasm
│   └── sparse_rbg_glue.qasm
├── jcl/
│   ├── qasm_batch.jcl         # z/OS QASM ingestion
│   ├── tensor_prune.jcl       # Logarithmic spiral pruning
│   ├── spiral_prune.jcl       # RBG library reduction
│   └── sparse_rbg_qasm.jcl    # Sparse RBG coprocessor dispatch
├── mumps/
│   └── singularity.m          # Blackhole ledger ingestion
├── elixir/lib/sovereign/
│   └── synthetic_plumbline.ex # Recursive z-axis tensor descent
├── matlab/
│   └── SovereignSystem.m      # Holographic Riemannian manifold
├── tests/
│   └── test_sovereign.py      # 14 tests
├── LICENSE                    # Trilicense header
├── LICENSE-GPL2               # GPL-2.0
├── LICENSE-GPL3               # GPL-3.0
├── LICENSE-AGPL3              # AGPL-3.0
└── pyproject.toml
```

## License

**Trilicense — Copyleft.** This software is released under your choice of:

- [GNU General Public License v2.0](LICENSE-GPL2) (GPL-2.0-only)
- [GNU General Public License v3.0](LICENSE-GPL3) (GPL-3.0-only)
- [GNU Affero General Public License v3.0](LICENSE-AGPL3) (AGPL-3.0-only)

Pick one. If you redistribute, you must include the full text of your chosen license and keep the copyleft intact. See [LICENSE](LICENSE) for the trilicense notice.

```
SPDX-License-Identifier: GPL-2.0-only OR GPL-3.0-only OR AGPL-3.0-only
```
