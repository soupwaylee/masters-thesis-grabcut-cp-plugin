from db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class GrabCutInteractionModel(db.Model):
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
    image_id = db.Column(db.Integer)
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
