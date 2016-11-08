import base64
import Crypto
from Crypto.Cipher import AES
import pymysql

# for heroku: key = os.environ.get('BOJANGLES')


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

    if type(_encrypted_password) == bytes:
        PASSWORD = _encrypted_password
    elif type(_encrypted_password) == str:
        PASSWORD = str.encode(_encrypted_password)


    PASSWORD = base64.b64decode(PASSWORD)

    obj2 = AES.new(key, AES.MODE_CBC, 'This is an IV456')
    DECRYPTED_PASSWORD = obj2.decrypt(PASSWORD).decode('utf-8')

    while DECRYPTED_PASSWORD[-1] == " ":
        DECRYPTED_PASSWORD = DECRYPTED_PASSWORD[0:len(DECRYPTED_PASSWORD)-1]

    return DECRYPTED_PASSWORD

# key = 'sduID72S14D47d8N'
