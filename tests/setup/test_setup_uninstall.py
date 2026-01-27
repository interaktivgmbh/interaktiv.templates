from interaktiv.templates import PACKAGE_NAME

import pytest


class TestSetupUninstall:
    @pytest.fixture(autouse=True)
    def uninstalled(self, installer):
        installer.uninstall_product(PACKAGE_NAME)

    def test_addon_uninstalled(self, installer):
        """Test if interaktiv.templates is uninstalled."""
        assert installer.is_product_installed(PACKAGE_NAME) is False

    def test_browserlayer_not_registered(self, browser_layers):
        """Test that IInteraktivTemplatesLayer is not registered."""
        from interaktiv.templates.interfaces import IInteraktivTemplatesLayer

        assert IInteraktivTemplatesLayer not in browser_layers
