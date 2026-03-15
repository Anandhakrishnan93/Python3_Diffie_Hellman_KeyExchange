The Diffie-Hellman (DH) algorithm is a foundational key exchange protocol. It allows two parties (usually called Alice and Bob) to generate a shared secret over an insecure channel without ever actually sending the secret itself.
In Python, implement this using basic modular exponentiation (g^a mod p).

Important Implementation Notessecrets vs random: Always use the secrets module for cryptography. The standard random module is pseudo-random and predictable, which would make your private keys hackable.

Prime Size: In the real world, your prime $p$ should be at least 2048 bits long to be considered secure against modern computing power.

The "Man-in-the-Middle" (MitM) Attack: DH by itself does not authenticate who you are talking to. An attacker could sit in the middle, pretend to be Bob to Alice, and pretend to be Alice to Bob. Usually, DH is paired with digital signatures (like RSA or ECDSA) to verify identities.

The Double Ratchet Algorithm is the gold standard for secure messaging (used by Signal, WhatsApp, and Matrix). It provides End-to-End Encryption (E2EE) with two critical properties:

Forward Secrecy: If a key is stolen today, past messages remain safe.

Post-Quantum Resistance (Break-in Recovery): If a key is stolen today, the system "heals" itself so future messages become secure again.


1. How the "Ratchet" Works
The name comes from a mechanical ratchet that only turns one way. In cryptography, this means once a key is used, it is deleted and replaced by a new one that cannot be used to derive the old one.

It combines two types of "ratchets":

The KDF (Symmetric) Ratchet: For every message sent, the "Chain Key" turns once to create a "Message Key."

The Diffie-Hellman (Asymmetric) Ratchet: Every time a response is received, a new DH exchange happens to create a brand new "Root Key."

2. Why This is Superior
If an attacker steals Alice's phone after the first two messages, they only have the current root_key.

They cannot calculate the keys for "Hello Bob" because the symmetric ratchet deleted them (Forward Secrecy).

Once Bob sends a new DH key and Alice performs receive_response(), the attacker's stolen root_key becomes useless for future messages (Post-Quantum/Break-in Recovery).