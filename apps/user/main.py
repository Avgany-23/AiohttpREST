from .schema import RegistrationSerializer
from .service import registration_user
from flask import Blueprint, jsonify
from .service import check_user
import flask_pydantic


app = Blueprint('user', __name__, url_prefix='/user')


@app.get('/check/<username>')
def check_registration(username: str):
    if check_user(username):
        return jsonify({"Success found": "Пользователь %s зарегистрирован" % username})
    else:
        response = jsonify({"Not found user": "Пользователь %s не нашелся" % username})
        response.status_code = 404
        return response


@app.post('/registration')
@flask_pydantic.validate()
def registration(body: RegistrationSerializer):
    registration_user(body.model_dump())
    response = jsonify({"User status": "Success created"})
    response.status_code = 201
    return response
