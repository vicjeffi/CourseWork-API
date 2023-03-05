import base64
import hashlib
import hmac

class PSWHash256:
    def __init__(self, secret_key):
        self.secret_key = secret_key
    def getHash(self, passwrd):
        passwrd = str.encode(passwrd)
        hash_psw = hmac.new(self.secret_key, msg=passwrd, digestmod=hashlib.sha256).digest()
        return base64.b64encode(hash_psw).decode()