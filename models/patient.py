from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from models import Base, patient_department_table


class Patient(Base):
    """
    The Patient class is a database backed model representing a patient that has
    checked in to the hospital. A patient has a one-to-many relationship with
    vitalinfos, each vitalinfo representing a different and potentially
    unrelated check in.

    """

    __tablename__ = 'patient'
    nhi = Column(String(10), primary_key=True)
    latest_check_in = Column(DateTime)

    departments = relationship(
        "Department",
        secondary=patient_department_table,
        backref="patients"
    )

    vitalinfos = relationship(
        "VitalInfo",
        backref="patient",
        cascade="delete",
        order_by="desc(VitalInfo.check_in_time)"
    )

    def __init__(self, **kwargs):
        self.deserialize(kwargs)

    def serialize(self):
        return {
            "nhi": self.nhi,
            "departments": [d.serialize() for d in self.departments],
            "latest_check_in": self.latest_check_in.isoformat() if self.latest_check_in else None,
            "latest_vitalinfo": self.vitalinfos[0].serialize() if self.vitalinfos else None
        }

    def deserialize(self, data):
        """
        Populate a Patient object with data from a dictionary

        Arguments:
        data -- a dictionary containing data to put on the patient.

        """
        for key in data:
            if not hasattr(self, key):
                continue

            setattr(self, key, data[key])

    def __repr__(self):
        return '<Patient (nhi: {})>'.format(self.nhi)
