from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from typing import NoReturn

import unittest


class TestCase(unittest.TestCase):
    """
    Base TestCase for interaktiv.templates tests.
    Provides common setup for Plone integration tests.
    """

    layer = None

    def setUp(self) -> None:
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager", "Site Administrator"])

    def tearDown(self) -> NoReturn:
        pass
