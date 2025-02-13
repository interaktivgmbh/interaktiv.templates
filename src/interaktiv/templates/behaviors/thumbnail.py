from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapts
from zope.interface import implementer, provider

from bsbw.contenttypes import _


@provider(IFormFieldProvider)
class IThumbnailBehavior(model.Schema):
   is_template_thumbnail = schema.Bool(
       title="Is Template Thumbnail?",
       description="Set this to true if it is a template thumbnail",
       default=False,
   )


@implementer(IThumbnailBehavior)
class ThumbnailBehavior(object):
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context