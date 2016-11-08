import newClient
import base64
import Crypto
from Crypto.Cipher import AES
import pymysql

def encrypt_password(_password, key):
    """
    Encrypts the password.
    # TODO: 32 bit token as well as
    # salt the password
    """

    password = _password

    if len(password) < 16:
        for i in range(16 - len(password)):
            password += " "

    obj = AES.new(key, AES.MODE_CBC, 'This is an IV456')

    ciphertext = obj.encrypt(password)
    PASSWORD = base64.b64encode(ciphertext)
    PASSWORD = PASSWORD.decode('utf-8')

    return PASSWORD



def decrypt_password(_encrypted_password, key):

    PASSWORD = str.encode(_encrypted_password)

    PASSWORD = base64.b64decode(PASSWORD)

    obj2 = AES.new(key, AES.MODE_CBC, 'This is an IV456')
    decrypted_pasword = obj2.decrypt(PASSWORD).decode('utf-8')

    return decrypted_pasword
#
# password = "bojangle's1"
# key = "this is a key123"
#
# E = encrypt_password(password, key)
# print(decrypt_password(E, key))

import os

print(os.environ['BOJANGLES'])
