from flask_restx import Api

from .demographics import api as demographics_api
from .grabcutinteractions import api as gci_api
from .dhmimages import api as dhmimg_api
from .annotatormasks import api as masks_api

api = Api(
    title='GrabCut interaction endpoints',
    description='The endpoints of the thesis user study.'
)

api.add_namespace(demographics_api, path='/demographics')
api.add_namespace(gci_api, path='/gcsegmentation')
api.add_namespace(dhmimg_api, path='/dhmimages')
api.add_namespace(masks_api, path='/masks')
