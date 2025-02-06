from zope.interface import implementer
from plone.app.contenttypes.interfaces import IDocument
from plone.app.contenttypes.content import Document
from zope import schema

from interaktiv.templates import _


class ITemplate(IDocument):
    """ Interface for Template """

    template_description = schema.TextLine(
        title=_('Template description'),
        description=_('give a quick description for the template'),
        default='',
        required=False
    )


@implementer(ITemplate)
class Template(Document):
    """ Template Container """
