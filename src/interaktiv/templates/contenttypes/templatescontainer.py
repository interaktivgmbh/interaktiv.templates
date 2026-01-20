from plone.volto.content import FolderishDocument
from zope.interface import Interface
from zope.interface import implementer


class ITemplatesContainer(Interface):
    """ Interface for TemplatesContainer """


@implementer(ITemplatesContainer)
class TemplatesContainer(FolderishDocument):
    """ TemplatesContainer Container """
