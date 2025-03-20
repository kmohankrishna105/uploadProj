from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class breachFile(db.Model):
    __tablename__ = "file"
    #__table_args__={"schema": __SCHEMA__}
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    fut_contract = db.Column(db.String(255))
    last_update_time = db.Column(db.DateTime)
    size = db.Column(db.Integer)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    filename = db.Column(db.String(255))
    data = db.Column(db.LargeBinary)
