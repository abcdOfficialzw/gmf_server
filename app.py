import os
from random import randint
from flask_cors import CORS,cross_origin


from sqlmodel import SQLModel, Session, select

import db_models
from db import engine

from geodetic_monument_finder import create_app
from geodetic_monument_finder.monuments import monuments


from geodetic_monument_finder.models.network_response import NetworkResponse, NetworkingStatus, HttpStatusCode
from geodetic_monument_finder.reports import reports
from raw_database import DATABASE

app = create_app()
CORS(app)

# Create Database Tables
SQLModel.metadata.create_all(engine)


app.register_blueprint(reports.bp)
app.register_blueprint(monuments.bp)




# Populate Database Tables

@app.route("/", methods=["GET"])
@cross_origin(supports_credentials=True)
def hello():
    with Session(engine) as session:
        statement = select(db_models.Test2)
        result = session.exec(statement).all()
        return NetworkResponse(
            status=NetworkingStatus.SUCCESS.value,
            message="Hello World",
            data=[test2.to_json() for test2 in result],
            is_exception=False,
            error_message=None
        ).to_json(), HttpStatusCode.OK.value,





@app.route("/populate", methods=["GET"])
def populate():

    conditions = ["MISSING", "DAMAGED", "GOOD"]
    monument_images = ["https://th.bing.com/th/id/OIP.kRTSB1eMfyt_kT-yrLLnCgHaJ4?w=675&h=900&rs=1&pid=ImgDetMain", "https://th.bing.com/th/id/OIP.IA8Uu-qkntysI3BLoSPYtQAAAA?w=320&h=240&rs=1&pid=ImgDetMain","https://th.bing.com/th/id/R.a6b88261342c63fee812ac7b39a1c2b9?rik=pJb7bkWdtn2I4g&riu=http%3a%2f%2fphotos1.blogger.com%2fblogger%2f4606%2f983%2f1024%2fPA290003.jpg&ehk=hO5MuiFIS6Yam1oh993MrmeS%2faFcvMbHROjBAhl2DS8%3d&risl=&pid=ImgRaw&r=0", "https://th.bing.com/th/id/R.cd15bb4544dfebe21828bc5ab8e395c8?rik=Wx3gGMDGXQ%2fzPQ&riu=http%3a%2f%2fwww.alexkershaw.com.au%2fimages%2ffullsize%2fGeodetic07_big.jpg&ehk=0H9J5TCuO7o%2bZ%2ba5P7lw%2bnVosP6kjswRLM%2bp6M2jUFM%3d&risl=&pid=ImgRaw&r=0", "https://thumbs.dreamstime.com/b/survey-mark-found-ground-detail-marker-also-called-monument-geodetic-74245078.jpg", "https://s0.geograph.org.uk/geophotos/03/55/05/3550547_407fea12.jpg"]



    for database in DATABASE:
        print(f"Adding {database['MONUNUM']} to Database")
        with Session(engine) as session:
            gauss = db_models.GaussPoints(
                gauss_lo=database["GAUSS_LO"],
                gauss_x=database["GAUSS_X"],
                gauss_y=database["GAUSS_Y"]
            )
            session.add(gauss)
            session.commit()

            wgs84 = db_models.WGS84Points(
                wgs84_lat=database["LAT_WGS84"],
                wgs84_lon=database["LON_WGS84"]
            )
            session.add(wgs84)
            session.commit()

            utm = db_models.UTMPoints(
                utm_cm=database["UTM_CM"],
                utm_north=database["UTM_N"],
                utm_east=database["UTM_E"]
            )
            session.add(utm)
            session.commit()

            delta = db_models.DeltaPoints(
                delta_lat = database["DELTA_LAT"],
                delta_lon = database["DELTA_LON"],
                delta_x=database["DELTA_X"],
                delta_y=database["DELTA_Y"],
                delta_e=database["DELTA_E"],
                delta_n=database["DELTA_N"]

            )
            session.add(delta)
            session.commit()

            index = randint(0, 2)
            image_index = randint(0, len(monument_images) - 1)

            monument = db_models.Monuments(
                monument_name=database["MONUNUM"],
                topo=database["TOPO"],
                condition = conditions[index],
                monument_image=monument_images[image_index],
                gauss_id=gauss.id,
                wgs84_id=wgs84.id,
                utm_id=utm.id,
                delta_id=delta.id

            )
            session.add(monument)
            session.commit()
        print(f"Added to Database")
    print("Database Populated")
    with Session(engine) as session:
        statement = select(db_models.Monuments)
        result = session.exec(statement).all()
        return NetworkResponse(
            status=NetworkingStatus.SUCCESS.value,
            message="Database Populated!",
            data=[monument.to_json() for monument in result],
            is_exception=False,
            error_message=None
        ).to_json(), HttpStatusCode.OK.value,



    return "Populating Database"



@app.errorhandler(403)
def forbidden(e):
    return NetworkResponse(
        status=NetworkingStatus.FAILED.value,
        message="Forbidden Access",
        data=None,
        is_exception=True,
        error_message=str(e)
    ).to_json(), HttpStatusCode.FORBIDEN.value,


@app.errorhandler(404)
def forbidden(e):
    return NetworkResponse(
        status=NetworkingStatus.FAILED.value,
        message="ENDPOINT NOT FOUND",
        data=None,
        is_exception=True,
        error_message=str(e)
    ).to_json(), HttpStatusCode.NOT_FOUND.value,


@app.errorhandler(401)
def unauthorized(e):
    return NetworkResponse(
        status=NetworkingStatus.FAILED.value,
        message="Unauthorized Access",
        data=None,
        is_exception=True,
        error_message=str(e)
    ).to_json(), HttpStatusCode.UNAUTHORIZED.value,


if __name__ == '__main__':
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int(os.environ.get('PORT', 5000))
    )
