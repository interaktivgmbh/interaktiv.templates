import unittest
from unittest.mock import Mock
from urllib.parse import urlparse

from Products.ZCatalog.interfaces import ICatalogBrain
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.uuid.utils import uuidToCatalogBrain
from plone.dexterity.content import DexterityContent

from interaktiv.templates.services.templateContainer.get import InteraktivTemplatesTemplateContainerGet
from interaktiv.templates.testing import INTERAKTIV_TEMPLATES_FUNCTIONAL_TESTING


class TestTemplatesContainerGet(unittest.TestCase):
    layer = INTERAKTIV_TEMPLATES_FUNCTIONAL_TESTING

    def setUp(self):
        super().setUp()

        self.portal = self.layer['portal']
        self.request = self.layer['request']

        self.service = InteraktivTemplatesTemplateContainerGet()
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

    def test_template_container_get__no_content(self):
        # setup
        self.service.request.form = {'url': '/de/container/template'}

        # do it
        result = self.service.reply()

        # post condition
        self.assertIsNone(result)

    def test_template_container_get__find_container(self):
        # setup
        self.service.request.form = {'url': urlparse(self.template.absolute_url()).path}

        # do it
        result = self.service.reply()

        # post condition
        self.assertIsNotNone(result)

    def test_template_container_get__container_result(self):
        # setup
        self.service.request.form = {'url': urlparse(self.template.absolute_url()).path}

        # do it
        result = self.service.reply()

        # post condition
        self.assertEqual(len(result.get('containers')), 1)
        self.assertEqual(result.get('containers')[0].get('id'), self.template_container.getId())
        self.assertEqual(result.get('containers')[0].get('path'), '/plone/templates_container')
        self.assertEqual(result.get('nearest_container'), self.template_container.absolute_url())

    def test_get_nearest_template_container(self):
        pass

    def test_get_nearest_template_container__no_container(self):
        # setup
        template_containers = []

        # do it
        result = self.service._get_nearest_template_container(self.template, [])

        # post condition
        self.assertIsNone(result)

    def test_get_nearest_template_container__nearest_container_returned(self):
        # setup
        content = Mock(spec=DexterityContent)
        content.getPhysicalPath = Mock(return_value=('', 'site', 'path', 'content'))

        container1 = Mock(spec=ICatalogBrain)
        container1.getPhysicalPath = Mock(return_value=('', 'site', 'path', 'a'))
        container1.getObject = Mock(return_value=container1)

        container2 = Mock(spec=ICatalogBrain)
        container2.getPhysicalPath = Mock(return_value=('', 'site', 'path', 'content', 'b'))
        container2.getObject = Mock(return_value=container2)

        container3 = Mock(spec=ICatalogBrain)
        container3.getPhysicalPath = Mock(return_value=('', 'site', 'path', 'c'))
        container3.getObject = Mock(return_value=container3)

        template_containers = [container1, container2, container3]

        # do it
        result = self.service._get_nearest_template_container(content, template_containers)

        # postcondition
        self.assertEqual(result, container2)

    def test_serialize_container(self):
        # do it
        result = self.service._serialize(brain=uuidToCatalogBrain(self.template_container.UID()))

        # post condition
        self.assertEqual(result.get('title'), 'Templates Container')
        self.assertEqual(result.get('url'), self.template_container.absolute_url())
        self.assertEqual(result.get('path'), '/plone/templates_container')
        self.assertEqual(result.get('id'), self.template_container.getId())
