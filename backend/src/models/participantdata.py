from db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class ParticipantData(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = db.Column(db.String)
    age_group = db.Column(db.String)
    academic_field = db.Column(db.String)

    def __repr__(self):
        return "<For session {}: Participant in age group {} with {} background.>".format(
            self.session_id,
            self.age_group,
            self.academic_field
        )


class ParticipationDataDAO(object):
    def __init__(self, session):
        self.session = session

    def participantdatapoints(self):
        return self.session.query(ParticipantData).all()

    def get(self, id):
        if participant_data := self.session.query(ParticipantData).get(id):
            return participant_data

    def create(self, data):
        new_data = ParticipantData(
            session_id=data['sessionId'],
            age_group=data['ageGroup'],
            academic_field=data['academicField'],
        )
        self.session.add(new_data)
        self.session.commit()
        return new_data
