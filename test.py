import newClient
import base64

password = str.encode("tits")

encoded = base64.b64encode(password)

print(encoded.decode('utf-8'))

decoded = base64.b64decode(encoded)

print(decoded)
