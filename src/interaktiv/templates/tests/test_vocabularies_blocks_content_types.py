from interaktiv.templates.testing import INTEGRATION_TESTING
from interaktiv.templates.tests import TestCase
from interaktiv.templates.vocabularies.blocks_content_types import blocks_content_types
from plone import api
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


class TestBlocksContentTypesVocabulary(TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        super().setUp()
        self.folder_fti = api.portal.get_tool("portal_types")["Folder"]
        self.folder_behaviors = self.folder_fti.behaviors

    def tearDown(self):
        self.folder_fti._updateProperty("behaviors", self.folder_behaviors)
        super().tearDown()

    def test_vocabulary__contains_types_with_blocks(self):
        # do it
        result = blocks_content_types(self.portal)

        # postcondition
        self.assertSetEqual(set(result.by_value), {"Document", "Event", "News Item"})

    def test_vocabulary__excludes_template_types_site_and_lrf(self):
        # precondition
        self.assertIn(
            "volto.blocks", api.portal.get_tool("portal_types")["Template"].behaviors
        )

        # do it
        result = blocks_content_types(self.portal)

        # postcondition
        for portal_type in ("Template", "TemplatesContainer", "Plone Site", "LRF"):
            self.assertNotIn(portal_type, result)

    def test_vocabulary__contains_type_after_blocks_behavior_added(self):
        # precondition
        self.assertNotIn("Folder", blocks_content_types(self.portal))

        # setup
        self.folder_fti._updateProperty(
            "behaviors", (*self.folder_behaviors, "volto.blocks")
        )

        # do it
        result = blocks_content_types(self.portal)

        # postcondition
        self.assertIn("Folder", result)

    def test_vocabulary__tokens_equal_values(self):
        # do it
        result = blocks_content_types(self.portal)

        # postcondition
        for term in result:
            self.assertEqual(term.token, term.value)

    def test_vocabulary__is_registered(self):
        # do it
        result = getUtility(
            IVocabularyFactory, name="interaktiv.templates.BlocksContentTypes"
        )(self.portal)

        # postcondition
        self.assertListEqual(
            [term.value for term in result],
            [term.value for term in blocks_content_types(self.portal)],
        )
