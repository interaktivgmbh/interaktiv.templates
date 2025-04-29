import interaktiv.framework as framework
from interaktiv.templates.testing import INTERAKTIV_TEMPLATES_FUNCTIONAL_TESTING
from interaktiv.templates.upgrades import (
    v1_to_v1010
)
from plone.dexterity.interfaces import IDexterityFTI
from plone.namedfile import NamedBlobFile
from zope.component import getUtility, queryUtility


class TestUpgrades(framework.TestCase):
    layer = INTERAKTIV_TEMPLATES_FUNCTIONAL_TESTING

    def test_upgrade_v1_to_v1010__add_template_thumbnail_behaviour(self):
        # setup
        template_thumbnail_behavior = 'interaktiv.templates.behaviors.template_thumbnail.ITemplateThumbnailBehavior'
        fti = queryUtility(IDexterityFTI, name="Image")

        behaviors = list(fti.behaviors)
        behaviors.remove(template_thumbnail_behavior)

        # noinspection PyProtectedMember
        fti._updateProperty('behaviors', tuple(behaviors))

        # do it
        v1_to_v1010.upgrade(None)

        # postcondition
        fti = getUtility(IDexterityFTI, name='Image')
        self.assertIn(template_thumbnail_behavior, fti.behaviors)
