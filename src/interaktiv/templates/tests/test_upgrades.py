from Products.CMFCore.CatalogTool import CatalogTool
from plone import api

from interaktiv.templates.testing import INTEGRATION_TESTING
from interaktiv.templates.tests import TestCase
from interaktiv.templates.upgrades import v1000_to_v1001


class TestUpgrades(TestCase):
    layer = INTEGRATION_TESTING

    def test_upgrade_v1020_to_v1030__changes_index_meta_type(self):
        catalog: CatalogTool = api.portal.get_tool('portal_catalog')
        catalog.delIndex('template_thumbnail')
        catalog.addIndex('template_thumbnail', 'BooleanIndex')

        # precondition
        index_obj = catalog._catalog.getIndex('template_thumbnail')
        self.assertEqual(index_obj.meta_type, 'BooleanIndex')

        # do it
        v1000_to_v1001.upgrade(None)

        # postcondition
        index_obj = catalog._catalog.getIndex('template_thumbnail')
        self.assertEqual(index_obj.meta_type, 'FieldIndex')
