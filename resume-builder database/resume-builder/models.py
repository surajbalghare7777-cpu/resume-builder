from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()


class Candidate(db.Model):
    __tablename__ = 'candidates'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(255), nullable=False, index=True)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    phone = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    linkedin = db.Column(db.String(500), nullable=True)
    summary = db.Column(db.Text, nullable=True)
    photo_filename = db.Column(db.String(255), nullable=True)
    template = db.Column(db.String(50), default='modern')
    
    education = db.Column(db.JSON, nullable=True)
    experience = db.Column(db.JSON, nullable=True)
    skills = db.Column(db.JSON, nullable=True)
    projects = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'linkedin': self.linkedin,
            'summary': self.summary,
            'photo_filename': self.photo_filename,
            'template': self.template,
            'education': self.education or [],
            'experience': self.experience or [],
            'skills': self.skills or [],
            'projects': self.projects or [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f'<Candidate {self.full_name} ({self.email})>'
