#!/usr/bin/env python

from random import choice, randrange, getrandbits, randint
from datetime import datetime, timedelta
import string

from models import db, Patient, VitalInfo, Department

with open('models/dictionary.txt') as f:
    words = [word.strip() for word in f.read().split('\n')]


def rand_date(from_days_ago=2000):
    return datetime.now() - timedelta(randint(0, from_days_ago))


def rand_word():
    return choice(words).lower()


def rand_sentence(length):
    return ' '.join([choice(words) for x in xrange(length)]).capitalize()


def rand_name():
    return rand_word().capitalize()


def rand_digit_str(length):
    return ''.join(choice(string.digits) for i in range(length))


def rand_nhi():
    letters = ''.join(choice(string.uppercase) for i in range(3))
    digits = ''.join(choice(string.digits) for i in range(3))
    return letters + digits


def rand_bool():
    return bool(getrandbits(1))


def list_of_rand_sentences(list_length, sentence_length):
    return ';'.join([rand_sentence(sentence_length) for x in xrange(list_length)])


def generate_patient():
    nhi = rand_nhi()

    return {
        'nhi': nhi,
    }


def generate_vital_info():
    check_in_time = rand_date()
    firstname = rand_name()
    lastname = rand_name()
    occupation = rand_name()
    citizen_resident = rand_bool()
    contact_num = rand_digit_str(10)
    gender = choice(['Male', 'Female'])
    dob = rand_date(30000)
    weight_value = randrange(0, 200)
    weight_unit = choice(['kg', 'lb'])
    height_value = randrange(0, 200)
    height_unit = choice(['cm'])
    blood_type = choice(['A', 'B', 'AB', 'O'])
    smoker = rand_bool()
    drinker = rand_bool()
    family_hist = list_of_rand_sentences(4, 10)
    overseas_recently = rand_bool()
    overseas_dests = list_of_rand_sentences(3, 2)
    medical_conditions = list_of_rand_sentences(2, 8)
    allergies = list_of_rand_sentences(4, 2)
    location = rand_name()

    return {
        'check_in_time': check_in_time,
        'firstname': firstname,
        'lastname': lastname,
        'occupation': occupation,
        'citizen_resident': citizen_resident,
        'contact_num': contact_num,
        'gender': gender,
        'dob': dob,
        'weight_value': weight_value,
        'weight_unit': weight_unit,
        'height_value': height_value,
        'height_unit': height_unit,
        'blood_type': blood_type,
        'smoker': smoker,
        'drinker': drinker,
        'family_hist': family_hist,
        'overseas_recently': overseas_recently,
        'overseas_dests': overseas_dests,
        'medical_conditions': medical_conditions,
        'allergies': allergies,
        'location': location
    }


def populate_database(num_patients, min_vital_infos, max_vital_infos):
    """
    Generates a number of Patients and a number of VitalInfos per patient and
    stores them in the database.

    Arguments
    num_patients    -- the number of patients to generate
    min_vital_infos -- the minimum number of VitalInfos to generate per Patient
    max_vital_infos -- the maximum number of VitalInfos to generate per Patient

    """
    departments = [
        Department(department_name="Cardiology"),
        Department(department_name="Emergency"),
        Department(department_name="Gynecology"),
        Department(department_name="Pediatrics"),
        Department(department_name="Obstetrics"),
        Department(department_name="Oncology"),
        Department(department_name="Orthopedics"),
        Department(department_name="Neurology")
    ]

    for i in xrange(num_patients):
        patient = Patient(**generate_patient())
        patient.departments.append(choice(departments))
        db.add(patient)
        db.commit()

        for j in xrange(randrange(min_vital_infos, max_vital_infos)):
            vitalinfo = VitalInfo(**generate_vital_info())
            vitalinfo.patient_nhi = patient.nhi

            lci = patient.latest_check_in
            vid = vitalinfo.check_in_time

            lci = vid if lci is None or vid > lci else lci
            patient.latest_check_in = lci

            db.add(vitalinfo)
            db.commit()
