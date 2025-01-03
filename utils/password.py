from bcrypt import checkpw, gensalt, hashpw


salt = gensalt()


def check_password(str_psw: bytes, hash_psw: bytes) -> bool:
    return checkpw(str_psw, hash_psw)


def hash_password(password: bytes, bytes_salt: bytes = salt) -> bytes:
    return hashpw(password, bytes_salt)
