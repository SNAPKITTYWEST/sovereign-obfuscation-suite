import os
from cryptography.fernet import Fernet

from .quantum_collapse import QuantumCollapseSystem


class GhostMirrorSystem(QuantumCollapseSystem):
    """Implements a Ghost-Mirror backup.

    Collapsed data is shifted to a hidden dimension for sovereign recovery.
    """

    def __init__(self, secret_key: str, entanglement_key: str, master_key: bytes):
        super().__init__(secret_key, entanglement_key)
        self.master_key = master_key
        self.cipher = Fernet(master_key)
        self.ghost_mirror = {}

    def _collapse(self, text_id: str):
        shadow_word = self.server_storage.get(text_id)

        if shadow_word and self.fuse_state.get(text_id) == "INTACT":
            encrypted_shadow = self.cipher.encrypt(shadow_word.encode())
            self.ghost_mirror[text_id] = encrypted_shadow
            print(f"Sovereign Shift: Shadow Word for {text_id} moved to Ghost Mirror.")

        noise = os.urandom(32).hex()
        self.server_storage[text_id] = noise
        self.fuse_state[text_id] = "COLLAPSED"
        print(f"!!! PRIMARY COLLAPSE COMPLETE for {text_id} !!!")

    def sovereign_recovery(self, text_id: str):
        """Recover the collapsed shadow word using the Master Key."""
        if text_id not in self.ghost_mirror:
            print("Recovery failed: No ghost image found in the mirror.")
            return False

        print(f"Initiating Sovereign Recovery for {text_id}...")
        encrypted_shadow = self.ghost_mirror[text_id]
        decrypted_shadow = self.cipher.decrypt(encrypted_shadow).decode()

        self.server_storage[text_id] = decrypted_shadow
        self.fuse_state[text_id] = "INTACT"

        del self.ghost_mirror[text_id]
        print("Restoration successful. State returned to INTACT.")
        return True
