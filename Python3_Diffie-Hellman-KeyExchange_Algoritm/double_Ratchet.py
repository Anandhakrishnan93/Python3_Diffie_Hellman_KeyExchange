import hashlib
import hmac
import secrets

def kdf(key, data):
    """Simple HMAC-based Key Derivation Function"""
    return hmac.new(key, data, hashlib.sha256).digest()

class RatchetNode:
    def __init__(self, shared_root_key):
        self.root_key = shared_root_key
        self.send_chain_key = None
        self.recv_chain_key = None
        
        # DH Keys for the asymmetric ratchet
        self.dh_private = secrets.token_bytes(32)
        self.dh_public = self._derive_public(self.dh_private)
        self.remote_dh_public = None

    def _derive_public(self, priv):
        # Simplification: In reality, use Curve25519
        return hashlib.sha256(priv).digest()

    def send_message(self, plaintext):
        """The Symmetric Ratchet Step"""
        # 1. Turn the ratchet: Derive Message Key and New Chain Key
        self.send_chain_key = kdf(self.send_chain_key or self.root_key, b"ratchet-step")
        message_key = kdf(self.send_chain_key, b"message-key")
        
        # 2. Encrypt (Simulated)
        print(f"Sending with Message Key: {message_key.hex()[:10]}...")
        return f"ENCRYPTED({plaintext})"

    def receive_response(self, new_remote_dh_public):
        """The Diffie-Hellman Ratchet Step (Break-in Recovery)"""
        self.remote_dh_public = new_remote_dh_public
        
        # 1. Perform DH Exchange
        dh_out = hmac.new(self.dh_private, self.remote_dh_public, hashlib.sha256).digest()
        
        # 2. Update the Root Key
        self.root_key = kdf(self.root_key, dh_out)
        
        # 3. Reset the Sending/Receiving chains with the new entropy
        self.send_chain_key = kdf(self.root_key, b"send")
        self.recv_chain_key = kdf(self.root_key, b"recv")
        print("DH Ratchet turned. Root key updated.")

# --- Simulation ---
shared_secret = b"initial_handshake_secret_from_DH"
alice = RatchetNode(shared_secret)

# Alice sends a few messages (Symmetric Ratchet)
alice.send_message("Hello Bob")
alice.send_message("How are you?")

# Alice receives a reply with a new DH key from Bob (DH Ratchet)
bob_new_key = secrets.token_bytes(32)
alice.receive_response(bob_new_key)

# Future messages use a completely refreshed key chain
alice.send_message("Glad you replied!")