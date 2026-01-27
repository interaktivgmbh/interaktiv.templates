from interaktiv.templates.interfaces import IInteraktivTemplatesLayer
from interaktiv.templates.testing import INTEGRATION_TESTING
from plone.browserlayer import utils

# noinspection PyUnresolvedReferences
from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    layer = INTEGRATION_TESTING
    product_name = "interaktiv.templates"

    def test_product_installed(self):
        # setup
        installer = get_installer(self.layer["portal"], self.layer["request"])

        # do it
        result = installer.is_product_installed(self.product_name)

        # postcondition
        self.assertTrue(result)

    def test_browserlayer_installed(self):
        # postcondition
        self.assertIn(IInteraktivTemplatesLayer, utils.registered_layers())
