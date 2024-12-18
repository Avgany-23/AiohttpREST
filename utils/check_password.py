from flask_bcrypt import Bcrypt
from flask import Flask


def check_password(str_psw: str, hash_psw: str) -> bool:
    app = Flask(__name__)
    bcrypt = Bcrypt(app)
    return bcrypt.check_password_hash(hash_psw, str_psw)
