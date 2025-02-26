import unittest
from interaktiv.templates.testing import INTERAKTIV_TEMPLATES_INTEGRATION_TESTING
from unittest.mock import patch, MagicMock

from interaktiv.templates.subscribers.thumbnail import _get_thumbnail_parent
from interaktiv.templates.subscribers.thumbnail import _unindex_other_thumbnails
from interaktiv.templates.subscribers import thumbnail
from plone.dexterity.content import DexterityContent
from zope.lifecycleevent import ObjectAddedEvent


class TestThumbnailSubscriber(unittest.TestCase):
    layer = INTERAKTIV_TEMPLATES_INTEGRATION_TESTING

    def setUp(self):
        super().setUp()

        self.obj = MagicMock()
        self.parent = MagicMock()

    @patch('interaktiv.templates.subscribers.thumbnail._get_thumbnail_parent')
    def test_assign_template_thumbnail__not_attr(self, mock_get_thumbnail_parent):
        # setup
        self.obj.thumbnailUpload = False

        # do it
        thumbnail.assign_template_thumbnail(self.obj, None)

        # post condition
        mock_get_thumbnail_parent.assert_not_called()

    @patch("interaktiv.templates.subscribers.thumbnail._get_thumbnail_parent", return_value=None)
    @patch("interaktiv.templates.subscribers.thumbnail._unindex_other_thumbnails")
    def test_get_thumbnail_parent__no_parent(self, mock_unindex_other_thumbnails, mock_get_thumbnail_parent):
        # setup
        self.obj.thumbnailUpload = True

        # do it
        thumbnail.assign_template_thumbnail(self.obj, None)

        # postcondition
        mock_get_thumbnail_parent.assert_called_once_with(self.obj)
        mock_unindex_other_thumbnails.assert_not_called()

    @patch("interaktiv.templates.subscribers.thumbnail._get_thumbnail_parent")
    @patch("interaktiv.templates.subscribers.thumbnail._unindex_other_thumbnails")
    def test_assign_template_thumbnail__sets_template_thumbnail(self, mock_unindex, mock_get_parent):
        # setup
        self.obj.thumbnailUpload = True
        mock_get_parent.return_value = self.parent

        # do it
        thumbnail.assign_template_thumbnail(self.obj, None)

        # postcondition
        self.assertTrue(self.obj.is_template_thumbnail)
        self.parent.reindexObject.assert_called_once_with(idxs=["template_thumbnail"])

    @patch("interaktiv.templates.subscribers.thumbnail._get_thumbnail_parent")
    @patch("interaktiv.templates.subscribers.thumbnail._unindex_other_thumbnails")
    def test_assign_template_thumbnail__calls_unindex_other_thumbnails(self, mock_unindex, mock_get_parent):
        # setup
        self.obj.thumbnailUpload = True
        mock_get_parent.return_value = self.parent

        # do it
        thumbnail.assign_template_thumbnail(self.obj, None)

        # postcondition
        mock_unindex.assert_called_once_with(self.parent, self.obj)

    @patch("interaktiv.templates.subscribers.thumbnail.getToolByName")
    def test_unindex_other_thumbnails__removes_others(self, mock_get_tool):
        # setup
        catalog = MagicMock()
        mock_get_tool.return_value = catalog

        other_thumbnail = MagicMock()
        other_thumbnail.is_template_thumbnail = True
        other_thumbnail.UID.return_value = "otherUID"
        other_thumbnail.id = "otherThumbnail"

        self.obj.UID.return_value = "currentUID"
        self.parent.objectValues.return_value = [self.obj, other_thumbnail]

        # do it
        thumbnail._unindex_other_thumbnails(self.parent, self.obj)

        # postcondition
        self.parent.manage_delObjects.assert_called_once_with(["otherThumbnail"])
        catalog.unindexObject.assert_called_once_with(other_thumbnail)


    def test_get_thumbnail_parent__returns_none_if_not_template(self):
        # setup
        self.parent.portal_type = "NotTemplate"
        self.obj.__parent__ = self.parent

        # do it
        parent = thumbnail._get_thumbnail_parent(self.obj)

        # postcondition
        self.assertIsNone(parent)


