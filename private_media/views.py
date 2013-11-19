#-*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.core.files.base import File
from django.core.files.storage import get_storage_class
from . import servers

import logging
logger = logging.getLogger(__name__)

from django.utils.importlib import import_module

def get_class(import_path=None):
    """
    Largely based on django.core.files.storage's get_storage_class
    """
    from django.core.exceptions import ImproperlyConfigured
    if import_path is None:
        raise ImproperlyConfigured('No class path specified.')
    try:
        dot = import_path.rindex('.')
    except ValueError:
        raise ImproperlyConfigured("%s isn't a module." % import_path)
    module, classname = import_path[:dot], import_path[dot+1:]
    try:
        mod = import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured('Error importing module %s: "%s"' % (module, e))
    try:
        return getattr(mod, classname)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" class.' % (module, classname))


server = get_class(settings.PRIVATE_MEDIA_SERVER)(**getattr(settings, 'PRIVATE_MEDIA_SERVER_OPTIONS', {}))
if hasattr(settings,'PRIVATE_MEDIA_PERMISSIONS'):
    permissions = get_class(settings.PRIVATE_MEDIA_PERMISSIONS)(**getattr(settings, 'PRIVATE_MEDIA_PERMISSIONS_OPTIONS', {}))
else:
    from .permissions import DefaultPrivatePermissions
    permissions = DefaultPrivatePermissions()


def serve_private_file(request, path):
    """
    Serve private files to users with read permission.
    """
    logger.debug('Serving {0} to {1}'.format(path, request.user))
    if not permissions.has_read_permission(request, path):
        if settings.DEBUG:
            raise PermissionDenied
        else:
            raise Http404('File not found')
    return server.serve(request, path=path)
