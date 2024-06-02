import json

from flask import Blueprint, request
from sqlmodel import Session, select, col

import db_models
from db import engine
from geodetic_monument_finder.models.network_response import NetworkResponse, NetworkingStatus, HttpStatusCode

bp = Blueprint('monuments', __name__, url_prefix='/monuments')


@bp.route('', methods=['GET'])
def get_monuments():
    try:
        page = request.args.get('page', default=0, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        with Session(engine) as session:
            statement = select(db_models.Monuments).limit(per_page).offset(page * per_page).order_by(
                db_models.Monuments.id.asc())
            result = session.exec(statement).all()
            return NetworkResponse(
                status=NetworkingStatus.SUCCESS.value,
                message="Monuments Retrieved!",
                data={
                    "monuments": [monument.to_json() for monument in result],
                    "total": len(result),
                    "is_empty": len(result) == 0,
                    "page": page,
                    "per_page": per_page
                },
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


@bp.route("/search", methods=['GET'])
def get_monument_by_name():
    try:
        data = request.get_json()
        monument_name = data["monument_name"]
        print("Monument Name: ", monument_name)
        page = request.args.get('page', default=0, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        with Session(engine) as session:
            statement = select(db_models.Monuments).where(
                col(db_models.Monuments.monument_name).contains(monument_name)).limit(per_page).offset(page * per_page).order_by(db_models.Monuments.id.asc())
            result = session.exec(statement).all()
            return NetworkResponse(
                status=NetworkingStatus.SUCCESS.value,
                message="Monument Retrieved!",
                data={
                    "monuments": [monument.to_json() for monument in result],
                    "total": len(result),
                    "is_empty": len(result) == 0,
                    "page": page,
                    "per_page": per_page
                },
                is_exception=False,
                error_message=None
            ).to_json(), HttpStatusCode.OK.value,
    except Exception as e:
        return NetworkResponse(
            status=NetworkingStatus.FAILED.value,
            message="Failed to get monument",
            data=None,
            is_exception=True,
            error_message=str(e)
        ).to_json(), HttpStatusCode.EXCEPTION.value,
