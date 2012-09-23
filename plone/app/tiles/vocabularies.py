# -*- coding: utf-8 -*-
from zope.component import getUtilitiesFor
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.tiles.interfaces import ITileType


def available_tiles_vocabulary(context):
    terms = []
    for tile_type in getUtilitiesFor(ITileType):
        terms.append(
            SimpleTerm(
                value=tile_type[0],
                token=tile_type[0],
                title=tile_type[0]))
    return SimpleVocabulary(terms)
