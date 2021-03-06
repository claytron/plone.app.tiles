# Image scale support for tile images
# -*- coding: utf-8 -*-

from logging import exception
from AccessControl import Unauthorized
from Acquisition import aq_base
from ZODB.POSException import ConflictError

from zope.component import getMultiAdapter
from zope.component import queryUtility

from zope.interface import implements
from zope.interface import Interface

from zope.schema import getFieldsInOrder

from zope.annotation import IAnnotations
from persistent.dict import PersistentDict
from zope.publisher.interfaces import NotFound

from plone import tiles

from plone.app.textfield.interfaces import ITransformer
from plone.app.textfield.value import RichTextValue

from plone.tiles.interfaces import ITileType

from plone.tiles.interfaces import ITileDataManager

from plone.scale.scale import scaleImage
from plone.scale.storage import AnnotationStorage as BaseAnnotationStorage
from plone.namedfile.scaling import ImageScale as BaseImageScale
from plone.namedfile.scaling import ImageScaling as BaseImageScaling
from plone.namedfile.utils import set_headers, stream_data
from plone.namedfile.interfaces import INamedImage
from plone.rfc822.interfaces import IPrimaryFieldInfo

from Products.CMFCore.utils import getToolByName


class AnnotationStorage(BaseAnnotationStorage):
    """ An abstract storage for image scale data using annotations and
        implementing :class:`IImageScaleStorage`. Image data is stored as an
        annotation on the object container, i.e. the image. This is needed
        since not all images are themselves annotatable. """

    @property
    def storage(self):
        tile = self.context
        cover = tile.context
        return IAnnotations(cover).setdefault(
            'plone.tiles.scale.%s' % tile.id,
            PersistentDict())


class ImageScale(BaseImageScale):
    """ view used for rendering image scales """

    def __init__(self, context, request, **info):
        self.context = context
        self.request = request
        self.__dict__.update(**info)
        if self.data is None:
            self.data = getattr(self.context, self.fieldname)
        url = self.context.url
        extension = self.data.contentType.split('/')[-1].lower()
        if 'uid' in info:
            name = info['uid']
        else:
            name = info['fieldname']
        self.__name__ = '%s.%s' % (name, extension)
        self.url = '%s/@@images/%s' % (url, self.__name__)

    def index_html(self):
        """ download the image """
        # validate access
        set_headers(self.data, self.request.response)
        return stream_data(self.data)


class ImageScaling(BaseImageScaling):
    """ view used for generating (and storing) image scales """

    def publishTraverse(self, request, name):
        """ used for traversal via publisher, i.e. when using as a url """
        stack = request.get('TraversalRequestNameStack')
        image = None
        if stack:
            # field and scale name were given...
            scale = stack.pop()
            image = self.scale(name, scale)             # this is aq-wrapped
        elif '-' in name:
            # we got a uid...
            if '.' in name:
                name, ext = name.rsplit('.', 1)
            storage = AnnotationStorage(self.context)
            info = storage.get(name)
            if info is not None:
                scale_view = ImageScale(self.context, self.request, **info)
                return scale_view.__of__(self.context)
        else:
            # otherwise `name` must refer to a field...
            if '.' in name:
                name, ext = name.rsplit('.', 1)
            value = getattr(self.context, name)
            scale_view = ImageScale(self.context, self.request,
                                    data=value, fieldname=name)
            return scale_view.__of__(self.context)
        if image is not None:
            return image
        raise NotFound(self, name, self.request)

    def create(self, fieldname, direction='thumbnail',
               height=None, width=None, **parameters):
        """ factory for image scales, see `IImageScaleStorage.scale` """
        orig_value = self.context.data.get(fieldname)
        if orig_value is None:
            return
        if height is None and width is None:
            _, format = orig_value.contentType.split('/', 1)
            return None, format, (orig_value._width, orig_value._height)
        if hasattr(aq_base(orig_value), 'open'):
            orig_data = orig_value.open()
        else:
            orig_data = getattr(aq_base(orig_value), 'data', orig_value)
        if not orig_data:
            return
        try:
            result = scaleImage(orig_data, direction=direction,
                                height=height, width=width, **parameters)
        except (ConflictError, KeyboardInterrupt):
            raise
        except Exception:
            exception('could not scale "%r" of %r',
                      orig_value, self.context.context.absolute_url())
            return
        if result is not None:
            data, format, dimensions = result
            mimetype = 'image/%s' % format.lower()
            value = orig_value.__class__(data, contentType=mimetype,
                                         filename=orig_value.filename)
            value.fieldname = fieldname
            return value, format, dimensions

    def modified(self):
        """ provide a callable to return the modification time of content
            items, so stored image scales can be invalidated """
        mtime = 0
        for k, v in self.context.data.items():
            if INamedImage.providedBy(v):
                mtime += self.context.data.get('%s_mtime' % k, 0)

        return mtime

    def scale(self, fieldname=None, scale=None,
              height=None, width=None, **parameters):
        if fieldname is None:
            fieldname = IPrimaryFieldInfo(self.context).fieldname
        if scale is not None:
            available = self.getAvailableSizes(fieldname)
            if not scale in available:
                return None
            width, height = available[scale]
        storage = AnnotationStorage(self.context, self.modified)
        info = storage.scale(factory=self.create,
                             fieldname=fieldname, height=height, width=width, **parameters)
        if info is not None:
            info['fieldname'] = fieldname
            scale_view = ImageScale(self.context, self.request, **info)
            return scale_view.__of__(self.context)
