from db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class GrabCutMask(db.Model):
    # TODO Eventually remove redundant column information (interaction record UUID suffices)
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = db.Column(db.String)
    interactionrecord_id = db.Column(db.String)
    image_id = db.Column(db.String)
    mask = db.Column(db.Text)

    def __repr__(self):
        return "<The final mask of session {} for image {}>".format(self.session_id, self.image_id)


class GrabCutMaskDAO(object):
    def __init__(self, session):
        self.session = session

    def grabcutmasks(self):
        return self.session.query(GrabCutMask).all()

    def get(self, id):
        if mask_record := self.session.query(GrabCutMask).get(id):
            return mask_record

    def create(self, data):
        mask = GrabCutMask(
            session_id=data['sessionId'],
            interactionrecord_id=data['interactionRecordId'],
            image_id=data['imageId'],
            mask=data['mask']
        )
        self.session.add(mask)
        self.session.commit()
        return mask
