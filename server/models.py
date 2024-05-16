from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Doctor(db.Model, SerializerMixin):
    
    __tablename__ = 'doctors_table'

    # define columns 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    specialty = db.Column(db.String)

    #define relationships

    appointments = db.relationship('Appointment', back_populates='doctor')

    #many to many relationship between doctors and patients
    # first go through appointments then get the patient linked to that appointment 
    # you always go through the join table to get to the other table so in this case appointments

    patients = association_proxy('appointments', 'patient')

    # converts the instance of a class to an object so its readable in json, this replaces to_dict(self)
    #firs thing to do is put it in the class() and then add SerializerMixin

    serialize_rules = ['-patients', '-appointments.doctor']



class Patient(db.Model, SerializerMixin):
    
    __tablename__ = 'patients_table'

    # define columns
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # define relationships

    appointments = db.relationship('Appointment', back_populates='patient')

    doctors = association_proxy('appointments', 'doctors')

    serialize_rules = ('-appointments.patient',  )
    
    




class Appointment(db.Model, SerializerMixin):
    
    __tablename__ = 'appointments_table'

    # define columns

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)

    # define relationships
    # join table between doctors and patients 
    # Foreign keys fist pointing to the other tables

    patient_id = db.Column(db.Integer, db.ForeignKey('patients_table.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors_table.id'))

    patient = db.relationship('Patient', back_populates='appointments')
    doctor = db.relationship('Doctor', back_populates='appointments')

    serialize_rules = ['-doctor.appointments', '-patient.appointments']
                    

