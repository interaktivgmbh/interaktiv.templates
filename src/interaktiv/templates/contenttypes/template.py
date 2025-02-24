from zope.interface import implementer, Interface
from zope import schema

from plone.volto.content import FolderishDocument
from plone.volto.interfaces import IFolderishDocument
from plone.app.contenttypes.interfaces import IDocument
from plone.autoform import directives

from interaktiv.templates import _


class ITemplate(IFolderishDocument):
    """ Interface for Template """

    template_description = schema.TextLine(
        title=_('Template description'),
        description=_('give a quick description for the template'),
        default='',
        required=False
    )

    template_thumbnail = schema.TextLine(
        title=_("Template Thumbnail"),
        description=_("URL to the template thumbnail"),
        required=False
    )


@implementer(ITemplate)
class Template(FolderishDocument):
    """ Template Container """
