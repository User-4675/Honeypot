import paramiko
import os

HOST_KEY_PATH = ".venv/.server.key"

def get_RSA_key():
    # Create directories if they don't exist
    os.makedirs(os.path.dirname(HOST_KEY_PATH), exist_ok=True)
    if not os.path.exists(HOST_KEY_PATH):
        # Generate key and store it
        key = paramiko.RSAKey.generate(2048)
        key.write_private_key_file(HOST_KEY_PATH)
    else:
        # Retrieve key from file
        key = paramiko.RSAKey(filename=HOST_KEY_PATH)
    return key
