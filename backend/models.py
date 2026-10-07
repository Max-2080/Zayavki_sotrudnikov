from database import db
from datetime import datetime

class Employee(db.Model):
    __tablename__ = 'employee'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), default='employee')
    
    # Связи с явным указанием foreign_keys
    requests = db.relationship('Request', 
                               backref='author', 
                               lazy=True,
                               foreign_keys='Request.author_id')
    
    assigned_requests = db.relationship('Request', 
                                        backref='executor', 
                                        lazy=True,
                                        foreign_keys='Request.executor_id')

class Category(db.Model):
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))
    
    requests = db.relationship('Request', backref='category', lazy=True)

class Request(db.Model):
    __tablename__ = 'request'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='new')
    priority = db.Column(db.String(20), default='medium')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    author_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    executor_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)