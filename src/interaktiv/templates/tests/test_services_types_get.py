from base64 import b64encode
from unittest.mock import patch

import interaktiv.framework as framework
from ZPublisher.pubevents import PubStart
from interaktiv.templates.services.types.get import InteraktivTemplatesTypesGet
from interaktiv.templates.testing import INTERAKTIV_TEMPLATES_FUNCTIONAL_TESTING
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.restapi.services.types.get import TypesGet
from plone.restapi.testing import RelativeSession
from zope.event import notify


class TestTemplatesTypesGet(framework.TestCase):
    layer = INTERAKTIV_TEMPLATES_FUNCTIONAL_TESTING
    service: InteraktivTemplatesTypesGet

    def setUp(self):
        super().setUp()

        self.service = self.traverse("/plone/@types/Document", method="GET")

        portal_url = self.portal.absolute_url()
        self.api_session = RelativeSession(portal_url, test=self)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

    # from plone.restapi tests
    def traverse(self, path="/plone", accept="application/json", method="GET"):
        request = self.layer["request"]
        request.environ["PATH_INFO"] = path
        request.environ["PATH_TRANSLATED"] = path
        request.environ["HTTP_ACCEPT"] = accept
        request.environ["REQUEST_METHOD"] = method
        auth = f"{SITE_OWNER_NAME}:{SITE_OWNER_PASSWORD}"
        request._auth = "Basic %s" % b64encode(auth.encode("utf8")).decode("utf8")
        notify(PubStart(request))
        return request.traverse(path)

    def test_services_types_get__processes_schema(self):
        # setup
        mock_schema = {"properties": {}}

        # do it
        with patch.object(TypesGet, 'reply_for_type', return_value=mock_schema) as mock_super_reply, \
                patch('interaktiv.templates.services.types.get.get_schema_from_template',
                      return_value=mock_schema) as mock_get_schema_from_template:
            result = self.service.reply_for_type()

        # post condition
        mock_super_reply.assert_called_once()
        mock_get_schema_from_template.assert_called_once_with(mock_schema)
        self.assertEqual(result, mock_schema)
