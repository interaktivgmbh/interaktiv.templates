from typing import Optional

from Products.GenericSetup.tool import SetupTool
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility


# noinspection PyUnusedLocal
def upgrade(site_setup: Optional[SetupTool] = None) -> None:
    template_thumbnail = 'interaktiv.templates.behaviors.template_thumbnail.ITemplateThumbnailBehavior'

    fti = queryUtility(IDexterityFTI, name="Image")

    behaviors = list(fti.behaviors)
    behaviors.append(template_thumbnail)

    # noinspection PyProtectedMember
    fti._updateProperty('behaviors', tuple(behaviors))
