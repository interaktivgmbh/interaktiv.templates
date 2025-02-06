from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import provider, implementer

from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope.component import adapts
import zope.schema as schema

from interaktiv.templates import _


@provider(IFormFieldProvider)
class ITemplateMetadataBehavior(model.Schema):
    contact_email = schema.TextLine(
        title=_('Template description'),
        description=_('give a quick description for the template'),
        default='',
        required=False
    )

@implementer(ITemplateMetadataBehavior)
class TemplateMetadataBehavior(object):
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context
