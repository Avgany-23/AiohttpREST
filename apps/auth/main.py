from .service import create_jwt_for_user, status_jwt_for_user, refresh_token, response_get_token
from .schema import AccessSerializer, TokenSerializer
from flask import Blueprint, jsonify
from flask_pydantic import validate


app = Blueprint('authentication', __name__, url_prefix='/auth')


@app.post(rule='/login')
@validate()
def create_access_jwt(body: AccessSerializer):
    user_tokens = create_jwt_for_user(**body.model_dump())
    return response_get_token(user_tokens)


@app.post(rule='/refresh')
@validate()
def update_tokens(body: TokenSerializer):
    new_tokens = refresh_token(**body.model_dump())
    return response_get_token(new_tokens)


@app.get(rule='/status')
@validate()
def check_status_token(body: TokenSerializer):
    status_jwt_for_user(**body.model_dump())
    return jsonify({'token': "Active"})
