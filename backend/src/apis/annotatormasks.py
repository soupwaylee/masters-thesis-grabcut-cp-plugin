from flask_restx import Namespace, Resource, fields
from flask import request

import app
from models.grabcutmask import GrabCutMaskDAO
from db import db
from sqlalchemy import exc


api = Namespace('annotatormasks', description='Masks generated by the GrabCut algorithm from user annotations.')

grabcutmask_fields = api.model('GrabCutMask', {
    'id': fields.String(description='UUID for the GrabCut mask', attribute='id'),
    'sessionId': fields.String(required=True, description='ID for the labeling session', attribute='session_id'),
    'interactionRecordId': fields.String(required=True,
                                         description='UUID of the interaction record',
                                         attribute='interactionrecord_id'),
    'imageId': fields.Integer(required=True,
                              description='ID for the image that had been labelled for the current record',
                              attribute='image_id'),
    'mask': fields.String(description='Comma separated foreground indices.')
})


DAO = GrabCutMaskDAO(db.session)


@api.route('/')
class GrabCutMaskList(Resource):
    @api.doc('list_gcmasks')
    @api.marshal_list_with(grabcutmask_fields)
    def get(self):
        return DAO.grabcutmasks()

    @api.doc('Create a new entry for the submitted mask.')
    @api.expect(grabcutmask_fields)
    @api.marshal_with(grabcutmask_fields)
    def post(self):
        data = request.json

        mask_record = {
            'sessionId': data['sessionId'],
            'interactionRecordId': data['interactionRecordId'],
            'imageId': data['imageId'],
            'mask': data['mask']
        }

        try:
            mask = DAO.create(mask_record)
            app.logger.info("[*] Created a mask.")
            #TODO why does this expression throw an error
            # "sqlalchemy model is not json serializable"

            # app.logger.info(
            #     "Created a mask for session {} and image {}".format(
            #         mask.session_id, mask.image_id
            #     )
            # )
            return mask
        except exc.SQLAlchemyError as err:
            return f'DB error: {err}', 500