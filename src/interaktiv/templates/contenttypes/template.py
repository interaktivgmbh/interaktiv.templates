from zope.interface import implementer
from plone.app.contenttypes.interfaces import IDocument
from plone.app.contenttypes.content import Document


class ITemplate(IDocument):
    """ Interface for Template """


@implementer(ITemplate)
class Template(Document):
    """ Template Container """
