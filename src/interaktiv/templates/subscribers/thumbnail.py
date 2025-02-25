from typing import NoReturn, Optional

from zope.lifecycleevent import ObjectAddedEvent, ObjectModifiedEvent
from plone.dexterity.content import DexterityContent
from plone import api
from Acquisition import aq_base, aq_parent
from zope.annotation.interfaces import IAnnotations
from Products.CMFCore.utils import getToolByName


def thumbnail_created(obj: DexterityContent, event: ObjectAddedEvent) -> NoReturn:
    if not getattr(obj, "thumbnailUpload", False):
        return

    obj.is_template_thumbnail = True

    parent = _get_template_parent(obj)
    if not parent:
        return

    _unindex_other_thumbnails(parent, obj)

    parent.template_thumbnail = obj.absolute_url()
    parent.reindexObject(idxs=["template_thumbnail"])


def _get_template_parent(obj: DexterityContent) -> Optional[DexterityContent]:
    parent = aq_parent(obj)
    if parent and parent.portal_type == "Template":
        return parent
    return None


def _unindex_other_thumbnails(parent: DexterityContent, current_obj: DexterityContent) -> None:
    catalog = getToolByName(parent, 'portal_catalog')
    for child in parent.objectValues():
        if getattr(child, "is_template_thumbnail", False) and current_obj.UID() != child.UID():
            parent.manage_delObjects([child.id])
            catalog.unindexObject(child)
