from flask import Blueprint, request
from sqlmodel import Session, select, col

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
            statement = select(db_models.Reports).limit(per_page).offset(page * per_page).order_by(
                db_models.Reports.is_resolved.asc())
            reports = session.exec(statement).all()

            return NetworkResponse(
                status=NetworkingStatus.SUCCESS.value,
                message="Successfully fetched Reports",
                data={
                    "reports": [report.to_json() for report in reports],
                    "total": len(reports),
                    "is_empty": len(reports) == 0,
                    "page": page,
                    "per_page": per_page
                },
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


@bp.route('/search', methods=["GET", "POST"])
def get_report_by_monument_name():
    try:
        page = request.args.get('page', default=0, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        data = request.get_json()
        monument_name = data['monument_name']

        with Session(engine) as session:
            statement = select(db_models.Reports).join(db_models.Monuments).where(
                col(db_models.Monuments.monument_name).contains(monument_name))

            reports = session.exec(statement).all()

            return NetworkResponse(
                status=NetworkingStatus.SUCCESS.value,
                message="Successfully fetched Reports",
                data={
                    "reports": [report.to_json() for report in reports],
                    "total": len(reports),
                    "is_empty": len(reports) == 0,
                    "page": page,
                    "per_page": per_page
                },
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


@bp.route('/resolve', methods=["PUT"])
def resolve_report():
    try:
        data = request.get_json()
        condition = data["condition"]
        monument_id = data["monument_id"]

        with Session(engine) as session:
            statement = select(db_models.Monuments).where(db_models.Monuments.id == monument_id)
            monument = session.exec(statement).one()

            monument.condition = condition
            session.add(monument)
            session.commit()
            session.refresh(monument)

            statement = select(db_models.Reports).join(db_models.Monuments).where(
                db_models.Reports.monument_id == monument_id)
            reports = session.exec(statement).all()
            for report in reports:
                report.is_resolved = True
                session.add(report)
                session.commit()
                session.refresh(report)

            return NetworkResponse(
                status=NetworkingStatus.SUCCESS.value,
                message=f"Resolved {len(reports)} reports for monument {monument_id}",
                data={},
                is_exception=False,
                error_message=None
            ).to_json(), HttpStatusCode.OK.value,

    except Exception as e:
        return NetworkResponse(
            status=NetworkingStatus.FAILED.value,
            message="Failed to resolve report",
            data=None,
            is_exception=True,
            error_message=str(e)
        ).to_json(), HttpStatusCode.EXCEPTION.value,


@bp.route('', methods=["POST"])
def create_report():
    try:
        data = request.get_json()
        monument_id = data["monument_id"]
        condition = data["condition"]

        with Session(engine) as session:
            # statement = select(db_models.Reports).where(db_models.Reports.monument_id == monument_id).where(
            #     db_models.Reports.condition == condition)
            # result = session.exec(statement).all()
            #
            # if len(result)> 0:
            #     return NetworkResponse(
            #         status=NetworkingStatus.FAILED.value,
            #         message=f"This monument has already been reported as {condition}, contact the Administrator to confirm it's status",
            #         data=None,
            #         is_exception=False,
            #         error_message=None
            #     ).to_json(), HttpStatusCode.OK.value,
            # else:
            new_report = db_models.Reports(
                monument_id=monument_id,
                condition=condition
            )
            session.add(new_report)
            session.commit()
            session.refresh(new_report)

            return NetworkResponse(
                status=NetworkingStatus.SUCCESS.value,
                message=f"Monument Reported as {condition}",
                data=new_report.to_json(),
                is_exception=False,
                error_message=None
            ).to_json(), HttpStatusCode.OK.value,

    except Exception as e:
        return NetworkResponse(
            status=NetworkingStatus.FAILED.value,
            message="Failed to create report",
            data=None,
            is_exception=True,
            error_message=str(e)
        ).to_json(), HttpStatusCode.EXCEPTION.value,