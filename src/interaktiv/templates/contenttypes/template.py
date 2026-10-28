from interaktiv.templates import _
from plone.namedfile.field import NamedBlobImage
from plone.volto.content import FolderishDocument
from plone.volto.interfaces import IFolderishDocument
from zope import schema
from zope.interface import implementer


class ITemplate(IFolderishDocument):
    template_description = schema.TextLine(
        title=_("Template description"),
        description=_("give a quick description for the template"),
        default="",
        required=False,
    )

    template_types = schema.List(
        title=_("label_template_types", default="Content types"),
        description=_(
            "help_template_types",
            default="The template is offered when adding content of these types.",
        ),
        value_type=schema.Choice(vocabulary="interaktiv.templates.BlocksContentTypes"),
        required=True,
        min_length=1,
    )

    template_thumbnail = NamedBlobImage(
        title=_("Template Thumbnail"),
        description=_("The template thumbnail image"),
        required=False,
    )


@implementer(ITemplate)
class Template(FolderishDocument):
    """Template Container"""
