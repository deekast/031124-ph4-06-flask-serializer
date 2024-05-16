#!/usr/bin/env python3

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Doctor, Patient, Appointment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)

migrate = Migrate(app, db)

db.init_app(app)

@app.get('/')
def index():
    return "Hello world"



# DOCTOR ROUTES ################################

@app.get('/doctors')
def all_doctors():
    return [d.to_dict() for d in Doctor.query.all()], 200


@app.get('/doctors/<int:id>')
def doctor_by_id(id):
    doctor = Doctor.query.where(Doctor.id == id).first()
    if doctor:
        return doctor.to_dict(rules = ['-appointments', '-id', '-patients']), 200
    else:
        return {'error': 'Not found'}, 404
    

@app.post('/doctors')
def post_doctor():
    doctor = Doctor(
        name=request.json.get('name'),
        specialty=request.json.get('specialty')
    )
    db.session.add(doctor)
    db.session.commit()
    return doctor.to_dict(), 201


@app.patch('/doctors/<int:id>')
def patch_doctor_by_id(id):
    doctor = Doctor.query.where(Doctor.id == id).first()
    if doctor:
        for key in request.json.keys():
            setattr(doctor, key, request.json[key])
        db.session.add(doctor)
        db.session.commit()
        return doctor.to_dict(), 202
    else:
        return {'error': 'Not found'}, 404
    

@app.delete('/doctors/<int:id>')
def delete_doctor_by_id(id):
    doctor = Doctor.query.where(Doctor.id == id).first()
    if doctor:
        db.session.delete(doctor)
        db.session.commit()
        return {}, 204
    else:
        return {'error': 'Not found'}, 404



# PATIENT ROUTES ################################

@app.get('/patients')
def all_patients():
    return [p.to_dict() for p in Patient.query.all()], 200


@app.get('/patients/<int:id>')
def patient_by_id(id):
    patient = Patient.query.where(Patient.id == id).first()
    if patient:
        return patient.to_dict(), 200
    else:
        return {'error': 'Not found'}, 404
    

@app.post('/patients')
def post_patient():
    patient = Patient( name=request.json.get('name') )
    db.session.add(patient)
    db.session.commit()
    return patient.to_dict(), 201


@app.patch('/patients/<int:id>')
def patch_patient_by_id(id):
    patient = Patient.query.where(Patient.id == id).first()
    if patient:
        for key in request.json.keys():
            setattr(patient, key, request.json[key])
        db.session.add(patient)
        db.session.commit()
        return patient.to_dict(), 202
    else:
        return {'error': 'Not found'}, 404
    

@app.delete('/patients/<int:id>')
def delete_patient_by_id(id):
    patient = Patient.query.where(Patient.id == id).first()
    if patient:
        db.session.delete(patient)
        db.session.commit()
        return {}, 204
    else:
        return {'error': 'Not found'}, 404



# APPOINTMENT ROUTES ################################

@app.get('/appointments')
def all_appointments():
    return [a.to_dict() for a in Appointment.query.all()], 200


@app.get('/appointments/<int:id>')
def appointment_by_id(id):
    appointment = Appointment.query.where(Appointment.id == id).first()
    if appointment:
        return appointment.to_dict(), 200
    else:
        return {'error': 'Not found'}, 404
    

@app.post('/appointments')
def post_appointment():
    appointment = Appointment(
        date=request.json.get('date'),
        doctor_id=request.json.get('doctor_id'),
        patient_id=request.json.get('patient_id')
    )
    db.session.add(appointment)
    db.session.commit()
    return appointment.to_dict(), 201


@app.patch('/appointments/<int:id>')
def patch_appointment_by_id(id):
    appointment = Appointment.query.where(Appointment.id == id).first()
    if appointment:
        for key in request.json.keys():
            setattr(appointment, key, request.json[key])
        db.session.add(appointment)
        db.session.commit()
        return appointment.to_dict(), 202
    else:
        return {'error': 'Not found'}, 404
    

@app.delete('/appointments/<int:id>')
def delete_appointment_by_id(id):
    appointment = Appointment.query.where(Appointment.id == id).first()
    if appointment:
        db.session.delete(appointment)
        db.session.commit()
        return {}, 204
    else:
        return {'error': 'Not found'}, 404



if __name__ == '__main__':
    app.run(port=5555, debug=True)