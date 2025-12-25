"""
Handles the creation and retrieval of the persistent RSA host key for the SSH server.

Ensures that the SSH honeypot uses the same host key across restarts, which
prevents SSH clients from displaying man-in-the-middle (MITM) warnings.
"""

import os
import paramiko

# Note: Storing the key in '.venv/' is not ideal as it can be wiped out.
# For a more robust implementation, consider a dedicated, git-ignored directory.
HOST_KEY_PATH = ".venv/.server.key"


def get_RSA_key() -> paramiko.RSAKey:
    
    # Ensure the directory for the host key exists.
    key_dir = os.path.dirname(HOST_KEY_PATH)
    os.makedirs(key_dir, exist_ok=True)

    if not os.path.exists(HOST_KEY_PATH):
        print(f"[-] No host key found. Generating a new one at: {HOST_KEY_PATH}")
        try:
            key = paramiko.RSAKey.generate(2048)
            key.write_private_key_file(HOST_KEY_PATH)
            print("[-] New host key generated successfully.")
        except Exception as e:
            print(f"[!] Failed to generate or write host key: {e}")
            raise
    else:
        try:
            key = paramiko.RSAKey(filename=HOST_KEY_PATH)
        except Exception as e:
            print(f"[!] Failed to load host key: {e}")
            raise
            
    return key
