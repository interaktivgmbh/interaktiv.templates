import zope.schema as schema
from interaktiv.templates import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope.component import adapts
from zope.interface import provider, implementer


@provider(IFormFieldProvider)
class ITemplateThumbnailBehavior(model.Schema):
    is_template_thumbnail = schema.Bool(
        title=_("Is template thumbnail?"),
        description=_("Marks image as a template thumbnail"),
        default=False,
        required=False
    )


@implementer(ITemplateThumbnailBehavior)
class TemplateThumbnailBehavior(object):
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context
