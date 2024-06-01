import json

from flask import Blueprint, request
from sqlmodel import Session, select

import db_models
from db import engine
from geodetic_monument_finder.models.network_response import NetworkResponse, NetworkingStatus, HttpStatusCode

bp = Blueprint('monuments', __name__, url_prefix='/monuments')


@bp.route('/', methods=['GET'])
def get_monuments():
    try:
        with Session(engine) as session:
            statement = select(db_models.Monuments)
            result = session.exec(statement).all()
            return NetworkResponse(
                status=NetworkingStatus.SUCCESS.value,
                message="Monuments Retrieved!",
                data=[monument.to_json() for monument in result],
                is_exception=False,
                error_message=None
            ).to_json(), HttpStatusCode.OK.value,
    except Exception as e:
        return NetworkResponse(
            status=NetworkingStatus.FAILED.value,
            message="Failed to get monuments",
            data=None,
            is_exception=True,
            error_message=str(e)
        ).to_json(), HttpStatusCode.EXCEPTION.value,


@bp.route('condition/<monument_id>', methods=['PUT'])
def update_monument_condition(monument_id):
    try:
        data = request.get_json()

        with Session(engine) as session:
            statement = select(db_models.Monuments).where(db_models.Monuments.id == monument_id)
            monument = session.exec(statement).one()
            monument.condition = data["condition"]

            session.add(monument)
            session.commit()
            session.refresh(monument)

            return NetworkResponse(
                status=NetworkingStatus.SUCCESS.value,
                message="Monument Updated!",
                data=monument.to_json(),
                is_exception=False,
                error_message=None
            ).to_json(), HttpStatusCode.OK.value,

    except Exception as e:
        return NetworkResponse(
            status=NetworkingStatus.FAILED.value,
            message="Failed to update monument",
            data=None,
            is_exception=True,
            error_message=str(e)
        ).to_json(), HttpStatusCode.EXCEPTION.value,
