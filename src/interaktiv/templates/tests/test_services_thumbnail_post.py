import json
import unittest
from unittest.mock import patch, MagicMock
from urllib.parse import urlparse

from interaktiv.templates.services.templatethumbnail.post import InteraktivTemplateThumbnailPost
from interaktiv.templates.testing import INTERAKTIV_TEMPLATES_FUNCTIONAL_TESTING
from plone import api
from plone.api.exc import MissingParameterError
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles


class TestThumbnailServicePost(unittest.TestCase):
    layer = INTERAKTIV_TEMPLATES_FUNCTIONAL_TESTING

    def setUp(self):
        super().setUp()

        self.portal = self.layer['portal']
        self.request = self.layer['request']

        self.service = InteraktivTemplateThumbnailPost()
        self.service.context = self.portal
        self.service.request = self.request

        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Site Administrator'])

        self.template_container = api.content.create(
            container=self.portal,
            type='TemplatesContainer',
            id='templates_container',
            title='Templates Container'
        )

        self.template = api.content.create(
            container=self.template_container,
            type='Template',
            id='template',
            title='Template'
        )

    def test_thumbnail_post__no_parameter(self):
        # do it / post condition
        with self.assertRaises(MissingParameterError):
            self.service.reply()

    def test_thumbnail_post__template_not_found(self):
        # setup
        self.request['BODY'] = json.dumps({'url': '/de/container/template'})

        # do it
        result = self.service.reply()

        # post condition
        self.assertEqual(self.request.response.getStatus(), 404)
        self.assertEqual(result['message'], 'Template not found')

    def test_thumbnail_post__template_found(self):
        # setup
        self.request['BODY'] = json.dumps({'url': urlparse(self.template.absolute_url()).path})

        # do it
        result = self.service.reply()

        # post condition
        self.assertNotEqual(self.request.response.getStatus(), 404)
        self.assertNotEqual(result['message'], 'Template not found')

    @patch('interaktiv.templates.services.templatethumbnail.post.InteraktivTemplateThumbnailPost._replace_thumbnail')
    def test_thumbnail_post__with_modified_key_true(self, mock_replace_thumbnail):
        # setup
        self.request['BODY'] = json.dumps({'url': urlparse(self.template.absolute_url()).path, 'modified': True})

        # do it
        self.service.reply()

        # post condition
        mock_replace_thumbnail.assert_called_once()

    @patch(
        'interaktiv.templates.services.templatethumbnail.post.InteraktivTemplateThumbnailPost._create_and_assign_template_thumbnail')
    def test_thumbnail_post__with_modified_key_false(self, mock_create_and_assign_template_thumbnail):
        # setup
        self.request['BODY'] = json.dumps({'url': urlparse(self.template.absolute_url()).path, 'modified': False})

        # do it
        self.service.reply()

        # post condition
        mock_create_and_assign_template_thumbnail.assert_called_once()

    @patch('interaktiv.templates.services.templatethumbnail.post.NamedBlobImage')
    @patch('interaktiv.templates.utilities.helper.get_thumbnail')
    def test_thumbnail_post__replace_thumbnail(self, mock_get_thumbnail, mock_namedblobimage):
        # setup
        mock_get_thumbnail.return_value = b"fake-thumbnail-data"
        mock_namedblobimage.return_value = MagicMock()

        thumbnail = api.content.create(
            container=self.template,
            type='Image',
            id="template-thumbnail",
            title="Template Thumbnail",
            image=b"old-image-data"
        )

        self.template.template_thumbnail = thumbnail.absolute_url()
        self.template.reindexObject(idxs=["template_thumbnail"])

        # do it
        self.service._replace_thumbnail(self.template)

        # post condition
        self.assertIsNotNone(self.template.template_thumbnail)
        self.assertEqual(self.template.template_thumbnail, thumbnail.absolute_url())

    @patch('interaktiv.templates.services.templatethumbnail.post.logger.exception')
    @patch('plone.api.content.get', side_effect=Exception("Mocked exception"))
    def test_thumbnail_post__replace_thumbnail_logs_error(self, mock_content_get, mock_logger):
        # setup:
        self.template.template_thumbnail = "http://example.com/fake-thumbnail"
        self.template.reindexObject(idxs=["template_thumbnail"])

        # do it & assert exception
        with self.assertRaises(Exception) as context:
            self.service._replace_thumbnail(self.template)

        # post condition
        mock_logger.assert_called_once_with("Error replacing template thumbnail: %s", "Mocked exception")
        self.assertEqual(str(context.exception), "Mocked exception")
