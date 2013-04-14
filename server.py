#!/usr/bin/env python

from flask import Flask
import data

app = Flask(__name__)


@app.route('/patients')
def patients():
    return data.get_patients


@app.route('/patients/<int:patient_id>', methods=['GET', 'POST'])
def patient(patient_id):
    return data.get_patient(patient_id)


@app.route('/patients/<int:patient_id>/vitalinfo')
def vital_infos(patient_id):
    return data.get_vital_infos()


@app.route('/patients/<int:patient_id>/vitalinfo/<int:vitalinfo_id>', methods=['GET', 'POST'])
def vital_info(patient_id, vitalinfo_id):
    return data.get_vital_info(vitalinfo_id)


if __name__ == '__main__':
    app.run(debug=True)