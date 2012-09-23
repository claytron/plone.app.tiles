import unittest

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from Products.PloneTestCase.ptc import PloneTestCase

from plone.app.tiles.testing import PLONE_APP_TILES_INTEGRATION_TESTING
from plone.tiles.interfaces import ITileType


class TestTile(ITileType):

    def __call__(self):
        return u"<html><body><p>Hello world</p></body></html>"


class AvailableTilesVocabularyIntegrationTest(PloneTestCase):

    layer = PLONE_APP_TILES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_empty_vocabulary(self):
        from plone.app.tiles.vocabularies import available_tiles_vocabulary
        # XXX: This should be 0. The two demo tiles have to be removed.
        self.assertEqual(len(available_tiles_vocabulary(self.portal)), 2)

    def test_register_tile_type_for_vocabulary(self):
        from plone.app.tiles.vocabularies import available_tiles_vocabulary
        from zope.component import getGlobalSiteManager
        gsm = getGlobalSiteManager()

        class TestTile(object):
            pass

        test_tile = TestTile()
        gsm.registerUtility(test_tile, ITileType)
        # XXX: This should be 0. The two demo tiles have to be removed.
        self.assertEqual(len(available_tiles_vocabulary(self.portal)), 3)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
