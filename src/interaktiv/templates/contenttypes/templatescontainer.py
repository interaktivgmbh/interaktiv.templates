from plone.dexterity.content import Container
from zope.interface import Interface
from zope.interface import implementer
from plone.app.contenttypes.interfaces import IFolder
from plone.app.contenttypes.content import Folder
from plone.volto.content import FolderishDocument


class ITemplatesContainer(Interface):
    """ Interface for TemplatesContainer """


@implementer(ITemplatesContainer)
class TemplatesContainer(FolderishDocument):
    """ TemplatesContainer Container """
