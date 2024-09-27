from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class NokiaUser(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    date_updated = db.Column(db.DateTime, default = datetime.utcnow)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date_updated': self.date_updated.isoformat(),
            'date_created': self.date_created.isoformat()
        }
