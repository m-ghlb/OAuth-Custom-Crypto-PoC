# OAuth Custom Crypto PoC

## 📌 Overview
This repository contains a Proof-of-Concept (PoC) Python script demonstrating a technique to reverse-engineer and decrypt custom cryptographic handshakes used by modern SaaS applications. 

Many enterprise applications implement custom RSA + AES-CTR encryption to protect OAuth scopes in transit. This script demonstrates how a security researcher can simulate the frontend handshake, decrypt the payload, and analyze the returned OAuth scopes for misconfigurations.

## ⚙️ How it Works
1. Generates a 2048-bit RSA keypair.
2. Sends the public key to the target API endpoint.
3. Receives the encrypted symmetric key, IV, and encrypted scope payload.
4. Decrypts the symmetric key using the RSA private key.
5. Decrypts the scope payload using AES-CTR and prints the result.

## 🚀 Usage
```bash
python3 poc.py
