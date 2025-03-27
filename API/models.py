from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#from sqlalchemy.ext import serializer

db = SQLAlchemy()


class Serializer:
    @staticmethod
    def serialize(obj):
        """Convert SQLAlchemy object to JSON"""
        return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}


class BreachDocument(db.Model):
    __tablename__ = "breachdocumentsnew"
    #__table_args__={"schema": __SCHEMA__}
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, nullable=True, default=None)  # Allow NULL values
    alert_type = db.Column(db.String(255), nullable=True)
    value = db.Column(db.Integer, nullable=True)
    currency = db.Column(db.String(10), nullable=True)
    breach_trigger = db.Column(db.Text, nullable=True)
    region = db.Column(db.String(100), nullable=True)
    kpi_relevant = db.Column(db.String(255), nullable=True)
    genuine = db.Column(db.String(255), nullable=True)
    remarks = db.Column(db.Text, nullable=True)
    sub_date_time = db.Column(db.DateTime, nullable=True, default=None)
    data = db.Column(db.LargeBinary, nullable=True)
    filename = db.Column(db.String(255), nullable=True)
    is_genuine = db.Column(db.Boolean, nullable=True, default=False)


    def to_json(self):
        json_obj = Serializer.serialize(self)
        json_obj.pop("data", None)
        return json_obj