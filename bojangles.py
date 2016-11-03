from Crypto.Cipher import AES

def encrypt_password(password, key):
	"""
    Takes a string of any length and encrypts it
    by breaking it down into multiple 
    components of 16 or fewer characters.
    #TODO: Figure out how to deal with long (>16) passwords
	"""
	if len(password) > 16:
		return False

	else:
		encrypter = AES.new(key, AES.MODE_CBC, 'This is an IV456')
		
		# Onyen must be 16 characters
		chars_added = 16 - len(password)

	    # Pad with spaces
		for i in range(0, chars_added):
			password += " "

		encrypted_password = encrypter.encrypt(password)

		return encrypted_password


def decrypt_password(encrypted_password, key):
	"""
	Takes encrypted password and decodes. Then removes padding for spaces.
	#TODO: Figure out how to deal with long (>16) passwords
	"""
	decrypter = AES.new(key, AES.MODE_CBC, 'This is an IV456')

	decrypted_password = decrypter.decrypt(encrypted_password).decode('utf-8')

	while decrypted_password[-1] == " ":
		decrypted_password = decrypted_password[0:len(decrypted_password)-1]

	return decrypted_password

password = "bojangles6'"
key = "Tq8eGl70L0MFTSB0ywWFtits"

E = encrypt_password(password, key)
print(len(E))
print(E)
z = decrypt_password(E, key)

print(z)