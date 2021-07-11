from flask_restx import Api

from .namespaceGCI import api as gci_api

api = Api(
    title='GrabCut interaction endpoint',
    description='The endpoint of the GrabCut application for segmenting DHM phase images.'
)

api.add_namespace(gci_api, path='/grabcuts')
# api.add_namespace(namespaceGCI, path='/dhmimages')