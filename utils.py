import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def pad(data): return data + b' ' * (16 - len(data) % 16)
def unpad(data): return data.rstrip(b' ')

def encrypt(data, password):
    # data sudah dalam bentuk bytes dari json.dumps(self.data).encode('utf-8')
    # Jadi, tidak perlu lagi data.encode() di sini.
    key = password.encode().ljust(32, b'\0')
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(data)) # Hapus .encode() di sini
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
            content = f.read().split(b'###DOHNA###')[0]
        with open(image_path, 'wb') as f:
            f.write(content + b'\n###DOHNA###\n' + encrypted_data)
    except Exception as e:
        error_occurred = True

    return error_occurred


def extract_from_image(image_path):
    with open(image_path, 'rb') as f:
        content = f.read()
        if b'###DOHNA###' in content:
            return content.split(b'###DOHNA###')[-1]
        return None