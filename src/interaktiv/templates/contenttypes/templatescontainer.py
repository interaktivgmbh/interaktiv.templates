from plone.volto.content import FolderishDocument
from zope.interface import implementer
from zope.interface import Interface


class ITemplatesContainer(Interface):
    """Interface for TemplatesContainer"""


@implementer(ITemplatesContainer)
class TemplatesContainer(FolderishDocument):
    """TemplatesContainer Container"""
