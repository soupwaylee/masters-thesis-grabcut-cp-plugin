from flask_restx import Namespace, Resource, fields
from models.grabcutinteraction import GrabCutInteractionModel
from db import db

api = Namespace('grabcutinteractions', description='GrabCutInteraction operations')

gc = api.model('GrabCutInteraction', {
    'id':                       fields.String(readonly=True, description='UUID for the GrabCut interaction record'),
    'session_id':               fields.String(readonly=True, required=True, description='ID for the labeling session'),
    'image_id':                 fields.Integer(readonly=True, required=True,
                                               description='ID for the image that had been '
                                                           'labelled for the current record'),
    'annotated_pixels':         fields.Integer(description='number of pixels that had been annotated by the user'),
    'foreground_pixels':        fields.Integer(description='number of foreground pixels that had been marked'),
    'background_pixels':        fields.Integer(description='number of background pixels that had been marked'),
    'scribbles':                fields.Integer(description='total number of scribbles created by the user'),
    'foreground_scribbles':     fields.Integer(description=''),
    'background_scribbles':     fields.Integer(description='total number of background scribbles created by the user'),
    'submissions':              fields.Integer(description='number of times a GrabCut segmentation was requested'),
    'first_submission_time':    fields.DateTime(description='Timestamp for the first GrabCut segmentation request'),
    'last_submission_time':     fields.DateTime(description='Timestamp of the last GrabCut segmentation request')
})


# TODO check this
class GrabCutInteractionDAO(object):
    def __init__(self, session):
        self.session = session

    def grabcutinteractions(self):
        return self.session.query(GrabCutInteractionModel).all()

    def get(self, id):
        if gci := self.session.query(GrabCutInteractionModel).get(id):
            return gci
        else:
            api.abort(404, "GrabCut Interaction record {} doesn't exist".format(id))

    def create(self, data):
        # app.logger.debug(f"Creating GrabCutInteraction record: {str(data)}")
        gci = GrabCutInteractionModel(
            session_id=data["session_id"],
            image_id=data["image_id"],
            annotated_pixels=data["annotated_pixels"],
            foreground_pixels=data["foreground_pixels"],
            background_pixels=data["background_pixels"],
            scribbles=data["scribbles"],
            foreground_scribbles=data["foreground_pixels"],
            background_scribbles=data["background_scribbles"],
            submissions=data["submissions"],
            first_submission_time=data["first_submission_time"],
            last_submission_time=data["last_submission_time"]
        )
        self.session.add(gci)
        self.session.commit()
        return gci

    def update(self, id, data):
        gci = self.session.query(GrabCutInteractionModel).get(id)
        gci.session_id = data["session_id"]
        gci.image_id = data["image_id"]
        gci.annotated_pixels = data["annotated_pixels"]
        gci.foreground_pixels = data["foreground_pixels"]
        gci.background_pixels = data["background_pixels"]
        gci.scribbles = data["scribbles"]
        gci.foreground_scribbles = data["foreground_pixels"]
        gci.background_scribbles = data["background_scribbles"]
        gci.submissions = data["submissions"]
        gci.first_submission_time = data["first_submission_time"]
        gci.last_submission_time = data["last_submission_time"]
        self.session.commit()
        return gci

    def delete(self, id):
        self.session.delete(GrabCutInteractionModel.query.get(id))
        self.session.commit()


DAO = GrabCutInteractionDAO(db.session)


@api.route('/')
class GrabCutInteractionList(Resource):
    """Shows a list of all GrabCut interaction records, and lets you POST to add a new interaction record"""

    @api.doc('list_gcinteractions')
    @api.marshal_list_with(gc)
    def get(self):
        '''List all interaction records'''
        return DAO.grabcutinteractions()

    @api.doc('create_gcinteraction')
    @api.expect(gc)
    @api.marshal_with(gc, code=201)
    def post(self):
        '''Create a new GrabCut interaction record'''
        return DAO.create(api.payload), 201


@api.route('/<int:id>')
@api.response(404, 'Interaction record not found')
@api.param('id', 'The interaction record identifier')
class GrabCutInteraction(Resource):
    '''Show or delete a single GrabCut interaction record'''

    @api.doc('get_grabcutinteraction')
    @api.marshal_with(gc)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @api.doc('delete_grabcutinteraction')
    @api.response(204, 'GrabCut interaction record deleted')
    def delete(self, id):
        '''Delete a GrabCut interaction record given its identifier'''
        DAO.delete(id)
        return '', 204

    @api.expect(gc)
    @api.marshal_with(gc)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)
