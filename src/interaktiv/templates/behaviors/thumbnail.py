from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapts
from zope.interface import implementer, provider

from interaktiv.templates import _


@provider(IFormFieldProvider)
class IThumbnailBehavior(model.Schema):
   is_template_thumbnail = schema.Bool(
       title=_("Is Template Thumbnail?"),
       description=_("Activate if this image is used as a thumbnail for a template"),
       default=False,
   )


@implementer(IThumbnailBehavior)
class ThumbnailBehavior(object):
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context