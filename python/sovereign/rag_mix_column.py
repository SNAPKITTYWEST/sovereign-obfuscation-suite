import numpy as np


class QuantumRAGMixColumn:
    """Quantum-entangled MixColumn transformation.

    Combines AES finite-field matrix mixing with RAG-weighted vector superposition.
    """

    def __init__(self, theta: float = 89 / 2462):
        self.theta = theta
        self.base_matrix = np.array([
            [2, 3, 1, 1],
            [1, 2, 3, 1],
            [1, 1, 2, 3],
            [3, 1, 1, 2],
        ], dtype=np.uint8)

    def _galois_mult(self, a: int, b: int) -> int:
        p = 0
        for _ in range(8):
            if b & 1:
                p ^= a
            hi_bit_set = a & 0x80
            a = (a << 1) & 0xFF
            if hi_bit_set:
                a ^= 0x1B
            b >>= 1
        return p

    def apply_quantum_phase_modulation(self, column: np.ndarray) -> np.ndarray:
        modulated = np.zeros_like(column, dtype=np.uint8)
        for i, val in enumerate(column):
            phase_shift = int((val * self.theta * (i + 1)) % 256)
            modulated[i] = val ^ phase_shift
        return modulated

    def mix_column(self, column: list[int], context_vector: list[float] = None) -> list[int]:
        if len(column) != 4:
            raise ValueError("Column must consist of exactly 4 state bytes.")

        col_arr = np.array(column, dtype=np.uint8)
        modulated_col = self.apply_quantum_phase_modulation(col_arr)

        output = [0, 0, 0, 0]
        for i in range(4):
            val = 0
            for j in range(4):
                coeff = self.base_matrix[i, j]
                val ^= self._galois_mult(coeff, int(modulated_col[j]))

            if context_vector and len(context_vector) == 4:
                rag_weight = int((context_vector[i] * 255)) % 256
                val ^= rag_weight

            output[i] = val

        return output
