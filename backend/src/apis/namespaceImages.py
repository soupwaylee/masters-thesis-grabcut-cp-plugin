from flask_restx import Namespace, Resource
from utils.dhm_phase_images import ImageHandler

api = Namespace('dhmimages', description='DHM phase image GET endpoint')


# img = api.model('DHMImage', {
#     'id': fields.Integer(readonly=True, description='Image ID'),
#     'data': fields.String(required=True, description='Image data as String')
# })


@api.route('/<string:img_id>')
@api.response(404, 'Image not found')
@api.param('img_id', 'Numerical ID of the image from the set of DHM phase images for the experiment')
class DHMImage(Resource):
    def get(self, img_id):
        ImageHandler.get_image_as_response(img_id)
