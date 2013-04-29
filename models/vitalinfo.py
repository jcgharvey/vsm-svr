from server import db


class VitalInfo(db.Model):
    vital_info_id = db.Column(db.Integer, primary_key=True)
    check_in_time = db.Column(db.DateTime, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.patient_id"), nullable=False)
    weight_value = db.Column(db.Float)
    weight_unit = db.Column(db.String(50))
    height_value = db.Column(db.Float)
    height_unit = db.Column(db.String(50))
    blood_type = db.Column(db.String(5))
    smoker = db.Column(db.Boolean)
    drinker = db.Column(db.Boolean)
    family_hist = db.Column(db.String(2500))
    overseas_recently = db.Column(db.Boolean)
    overseas_dests = db.Column(db.String(2500))
    medical_conditions = db.Column(db.String(2500))
    allergies = db.Column(db.String(2500))

    """docstring for VitalInfo"""
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def to_dict(self):
        temp = self.__dict__.copy()
        del temp['_sa_instance_state']
        temp['check_in_time'] = temp['check_in_time'].isoformat()
        return temp

    def __repr__(self):
        return '<VitalInfo (id: {}, patient: {})>'.format(self.vital_info_id, self.patient_id)