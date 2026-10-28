from interaktiv.templates.contenttypes.template import ITemplate
from interaktiv.templates.testing import INTEGRATION_TESTING
from interaktiv.templates.tests import TestCase
from plone import api
from plone.restapi.interfaces import IDeserializeFromJson
from zExceptions import BadRequest
from zope.component import getMultiAdapter
from zope.schema.interfaces import RequiredMissing
from zope.schema.interfaces import TooShort
from zope.schema.interfaces import WrongContainedType

import json


class TestTemplateTypesField(TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        super().setUp()
        self.templates_container = api.content.create(
            container=self.portal, type="TemplatesContainer", id="templates_container"
        )
        self.template = api.content.create(
            container=self.templates_container,
            type="Template",
            id="template",
            template_types=["Document", "Event"],
        )
        self.field = ITemplate["template_types"].bind(self.template)

    def test_template_types__stored_on_template(self):
        # postcondition
        self.assertListEqual(self.template.template_types, ["Document", "Event"])

    def test_template_types__accepts_types_with_blocks(self):
        # do it
        result = self.field.validate(["Document", "Event", "News Item"])

        # postcondition
        self.assertIsNone(result)

    def test_template_types__missing_value_is_rejected(self):
        # do it
        with self.assertRaises(RequiredMissing):
            self.field.validate(None)

    def test_template_types__empty_list_is_rejected(self):
        # do it
        with self.assertRaises(TooShort):
            self.field.validate([])

    def test_template_types__type_without_blocks_is_rejected(self):
        # do it
        with self.assertRaises(WrongContainedType):
            self.field.validate(["File"])

    def test_template_types__api_create_without_types_is_rejected(self):
        # setup
        template = api.content.create(
            container=self.templates_container, type="Template", id="template_b"
        )
        self.request["BODY"] = json.dumps({"title": "Title Value"})
        deserializer = getMultiAdapter((template, self.request), IDeserializeFromJson)

        # do it
        with self.assertRaises(BadRequest) as context:
            deserializer(validate_all=True, create=True)

        # postcondition
        self.assertIn("template_types", str(context.exception))
