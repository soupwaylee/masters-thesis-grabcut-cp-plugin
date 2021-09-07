from flask_restx import Namespace, Resource, fields
from flask import request

import app
from models.participantdata import ParticipationDataDAO
from db import db
from sqlalchemy import exc


api = Namespace('demographics', description='User demographics')

participant_data_fields = api.model('ParticipantData', {
    'id': fields.String(description='UUID for the participant record', attribute='id'),
    'sessionId': fields.String(required=True, description='ID of the labeling session', attribute='session_id'),
    'ageGroup': fields.String(required=True, description='Age group of the participant', attribute='age_group'),
    'academicField': fields.String(required=True,
                                   description='Academic field of the participant', attribute='academic_field'),
})


DAO = ParticipationDataDAO(db.session)


@api.route('/')
class GrabCutMaskList(Resource):
    @api.doc('List all entries of study participants.')
    @api.marshal_list_with(participant_data_fields)
    def get(self):
        return DAO.participantdatapoints()

    @api.doc('Create a new entry for the study participant.')
    @api.expect(participant_data_fields)
    @api.marshal_with(participant_data_fields)
    def post(self):
        data = request.json

        participant_data = {
            'sessionId': data['sessionId'],
            'ageGroup': data['ageGroup'],
            'academicField': data['academicField']
        }

        try:
            new_data = DAO.create(participant_data)
            app.logger.info(f"[*] Created participant data record {participant_data}")
            return new_data
        except exc.SQLAlchemyError as err:
            return f'DB error: {err}', 500
