from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import os
 
code = str(input('Введите кодовое слово: '))

def decrypt(filename):
    with open(filename, 'rb') as fobj:
        private_key = RSA.import_key(open('my_private_rsa_key.bin').read(),passphrase=code)
    
        enc_session_key, nonce, tag, ciphertext = [fobj.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]
    
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)
    
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
 
    new_filename = 'decrypted/' + filename[0:filename.rfind('.')] + '_decrypted' + filename[filename.rfind('.'):len(filename)]
    f = open(new_filename, 'wb')
    f.write(data)
    f.close()

if not os.path.exists('decrypted'):
        os.makedirs('decrypted')
for filename in os.listdir(os.path.dirname(os.path.abspath(__file__))):  
    if filename != 'my_private_rsa_key.bin' and filename != 'decrypt.py' and filename != 'decrypted':
        decrypt(filename)
