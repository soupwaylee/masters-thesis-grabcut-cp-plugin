from db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class GrabCutInteraction(db.Model):
    """
    A GrabCutInteraction defines a user interaction via the GrabCut tool
    to annotate a DHM phase image.

    Columns:
    ---
    id : UUID
        UUID for the GrabCut interaction record
    session_id : str
        ID for the labeling session
    image_id: int
        ID for the image that had been labelled for the current record
    annotated_pixels : int
        total number of pixels that had been annotated by the user
    foreground_pixels : int
        total number of foreground pixels that had been marked
    background_pixels : int
        total number of background pixels that had been marked
    scribbles : int
        total number of scribbles created by the user
    foreground_scribbles : int
        total number of foreground scribbles created by the user
    background_scribbles : int
        total number of background scribbles created by the user
    submissions : int
        number of times a GrabCut segmentation was requested
    first_submission_time : datetime
        Timestamp for the first GrabCut segmentation request
    last_submission_time : datetime
        Timestamp of the last GrabCut segmentation request (finishing timestamp)
    """
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = db.Column(db.String)
    image_id = db.Column(db.String)
    annotated_pixels = db.Column(db.Integer)
    foreground_pixels = db.Column(db.Integer)
    background_pixels = db.Column(db.Integer)
    scribbles = db.Column(db.Integer)
    foreground_scribbles = db.Column(db.Integer)
    background_scribbles = db.Column(db.Integer)
    submission_counter = db.Column(db.Integer)
    first_interaction_time = db.Column(db.DateTime)
    submission_time = db.Column(db.DateTime)

    def __repr__(self):
        return "<GrabCutInteraction session {} for image {}>".format(self.session_id, self.image_id)

    #TODO
    # @staticmethod
    # def from_dict(dictionary=dict()):


# TODO check this
class GrabCutInteractionDAO(object):
    def __init__(self, session):
        self.session = session

    def grabcutinteractions(self):
        return self.session.query(GrabCutInteraction).all()

    def get(self, id):
        if gci := self.session.query(GrabCutInteraction).get(id):
            return gci

    def create(self, data):
        # TODO perform db connection & segmentation asynchronously?
        gci = GrabCutInteraction(
            session_id=data['sessionId'],
            image_id=data['imageId'],
            annotated_pixels=data['annotatedPixels'],
            foreground_pixels=data['foregroundPixels'],
            background_pixels=data['backgroundPixels'],
            scribbles=data['scribbles'],
            foreground_scribbles=data['foregroundScribbles'],
            background_scribbles=data['backgroundScribbles'],
            submission_counter=data['submissionIndex'],
            first_interaction_time=data['firstInteractionTime'],
            submission_time=data['submissionTime']
        )
        self.session.add(gci)
        self.session.commit()
        return gci

    def update(self, id, data):
        gci = self.session.query(GrabCutInteraction).get(id)
        gci.session_id = data['sessionId']
        gci.image_id = data['imageId']
        gci.annotated_pixels = data['annotatedPixels']
        gci.foreground_pixels = data['foregroundPixels']
        gci.background_pixels = data['backgroundPixels']
        gci.scribbles = data['scribbles'],
        gci.foreground_scribbles = data['foregroundScribbles'],
        gci.background_scribbles = data['backgroundScribbles'],
        gci.submission_counter = data['submissionIndex'],
        gci.first_interaction_time = data['firstInteractionTime'],
        gci.submission_time = data['submissionTime']
        self.session.commit()
        return gci

    def delete(self, id):
        self.session.delete(GrabCutInteraction.query.get(id))
        self.session.commit()