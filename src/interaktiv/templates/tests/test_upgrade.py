from interaktiv.templates.testing import INTERAKTIV_TEMPLATES_INTEGRATION_TESTING
from interaktiv.templates.upgrades import v1_to_v1010
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import getUtility
import unittest

class TestUpgrades(unittest.TestCase):
    layer = INTERAKTIV_TEMPLATES_INTEGRATION_TESTING

    def test_upgrade_v1_to_v10010(self):
        # setup
        behavior = 'interaktiv.templates.behaviors.thumbnail.IThumbnailBehavior'

        # do it
        v1_to_v1010.upgrade(None)

        # postcondiition
        fti = getUtility(IDexterityFTI, name='Image')
        self.assertIn(behavior, fti.behaviors)
