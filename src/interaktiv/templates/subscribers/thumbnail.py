from typing import Optional, NoReturn

from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from plone.dexterity.content import DexterityContent
from zope.lifecycleevent import ObjectAddedEvent


def assign_template_thumbnail(obj: DexterityContent, event: ObjectAddedEvent) -> None:
    if not getattr(obj, 'thumbnailUpload', False):
        return

    obj.is_template_thumbnail = True

    template = _get_thumbnail_parent(obj)
    if not template:
        return

    _unindex_other_thumbnails(template, obj)

    template.template_thumbnail = obj.absolute_url()
    template.reindexObject(idxs=['template_thumbnail'])


def _get_thumbnail_parent(obj: DexterityContent) -> Optional[DexterityContent]:
    parent = aq_parent(obj)
    if parent and parent.portal_type == 'Template':
        return parent
    return None


def _unindex_other_thumbnails(parent: DexterityContent, obj: DexterityContent) -> NoReturn:
    catalog = getToolByName(parent, 'portal_catalog')
    for child in parent.objectValues():
        if getattr(child, 'is_template_thumbnail', False) and obj.UID() != child.UID():
            parent.manage_delObjects([child.id])
            catalog.unindexObject(child)
