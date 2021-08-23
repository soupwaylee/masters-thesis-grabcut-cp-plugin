from flask_restx import Namespace, Resource, fields, marshal
from flask import abort, current_app, request
from models.grabcutinteraction import GrabCutInteractionModel
from db import db
from sqlalchemy import exc
from utils.grabcut_segmentation import GrabCutSegmenter
from utils.dhm_phase_images import ImageHandler


api = Namespace('grabcutinteractions', description='GrabCutInteraction operations')

interaction_record_fields = api.model('GrabCutInteraction', {
    'id': fields.String(description='UUID for the GrabCut interaction record', attribute=''),
    'sessionId': fields.String(required=True, description='ID for the labeling session', attribute='session_id'),
    'imageId': fields.Integer(required=True,
                              description='ID for the image that had been labelled for the current record',
                              attribute='image_id'),
    'annotatedPixels': fields.Integer(description='number of pixels that had been annotated by the user',
                                      attribute='annotated_pixels'),
    'foregroundPixels': fields.Integer(description='number of foreground pixels that had been marked',
                                       attribute='foreground_pixels'),
    'backgroundPixels': fields.Integer(description='number of background pixels that had been marked',
                                       attribute='background_pixels'),
    'scribbles': fields.Integer(description='total number of scribbles created by the user',
                                attribute='scribbles'),
    'foregroundScribbles': fields.Integer(description='total number of foreground scribbles created by the user',
                                          attribute='foreground_scribbles'),
    'backgroundScribbles': fields.Integer(description='total number of background scribbles created by the user',
                                          attribute='background_scribbles'),
    'submissionIndex': fields.Integer(description='submission counter',
                                      attribute='submission_counter'),
    'firstInteractionTime': fields.DateTime(description='timestamp for first ever mousedown event on current image',
                                            dt_format='rfc822',
                                            attribute='first_interaction_time'),
    'submissionTime': fields.DateTime(description='GrabCut segmentation request timestamp',
                                      dt_format='rfc822',
                                      attribute='submission_time'),
})

segmentation_fields = api.model('Segmentation', {
    'interactionRecord': fields.Nested(interaction_record_fields, skip_none=True),
    'annotatedPixelIndices': fields.List(fields.Integer),  # (description='Index of flattened mask')
    'annotatedPixelTypes': fields.List(fields.Boolean)  # (description='True if foreground else background')
})

segmentation_post_response_fields = api.model('SegmentationResponse', {
    'interactionRecord': fields.Nested(interaction_record_fields, skip_none=True),
    'maskDataArray': fields.List(fields.Boolean)
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
        current_app.logger.info(f"Creating GrabCutInteraction record: {str(data)}")
        # TODO perform db connection & segmentation asynchronously?
        gci = GrabCutInteractionModel(
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
        gci = self.session.query(GrabCutInteractionModel).get(id)
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
        self.session.delete(GrabCutInteractionModel.query.get(id))
        self.session.commit()


DAO = GrabCutInteractionDAO(db.session)


@api.route('/')
class GrabCutInteractionList(Resource):
    """Shows a list of all GrabCut interaction records, and lets you POST to add a new interaction record"""

    @api.doc('list_gcinteractions')
    @api.marshal_list_with(interaction_record_fields)
    def get(self):
        """List all interaction records"""
        return DAO.grabcutinteractions()

    @api.doc('Submit user interaction record and perform segmentation for given image and annotation pixels.')
    @api.expect(segmentation_fields)
    def post(self):
        """Create a new GrabCut interaction record and perform segmentation"""
        data = request.json

        interaction_record = data['interactionRecord']
        annotated_pixel_indices = data['annotatedPixelIndices']
        annotated_pixel_types = data['annotatedPixelTypes']

        target_image_index = interaction_record['imageId']
        target_image = ImageHandler.get_image(target_image_index)

        try:
            gc_mask = GrabCutSegmenter.gc_segment(
                target_image,
                annotated_pixel_indices,
                annotated_pixel_types)
        except RuntimeError as err:
            return f'RuntimeError: {err}', 404

        try:
            gci = DAO.create(interaction_record)
        except exc.SQLAlchemyError as err:
            return f'DB error: {err}', 404

        return marshal(
            {
                'interactionRecord': gci,
                'maskDataArray': gc_mask
            },
            segmentation_post_response_fields,
        ), 201


@api.route('/<int:id>')
@api.response(404, 'Interaction record not found')
@api.param('id', 'The interaction record identifier')
class GrabCutInteraction(Resource):
    """Show or delete a single GrabCut interaction record"""

    @api.doc('get_grabcutinteraction')
    @api.marshal_with(interaction_record_fields)
    def get(self, id):
        """Fetch a given resource"""
        return DAO.get(id)

    @api.doc('delete_grabcutinteraction')
    @api.response(204, 'GrabCut interaction record deleted')
    def delete(self, id):
        """Delete a GrabCut interaction record given its identifier"""
        DAO.delete(id)
        return '', 204

    @api.expect(interaction_record_fields)
    @api.marshal_with(interaction_record_fields)
    def put(self, id):
        """Update a task given its identifier"""
        return DAO.update(id, api.payload)
