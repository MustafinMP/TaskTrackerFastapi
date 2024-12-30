import hashlib

import config


class PasswordHasher:
    def __init__(self):
        self._salt = config.PASSWORD_SALT

    def hash_password(self, password):
        return hashlib.sha256((password + self._salt).encode()).hexdigest()

    def check_password(self, stored_password, provided_password):
        return stored_password == hashlib.sha256((provided_password + self._salt).encode()).hexdigest()
