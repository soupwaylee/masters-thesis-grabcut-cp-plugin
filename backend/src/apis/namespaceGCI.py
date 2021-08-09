from flask_restx import Namespace, Resource, fields
from flask import abort, current_app, request
from models.grabcutinteraction import GrabCutInteractionModel
from db import db

api = Namespace('grabcutinteractions', description='GrabCutInteraction operations')

interaction_record_fields = api.model('GrabCutInteraction', {
    'id': fields.String(description='UUID for the GrabCut interaction record'),
    'sessionId': fields.String(required=True, description='ID for the labeling session'),
    'imageId': fields.Integer(required=True,
                              description='ID for the image that had been '
                                          'labelled for the current record'),
    'annotatedPixels': fields.Integer(description='number of pixels that had been annotated by the user'),
    'foregroundPixels': fields.Integer(description='number of foreground pixels that had been marked'),
    'backgroundPixels': fields.Integer(description='number of background pixels that had been marked'),
    'scribbles': fields.Integer(description='total number of scribbles created by the user'),
    'foregroundScribbles': fields.Integer(description=''),
    'backgroundScribbles': fields.Integer(description='total number of background scribbles created by the user'),
    'submissionIndex': fields.Integer(description='submission counter'),
    'submissionTime': fields.DateTime(description='GrabCut segmentation request timestamp',
                                      dt_format='rfc822'),
})

scribble_pixel_fields = api.model('ScribblePixel', {
    'x': fields.Integer(description='x-Coordinate for the pixel'),
    'y': fields.Integer(description='y-Coordinate for the pixel'),
    'type': fields.Integer(description='1 for foreground and 0 for background respectively',
                           min=0, max=1)
})

segmentation_fields = api.model('ScribblePixelsList', {
    'interactionRecord': fields.Nested(interaction_record_fields, skip_none=True),
    'scribblePixels': fields.List(fields.Nested(scribble_pixel_fields))
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
            api.abort(404, f'GrabCut Interaction record {id} does not exist')

    def create(self, data):
        interaction_record = data['interactionRecord']
        current_app.logger.info(f"Creating GrabCutInteraction record: {str(interaction_record)}")
        # TODO perform db connection & segmentation asynchronously?
        gci = GrabCutInteractionModel(
            session_id=data['sessionId'],
            image_id=data['imageId'],
            annotated_pixels=data['annotatedPixels'],
            foreground_pixels=data['foregroundPixels'],
            background_pixels=data['backgroundPixels'],
            scribbles=data['scribbles'],
            foreground_scribbles=data['foregroundPixels'],
            background_scribbles=data['backgroundScribbles'],
            submissions=data['submissions'],
            first_submission_time=data['firstSubmissionTime'],
            last_submission_time=data['lastSubmissionTime']
        )
        self.session.add(gci)
        self.session.commit()
        return gci

    def update(self, id, data):
        gci = self.session.query(GrabCutInteractionModel).get(id)
        gci.session_id =data['sessionId']
        gci.image_id = data['imageId']
        gci.annotated_pixels = data['annotatedPixels']
        gci.foreground_pixels = data['foregroundPixels']
        gci.background_pixels = data['backgroundPixels']
        gci.scribbles = data['scribbles']
        gci.foreground_scribbles = data['foregroundPixels']
        gci.background_scribbles = data['backgroundScribbles']
        gci.submissions = data['submissions']
        gci.first_submission_time = data['firstSubmissionTime']
        gci.last_submission_time = data['lastSubmissionTime']
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
    @api.marshal_list_with(interaction_record_fields)
    def get(self):
        '''List all interaction records'''
        return DAO.grabcutinteractions()

    @api.doc('Submit user interaction record and perform segmentation for given image and annotation pixels.')
    @api.expect(segmentation_fields)
    def post(self):
        '''Create a new GrabCut interaction record and perform segmentation'''
        data = request.json
        interaction_record = data['interactionRecord']
        scribble_pixels = data['scribblePixels']
        target_image_id = interaction_record['imageId']
        current_app.logger.info("Creating GrabCutInteraction record: {}".format(scribble_pixels[0]['y']))
        return {'test': 'y of first point: {}'.format(scribble_pixels[0]['y'])}, 201


@api.route('/<int:id>')
@api.response(404, 'Interaction record not found')
@api.param('id', 'The interaction record identifier')
class GrabCutInteraction(Resource):
    '''Show or delete a single GrabCut interaction record'''

    @api.doc('get_grabcutinteraction')
    @api.marshal_with(interaction_record_fields)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @api.doc('delete_grabcutinteraction')
    @api.response(204, 'GrabCut interaction record deleted')
    def delete(self, id):
        '''Delete a GrabCut interaction record given its identifier'''
        DAO.delete(id)
        return '', 204

    @api.expect(interaction_record_fields)
    @api.marshal_with(interaction_record_fields)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)
