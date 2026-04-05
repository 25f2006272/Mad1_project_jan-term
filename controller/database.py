from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db=SQLAlchemy()

class admin(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(200),nullable=False)
    password=db.Column(db.String(200),nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

class roles(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    role=db.Column(db.String(10),nullable=False)


class students(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(200),nullable=False)
    password=db.Column(db.String(200),nullable=False)
    phone=db.Column(db.String(20),nullable=False)
    branch=db.Column(db.String(100))
    cgpa=db.Column(db.Float)
    graduation_year=db.Column(db.Integer)
    resume=db.Column(db.String(200))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)


class application(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    studennt_id=db.Column(db.Integer,db.ForeignKey('students.id'),nullable=False)
    drive_id=db.Column(db.Integer,db.ForeignKey('drive.id'),nullable=False)
    status=db.Column(db.String(20),default='Applied')




class company(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    company_name=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(200),nullable=False)
    password=db.Column(db.String(200),nullable=False)
    hr_contact=db.Column(db.String(100))
    website=db.Column(db.String(200))
    description=db.Column(db.Text)
    address=db.Column(db.Text)
    is_approved=db.Column(db.Boolean,default=False)
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'),nullable=False)



class drive(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    job_title=db.Column(db.String(50),nullable=False)
    job_description=db.Column(db.Text,nullable=False)
    criteria=db.Column(db.Text)
    salary_package=db.Column(db.String(100))
    application_deadline=db.Column(db.DateTime)
    status=db.Column(db.String(50),default='pending')
    company_id=db.Column(db.Integer,db.ForeignKey('company.id'),nullable=False)




