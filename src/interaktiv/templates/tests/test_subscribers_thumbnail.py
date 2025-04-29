from unittest.mock import patch, MagicMock

from interaktiv.templates.subscribers import thumbnail
from interaktiv.templates.testing import INTERAKTIV_TEMPLATES_FUNCTIONAL_TESTING
from interaktiv.framework import TestCase


class TestThumbnailSubscriber(TestCase):
    layer = INTERAKTIV_TEMPLATES_FUNCTIONAL_TESTING

    def setUp(self):
        super().setUp()

        self.content = MagicMock()
        self.catalog = MagicMock()
        self.parent = MagicMock()

    @patch('interaktiv.templates.subscribers.thumbnail._get_thumbnail_parent')
    @patch('interaktiv.templates.subscribers.thumbnail._unindex_other_thumbnails')
    def test_thumbnail__thumbnail_upload__no_attr(self, mock_parent, mock_unindex):
        # setup
        self.content.thumbnailUpload = False
        self.content.is_template_thumbnail = False

        # do it
        thumbnail.assign_template_thumbnail(self.content, None)

        # post condition
        self.assertFalse(self.content.is_template_thumbnail)
        mock_parent.assert_not_called()
        mock_unindex.assert_not_called()

    @patch('interaktiv.templates.subscribers.thumbnail._get_thumbnail_parent')
    def test_thumbnail__is_template_thumbnail(self, mock_parent):
        # setup
        self.content.thumbnailUpload = True
        self.content.is_template_thumbnail = False

        # do it
        thumbnail.assign_template_thumbnail(self.content, None)

        # post condition
        self.assertTrue(self.content.is_template_thumbnail)
        mock_parent.called_once()

    @patch('interaktiv.templates.subscribers.thumbnail._unindex_other_thumbnails')
    @patch('interaktiv.templates.subscribers.thumbnail._get_thumbnail_parent')
    def test_thumbnail__no_parent(self, mock_get_thumbnail_parent, mock_unindex):
        # setup
        self.content.thumbnailUpload = True
        mock_get_thumbnail_parent.return_value = None

        # do it
        thumbnail.assign_template_thumbnail(self.content, None)

        # post condition
        mock_get_thumbnail_parent.assert_called_once_with(self.content)
        mock_unindex.assert_not_called()

    @patch("interaktiv.templates.subscribers.thumbnail.aq_parent")
    def test_get_thumbnail_parent(self, mock_aq_parent):
        # setup
        mock_aq_parent.return_value = self.parent
        self.parent.portal_type = "Template"

        # do it
        result = thumbnail._get_thumbnail_parent(self.content)

        # post condition
        self.assertEqual(result, self.parent)
        mock_aq_parent.assert_called_once_with(self.content)

    @patch("interaktiv.templates.subscribers.thumbnail.aq_parent")
    def test_get_thumbnail_parent_no_template(self, mock_aq_parent):
        # setup
        mock_aq_parent.return_value = self.parent
        self.parent.portal_type = "Document"

        # do it
        result = thumbnail._get_thumbnail_parent(self.content)

        # post condition
        self.assertIsNone(result)
        mock_aq_parent.assert_called_once_with(self.content)

    @patch("interaktiv.templates.subscribers.thumbnail.getToolByName")
    def test_unindex_other_thumbnails(self, mock_get_tool):
        # setup
        mock_get_tool.return_value = self.catalog
        child1 = MagicMock()
        child2 = MagicMock()

        child1.is_template_thumbnail = True
        child1.UID.return_value = "uid1"
        child1.id = "id1"
        child2.is_template_thumbnail = False
        child2.UID.return_value = self.content.UID.return_value

        self.parent.objectValues.return_value = [child1, child2]

        # do it
        thumbnail._unindex_other_thumbnails(self.parent, self.content)

        # post condition
        self.parent.manage_delObjects.assert_called_once_with(["id1"])
        mock_get_tool.assert_called_once_with(self.parent, "portal_catalog")
        self.catalog.unindexObject.assert_called_once_with(child1)

    @patch("interaktiv.templates.subscribers.thumbnail.getToolByName")
    def test_unindex_other_thumbnails_no_thumbnails(self, mock_get_tool):
        # setup
        mock_get_tool.return_value = self.catalog
        child1 = MagicMock()
        child2 = MagicMock()

        child1.is_template_thumbnail = False
        child2.is_template_thumbnail = False

        self.parent.objectValues.return_value = [child1, child2]

        # do it
        thumbnail._unindex_other_thumbnails(self.parent, self.content)

        # post condition
        self.parent.manage_delObjects.assert_not_called()
        self.catalog.unindexObject.assert_not_called()
