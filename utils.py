import base64
import json
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def pad(data): return data + b' ' * (16 - len(data) % 16)
def unpad(data): return data.rstrip(b' ')

def encrypt(data, password):
    key = password.encode().ljust(32, b'\0')
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(data.encode()))
    return base64.b64encode(iv + encrypted)

def decrypt(enc_data, password):
    key = password.encode().ljust(32, b'\0')
    try:
        raw = base64.b64decode(enc_data)
        iv = raw[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(raw[16:])
        return unpad(decrypted).decode()
    except:
        return None

def embed_to_image(image_path, encrypted_data):
    error_occurred = False
    try:
        with open(image_path, 'rb') as f:
            content = f.read().split(b'###DATA###')[0]
        with open(image_path, 'wb') as f:
            f.write(content + b'\n###DATA###\n' + encrypted_data)
    except Exception as e:
        error_occurred = True

    return error_occurred


def extract_from_image(image_path):
    with open(image_path, 'rb') as f:
        content = f.read()
        if b'###DATA###' in content:
            return content.split(b'###DATA###')[-1]
        return None