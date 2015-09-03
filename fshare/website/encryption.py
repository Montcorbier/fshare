import hashlib
from random import randint
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

CHUNK_SIZE = 24*1024

def encrypt_file(filepath, file_content, pwd):
    # Generate a random IV
    iv = str.encode("".join([chr(randint(0, 127)) for i in range(16)]))
    # Derive a key from "human" password
    key = PBKDF2(pwd, iv)
    # Create a AES encryptor object
    enc = AES.new(key, AES.MODE_CBC, iv)
    # Create a MD5 hasher for file checksum
    m = hashlib.md5()
    # Open destination for write
    with open(filepath, 'wb+') as dest:
        # Iteration chunk by chunk
        while True:
            # Getting bytes from file
            chunk = file_content.read(CHUNK_SIZE)
            # Update md5
            m.update(chunk)
            # Detect EOF
            if len(chunk) == 0:
                break
            # Add padding if needed
            elif len(chunk) % 16 != 0:
                chunk += str.encode(' ' * (16 - len(chunk) % 16))
            # Write to destination encrypted chunk
            dest.write(enc.encrypt(chunk))
    # Return iv used for encryption (need to be stored in DB)
    return iv, m.hexdigest()

def decrypt_file(file_object, pwd):
    # Getting iv from DB
    iv = file_object.iv
    # Derive a key from "human" password and iv
    key = PBKDF2(pwd, iv.encode("utf-8"))
    # Create a AES decryptor object
    dec = AES.new(key, AES.MODE_CBC, iv.encode("utf-8"))
    # Content of the deciphered file to be filled chunk by chunk
    content = b""

    # Open source file
    with open(file_object.path, 'rb') as f:
        # Iteration on each chunk
        i = 0
        while True:
            i += 1
            # Getting bytes from file
            chunk = f.read(1024*1024)
            # Detect EOF
            if len(chunk) == 0:
                break
            # Decrypt chunk
            content += dec.decrypt(chunk)
            if i % 100 == 0:
                print(len(content))
    # Return deciphered content truncated by the padding
    return content[:file_object.size]
