import unittest

from zope.component import getMultiAdapter

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from plone.registry import Registry

from Products.CMFCore.utils import getToolByName
from Products.PloneTestCase.ptc import PloneTestCase

from plone.app.tiles.testing import PLONE_APP_TILES_INTEGRATION_TESTING

from plone.app.tiles.interfaces import IDecoSettings


class DecoControlPanelIntegrationTest(PloneTestCase):

    layer = PLONE_APP_TILES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.registry = Registry()
        self.registry.registerInterface(IDecoSettings)

    def test_deco_registry_registered(self):
        self.assertTrue(self.registry.forInterface(IDecoSettings))

    def test_deco_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name="deco-controlpanel")
        view = view.__of__(self.portal)
        self.assertTrue(view())
        self.assertTrue("Deco Controlpanel" in view())

    def test_akismet_controlpanel_view_protected(self):
        from AccessControl import Unauthorized
        self.logout()
        self.assertRaises(
            Unauthorized,
            self.portal.restrictedTraverse,
            '@@deco-controlpanel')

    def test_akismet_in_controlpanel(self):
        self.controlpanel = getToolByName(self.portal, "portal_controlpanel")
        self.assertTrue(
            'deco' in [a.getAction(self)['id']
            for a in self.controlpanel.listActions()])

    def test_available_tiles_key(self):
        record_available_tiles = self.registry.records[
            'plone.app.tiles.interfaces.IDecoSettings.available_tiles']
        self.assertTrue('available_tiles' in IDecoSettings)
        self.assertEqual(record_available_tiles.value, ())


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
