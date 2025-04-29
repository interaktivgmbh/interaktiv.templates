import subprocess
import unittest
from unittest.mock import patch, MagicMock

from interaktiv.templates.testing import INTERAKTIV_TEMPLATES_INTEGRATION_TESTING
from interaktiv.templates.utilities.helper import get_schema_from_template, get_thumbnail


class TestHelper(unittest.TestCase):
    layer = INTERAKTIV_TEMPLATES_INTEGRATION_TESTING

    def test_no_request_returns_same_schema(self):
        # setup
        schema = {"properties": {}}

        # do it
        with patch("interaktiv.templates.utilities.helper.getRequest", return_value=None):
            result = get_schema_from_template(schema)

        # postcondition
        self.assertEqual(result, schema)

    def test_no_blocks_layout_in_properties_returns_same_schema(self):
        # setup
        schema = {"properties": {}}
        mock_request = MagicMock()

        # do it
        with patch("interaktiv.templates.utilities.helper.getRequest", return_value=mock_request):
            result = get_schema_from_template(schema)

        # postcondition
        self.assertEqual(result, schema)

    def test_template_not_found_returns_same_schema(self):
        # setup
        schema = {"properties": {"blocks_layout": {}}}
        mock_request = MagicMock()
        mock_request.form = {"template": "nonexistent-template-id"}

        # do it
        with patch("interaktiv.templates.utilities.helper.getRequest", return_value=mock_request):
            result = get_schema_from_template(schema)

        # postcondition
        self.assertEqual(result, schema)

    def test_template_blocks_missing_returns_same_schema(self):
        # setup
        schema = {"properties": {"blocks_layout": {}}}
        mock_request = MagicMock()
        mock_request.form = {"template": "template-id"}
        mock_template = MagicMock()
        mock_template.blocks = {}
        mock_template.blocks_layout = {}

        # do it
        with patch("interaktiv.templates.utilities.helper.getRequest", return_value=mock_request), \
                patch("interaktiv.templates.utilities.helper.uuidToObject", return_value=mock_template):
            result = get_schema_from_template(schema)

        # postcondition
        self.assertEqual(result, schema)

    def test_schema_updated_with_template_blocks(self):
        # setup
        schema = {
            "properties": {
                "blocks": {"default": {}},
                "blocks_layout": {"default": {"items": []}},
            }
        }
        mock_request = MagicMock()
        mock_request.form = {"template": "template-id"}
        mock_template = MagicMock()
        mock_template.blocks = {"block-1": {"type": "text"}}
        mock_template.blocks_layout = {"items": ["block-1"]}

        # do it
        with patch("interaktiv.templates.utilities.helper.getRequest", return_value=mock_request), \
                patch("interaktiv.templates.utilities.helper.uuidToObject", return_value=mock_template), \
                patch("interaktiv.templates.utilities.helper.uuid4", side_effect=["new-block-id"]):
            result = get_schema_from_template(schema)

        # postcondition
        expected_schema = {
            "properties": {
                "blocks": {
                    "default": {
                        "new-block-id": {"type": "text"}
                    }
                },
                "blocks_layout": {
                    "default": {
                        "items": ["new-block-id"]
                    }
                }
            }
        }
        self.assertEqual(result, expected_schema)
