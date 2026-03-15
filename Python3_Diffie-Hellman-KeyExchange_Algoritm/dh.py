import secrets
#  implement this using basic modular exponentiation (g^a mod p).
# 1. Agree,Both agree on a large prime p and a generator g.,(Publicly known)
# 2. Private Key,Chooses a secret integer a.,Chooses a secret integer b.
# 3. Public Key,Computes A=ga(modp).,Computes B=gb(modp).
# 4. Exchange,Glen sends A to Tom.,Tom sends B to Glen.
# 5. Shared Secret,Computes S=Ba(modp).,Computes S=Ab(modp).

def diffie_hellman():
    # 1. Publicly shared parameters (RFC 3526 Group 14 - 2048-bit prime)
    # In a real app, use a standard large prime. For this example, we use a smaller one.
    p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1 # Example Prime
    g = 2 # Common generator

    # 2. Glen generates her private and public keys
    glen_private = secrets.randbelow(p)
    glen_public = pow(g, glen_private, p)

    # 3. Tom generates his private and public keys
    tom_private = secrets.randbelow(p)
    tom_public = pow(g, tom_private, p)

    # --- SIMULATE EXCHANGE ---
    
    # 4. Glen computes the shared secret using Tom's public key
    glen_shared_secret = pow(tom_public, glen_private, p)

    # 5. Tom computes the shared secret using Glen's public key
    tom_shared_secret = pow(glen_public, tom_private, p)

    print(f"Alice's Secret: {hex(glen_shared_secret)[:20]}...")
    print(f"Bob's Secret:   {hex(tom_shared_secret)[:20]}...")
    
    return glen_shared_secret == tom_shared_secret

if __name__ == "__main__":
    if diffie_hellman():
        print("Success! Shared secrets match.")