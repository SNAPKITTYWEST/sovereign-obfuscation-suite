import numpy as np

MASTER_COEFFS = np.array([123, 456, 789, 1011, 1213], dtype=np.uint64)
PRIME = np.uint64(2**31 - 1)
BOUND_TEXT = b"Sovereign Quantum-Centric Nighthawk Transmission"

RBG_DIM = 64
SPARSITY_THRESHOLD = 0.85


def rbg_sparse_dispatch(text_bytes: bytes, coeffs: np.ndarray, p: np.uint64) -> bytes:
    """Strip dense MixColumn entanglement via Sparse Routed RBG GLUE execution."""
    manifold = np.frombuffer(text_bytes, dtype=np.uint8)
    n = len(coeffs)

    phi = (1.0 + np.sqrt(5.0)) / 2.0
    spiral_strides = np.arange(n, dtype=np.float64) * phi
    indices = np.mod(spiral_strides.astype(np.int32), manifold.size)

    multipliers = np.arange(1, n + 1, dtype=np.uint64)
    v_coords = manifold[indices].astype(np.uint64) * multipliers

    rbg_threshold = np.median(v_coords)
    sparse_mask = v_coords >= rbg_threshold

    v_sparse = np.where(sparse_mask, v_coords, 0).astype(object)
    powers = multipliers.astype(object)

    dispatch_tensor = np.power(v_sparse, powers)
    kappa = np.mod(np.dot(coeffs.astype(object), dispatch_tensor), int(p))

    return np.array([kappa], dtype=np.uint64).tobytes()


def strip_mix_columns_to_sparse_rbg(
    text_bytes: bytes, coeffs: np.ndarray, p: np.uint64
) -> tuple[np.ndarray, np.ndarray, np.bytes_]:
    """Strip dense MixColumns and replace with sparse routed RBG GLUE tensor projection."""
    manifold = np.frombuffer(text_bytes, dtype=np.uint8)
    n = len(coeffs)

    phi = (1.0 + np.sqrt(5.0)) / 2.0
    spiral_strides = np.arange(n, dtype=np.float64) * phi
    indices = np.mod(spiral_strides.astype(np.int32), manifold.size)

    multipliers = np.arange(1, n + 1, dtype=np.uint64)
    v_coords = manifold[indices].astype(np.uint64) * multipliers

    v_obj = v_coords.astype(object)
    powers = multipliers.astype(object)

    dispatch_tensor = np.power(v_obj, powers)
    kappa = np.mod(np.dot(coeffs.astype(object), dispatch_tensor), int(p))

    np.random.seed(int(kappa % 2**32))

    num_active_nodes = min(max(4, int(RBG_DIM * (1.0 - SPARSITY_THRESHOLD))), n)
    row_indices = np.random.randint(0, RBG_DIM, size=num_active_nodes, dtype=np.int32)
    col_indices = np.random.randint(0, RBG_DIM, size=num_active_nodes, dtype=np.int32)

    edge_weights = (manifold[indices[:num_active_nodes]].astype(np.uint64) ^ np.uint64(kappa & 0xFF))

    sparse_rbg_matrix = np.zeros((RBG_DIM, RBG_DIM), dtype=np.uint64)
    sparse_rbg_matrix[row_indices, col_indices] = edge_weights

    active_mask = sparse_rbg_matrix > 0
    sparse_payload = sparse_rbg_matrix[active_mask].tobytes()

    return row_indices, col_indices, sparse_payload
