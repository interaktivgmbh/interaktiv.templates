from typing import NoReturn

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

    parent = aq_parent(obj)
    if parent and parent.portal_type == "Template":
        catalog = getToolByName(parent, 'portal_catalog')
        for child in parent.objectValues():
            if child.is_template_thumbnail and obj.UID() != child.UID():
                catalog.unindexObject(child)

        parent.template_thumbnail = obj.absolute_url()
        parent.reindexObject(idxs=["template_thumbnail"])