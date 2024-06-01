import datetime
import json
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, List


class Monuments(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    monument_name: str
    topo: str
    condition: str
    monument_image: str
    gauss_id: int = Field(foreign_key="gausspoints.id")
    wgs84_id: int = Field(foreign_key="wgs84points.id")
    utm_id: int = Field(foreign_key="utmpoints.id")
    delta_id: int = Field(foreign_key="deltapoints.id")

    # Relationships
    reports: List["Reports"] = Relationship(back_populates="monument")
    gausspoints: Optional["GaussPoints"] = Relationship(back_populates="monuments")
    wgs84points: Optional["WGS84Points"] = Relationship(back_populates="monuments")
    utmpoints: Optional["UTMPoints"] = Relationship(back_populates="monuments")
    deltapoints: Optional["DeltaPoints"] = Relationship(back_populates="monuments")

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)

        # Handling nested JSON objects for related points
        if 'gausspoints' in json_dict and json_dict['gausspoints'] is not None:
            json_dict['gausspoints'] = GaussPoints.from_json(json.dumps(json_dict['gausspoints']))

        if 'wgs84points' in json_dict and json_dict['wgs84points'] is not None:
            json_dict['wgs84points'] = WGS84Points.from_json(json.dumps(json_dict['wgs84points']))

        if 'utmpoints' in json_dict and json_dict['utmpoints'] is not None:
            json_dict['utmpoints'] = UTMPoints.from_json(json.dumps(json_dict['utmpoints']))

        if 'deltapoints' in json_dict and json_dict['deltapoints'] is not None:
            json_dict['deltapoints'] = DeltaPoints.from_json(json.dumps(json_dict['deltapoints']))

        return cls(**json_dict)

    def to_json(self):
        return {
            "id": self.id,
            "monument_name": self.monument_name,
            "topo": self.topo,
            "condition": self.condition,
            "monument_image": self.monument_image,
            "gauss_id": self.gauss_id,
            "wgs84_id": self.wgs84_id,
            "utm_id": self.utm_id,
            "delta_id": self.delta_id,

            # onjects
            "gausspoints": self.gausspoints.to_json(),
            "wgs84points": self.wgs84points.to_json(),
            "utmpoints": self.utmpoints.to_json(),
            "deltapoints": self.deltapoints.to_json()

        }


class Reports(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    monument_id: int = Field(foreign_key="monuments.id")
    condition: str
    is_resolved: bool = Field(default=False)

    # Relationships
    monument: Optional["Monuments"] = Relationship(back_populates="reports")


    def to_json(self):
        return {
            "id": self.id,
            "monument_id": self.monument_id,
            "condition": self.condition,
            "is_resolved" : self.is_resolved,
            "monument": self.monument.to_json()
        }

class GaussPoints(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    gauss_lo: str
    gauss_x: str
    gauss_y: str

    # Relationships
    monuments: List["Monuments"] = Relationship(back_populates="gausspoints")

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)

    def to_json(self):
        return {
            "id": self.id,
            "gauss_lo": self.gauss_lo,
            "gauss_x": self.gauss_x,
            "gauss_y": self.gauss_y
        }


class WGS84Points(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    wgs84_lat: str
    wgs84_lon: str

    # Relationships
    monuments: List["Monuments"] = Relationship(back_populates="wgs84points")

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)

    def to_json(self):
        return {
            "id": self.id,
            "wgs84_lat": self.wgs84_lat,
            "wgs84_lon": self.wgs84_lon
        }


class UTMPoints(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    utm_cm: str
    utm_north: str
    utm_east: str

    # Relationships
    monuments: List["Monuments"] = Relationship(back_populates="utmpoints")

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)

    def to_json(self):
        return {
            "id": self.id,
            "utm_cm": self.utm_cm,
            "utm_north": self.utm_north,
            "utm_east": self.utm_east
        }


class DeltaPoints(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    delta_lat: str
    delta_lon: str
    delta_x: str
    delta_y: str
    delta_e: str
    delta_n: str

    # Relationships
    monuments: List["Monuments"] = Relationship(back_populates="deltapoints")

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)

    def to_json(self):
        return {
            "id": self.id,
            "delta_lat": self.delta_lat,
            "delta_lon": self.delta_lon,
            "delta_x": self.delta_x,
            "delta_y": self.delta_y,
            "delta_e": self.delta_e,
            "delta_n": self.delta_n
        }


class Test(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    date: datetime.datetime

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date
        }


class Test2(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    date: datetime.datetime

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)
        return cls(**json_dict)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date
        }
