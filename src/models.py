import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    model = db.Column(db.String(255), nullable=False)
    dataset = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(512), nullable=False)
    parallel = db.Column(db.String(512), default=1)
    number = db.Column(db.String(512), default=10)
    max_tokens = db.Column(db.Integer, default=1024)
    status = db.Column(db.String(20), default='pending')
    output_path = db.Column(db.String(512), nullable=True)
    extra_args = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'dataset': self.dataset,
            'url': self.url,
            'parallel': self.parallel,
            'number': self.number,
            'max_tokens': self.max_tokens,
            'status': self.status,
            'output_path': self.output_path,
            'extra_args': self.extra_args,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            'completed_at': self.completed_at.strftime('%Y-%m-%d %H:%M:%S') if self.completed_at else None
        }


class Dataset(db.Model):
    __tablename__ = 'datasets'
    
    id = db.Column(db.String(64), primary_key=True)
    dataset_name = db.Column(db.String(255), nullable=False)
    dataset_desc = db.Column(db.Text, nullable=True)
    dataset_path = db.Column(db.String(512), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'dataset_name': self.dataset_name,
            'dataset_desc': self.dataset_desc,
            'dataset_path': self.dataset_path,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
