from flask import request
from flask_restx import Namespace, Resource, fields, marshal
from sqlalchemy import exc

import app
from db import db
from models.grabcutinteraction import GrabCutInteractionDAO
from utils.dhm_phase_images import ImageHandler
from utils.grabcut_segmentation import GrabCutSegmenter

api = Namespace('grabcutinteractions', description='GrabCutInteraction operations')

interaction_record_fields = api.model('GrabCutInteraction', {
    'id': fields.String(description='UUID for the GrabCut interaction record', attribute='id'),
    'sessionId': fields.String(required=True, description='ID for the labeling session', attribute='session_id'),
    'imageId': fields.String(required=True,
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


DAO = GrabCutInteractionDAO(db.session)


@api.route('/')
class GrabCutInteractionList(Resource):
    """Shows a list of all GrabCut interaction records, and lets you POST to add a new interaction record"""

    @api.doc('list_gcinteractions')
    @api.marshal_list_with(interaction_record_fields)
    def get(self):
        """List all interaction records"""
        try:
            return DAO.grabcutinteractions()
        except RuntimeError as err:
            return f'RuntimeError: {err}', 404

    @api.doc('Submit user interaction record and perform segmentation for given image and annotation pixels.')
    @api.expect(segmentation_fields)
    def post(self):
        """Create a new GrabCut interaction record and perform segmentation"""
        data = request.json

        interaction_record = data['interactionRecord']
        annotated_pixel_indices = data['annotatedPixelIndices']
        annotated_pixel_types = data['annotatedPixelTypes']

        target_image_id = interaction_record['imageId']
        target_image = ImageHandler.get_image(target_image_id)

        try:
            gc_mask = GrabCutSegmenter.gc_segment(
                target_image,
                annotated_pixel_indices,
                annotated_pixel_types)
        except RuntimeError as err:
            app.logger.error(err)
            return f'RuntimeError: {err}', 500

        try:
            gci = DAO.create(interaction_record)
            app.logger.info(f"[*] Created InteractionRecord {interaction_record}")
        except exc.SQLAlchemyError as err:
            app.logger.error(err)
            return f'DB error: {err}', 500

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
        if result := DAO.get(id):
            return result, 200

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
