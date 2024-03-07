from interaktiv.framework.test import TestLayer
from plone.app.testing import FunctionalTesting, IntegrationTesting
from plone.testing.zope import WSGI_SERVER_FIXTURE


class InteraktivTemplatesLayer(TestLayer):

    def __init__(self):
        super().__init__()
        self.products_to_import = ['interaktiv.templates']
        self.product_to_install = 'interaktiv.templates'


INTERAKTIV_TEMPLATES_FIXTURE = InteraktivTemplatesLayer()
INTERAKTIV_TEMPLATES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(INTERAKTIV_TEMPLATES_FIXTURE,),
    name='InteraktivTemplatesLayer:IntegrationTesting'
)
INTERAKTIV_TEMPLATES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(INTERAKTIV_TEMPLATES_FIXTURE, WSGI_SERVER_FIXTURE),
    name='InteraktivTemplatesLayer:FunctionalTesting'
)
