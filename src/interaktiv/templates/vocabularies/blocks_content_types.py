from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import iterSchemataForType
from plone.restapi.behaviors import IBlocks
from zope.globalrequest import getRequest
from zope.i18n import translate
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


EXCLUDED_TYPES = ("Template", "TemplatesContainer", "Plone Site", "LRF")


def has_blocks(portal_type: str) -> bool:
    return any(
        schema.isOrExtends(IBlocks) for schema in iterSchemataForType(portal_type)
    )


@provider(IVocabularyFactory)
def blocks_content_types(context=None) -> SimpleVocabulary:
    request = getRequest()
    portal_types = api.portal.get_tool("portal_types")

    terms = [
        SimpleTerm(
            value=fti.getId(),
            token=fti.getId(),
            title=translate(fti.Title(), context=request),
        )
        for fti in portal_types.listTypeInfo()
        if IDexterityFTI.providedBy(fti)
        and fti.getId() not in EXCLUDED_TYPES
        and has_blocks(fti.getId())
    ]
    return SimpleVocabulary(sorted(terms, key=lambda term: term.title.lower()))
