from flask import Blueprint, request
from sqlmodel import Session, select

import db_models
from db import engine
from geodetic_monument_finder.models.network_response import NetworkResponse, NetworkingStatus, HttpStatusCode

bp = Blueprint('reports', __name__, url_prefix='/reports')


@bp.route('/', methods=["GET"])
def get_reports():
    try:

        page = request.args.get('page', default=0, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        with Session(engine) as session:
            statement = select(db_models.Reports).limit(per_page).offset(page * per_page)
            reports = session.exec(statement).all()

            return NetworkResponse(
                status=NetworkingStatus.SUCCESS.value,
                message="Successfully fetched Reports",
                data=[report.to_json() for report in reports],
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
