from flask_restx import Namespace, Resource
import numpy as np

api = Namespace('dhmimages', description='DHM phase image GET endpoint')

# img = api.model('DHMImage', {
#     'id': fields.Integer(readonly=True, description='Image ID'),
#     'data': fields.String(required=True, description='Image data as String')
# })

img_data = np.load('./testimages.npz')
img_count = len(img_data)
images = {'{}'.format(i): img_data['img{}'.format(i)] for i in range(1, img_count + 1)}


@api.route('/<string:img_id>')
@api.response(404, 'Image not found')
@api.param('img_id', 'Numerical ID of the image from the set of DHM phase images for the experiment')
class DHMImage(Resource):
    def get(self, img_id):
        result = images.get(img_id, None)
        if result is not None:
            return np.ravel(result).tolist()

            #TODO
            # nz_size = np.transpose(np.nonzero(result)).shape[0]
            # return {
            #     tuple(np.transpose(np.nonzero(result))[nz_idx]):
            #       result[tuple(np.transpose(np.nonzero(result))[nz_idx])]
            #     for nz_idx in range(nz_size)
            # }
