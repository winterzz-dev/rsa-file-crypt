from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import os
import random

def crypt(filename):
    result = False
    new_filename = 'crypted/' + filename[0:filename.rfind('.')] + '_crypted' + filename[filename.rfind('.'):len(filename)]
    if(os.path.isfile(new_filename) != True):
        with open(new_filename, 'wb') as out_file:
            recipient_key = RSA.import_key(open('my_rsa_public.pem').read())
            session_key = get_random_bytes(16)
            cipher_rsa = PKCS1_OAEP.new(recipient_key)
            out_file.write(cipher_rsa.encrypt(session_key))
            cipher_aes = AES.new(session_key, AES.MODE_EAX)
            data = open(filename, 'rb').read()
            ciphertext, tag = cipher_aes.encrypt_and_digest(data)
            out_file.write(cipher_aes.nonce)
            out_file.write(tag)
            out_file.write(ciphertext)
            result = True
    return result

if not os.path.exists('crypted'):
        os.makedirs('crypted')
for filename in os.listdir(os.path.dirname(os.path.abspath(__file__))):  
    if filename != 'my_rsa_public.pem' and filename != 'crypt.py' and filename != 'crypted':
        crypt(filename)
