from sqlalchemy.orm import Session
from flask_bcrypt import Bcrypt
from db import connect_psql
from .models import User
import flask


@connect_psql(auto_commit=True)
def registration_user(data: dict, session: Session) -> None:
    password = hash_password(data.pop('password'))
    user = User(**data, password=password)
    session.add(user)
    session.commit()


def hash_password(password: str) -> str:
    app = flask.Flask(__name__)
    bcrypt = Bcrypt(app)
    return bcrypt.generate_password_hash(password).decode()


@connect_psql()
def check_user(username: str, session: Session) -> bool:
    if session.query(User).filter_by(username=username).first():
        return True
    return False
