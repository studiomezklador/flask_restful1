import bcrypt
import moment
from base64 import b64encode, b64decode

class Vault:
    def __init__(self, value=None):
        if value is not None:
            self.target = value
        else:
            self.target = moment.utcnow().timezone('Europe/Paris').format('YYYY-M-D H:m').encode('utf-8')
        self.bcrypt_value = None
        self.b64_value = None

    def encrypt(self, length=10):
        self.bcrypt_value = bcrypt.hashpw(self.target, bcrypt.gensalt(length))
        self.b64_value = b64encode(self.bcrypt_value)
        return self.show()

    def show(self):
        return self.b64_value.decode()

    def is_valid(self, req_value):
        req_value = b64decode(req_value.encode('ascii'))
        # print("entry: {}\nIndoor: {}".format(req_value, self.bcrypt_value))
        return req_value == self.bcrypt_value

    def invalid(self, req_value):
        return not self.is_valid(req_value)
