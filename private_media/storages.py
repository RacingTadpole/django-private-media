from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings

"""
Key parts of this code are based on code by Stephan Foulis and contributors
from django-filer.

To upload to a private location, add to your settings.py e.g.:

PRIVATE_MEDIA_URL = '/private/'
if DEBUG:
    # dev
    import os
    PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
    PRIVATE_MEDIA_ROOT = os.path.join(PROJECT_PATH, 'private')
    PRIVATE_MEDIA_SERVER = 'private_media.servers.DefaultServer'
else:
    # prod
    PRIVATE_MEDIA_ROOT = '/home/user/my/path/to/private/media'
    PRIVATE_MEDIA_SERVER = 'private_media.servers.ApacheXSendfileServer'
    #PRIVATE_MEDIA_SERVER_OPTIONS = {'arg1': 1, ...}  # (optional) kwargs to init server

The default permissioning is for authenticated staff members to see all, and no one else.
To generalise this, also add:

PRIVATE_MEDIA_PERMISSIONS = 'myapp.permissions.MyPermissionClass'
PRIVATE_MEDIA_PERMISSIONS_OPTIONS = {'arg1': 1, ...}  # (optional) kwargs to init

This permissions class must have the method:
    has_read_permission(self, request, path)
which returns True or False.


Add to your INSTALLED_APPS:

INSTALLED_APPS = {
    ...
    'private_media',
    ...
}


Add to urls.py:
       ...
       url(r'^', include('private_media.urls')),


In your models.py, to upload a specific file or image to a private area, use:

    from django.db import models
    from private_media.storages import PrivateMediaStorage

    class Car(models.Model):
        photo = models.ImageField(storage=PrivateMediaStorage())


Because the only information about the file available to the permissions method
is its path, you will need to encode the allowed permissioning into the path on upload.

E.g. you could use this to save the owner's primary key into the path:

    import os
    from django.db import models
    from django.contrib.auth.models import User
    from private_media.storages import PrivateMediaStorage

    def owner_file_name(instance, filename):
        return os.path.join('cars', "{0}".format(instance.user.pk), filename)

    class Car(models.Model):
        owner = models.ForeignKey(User)
        photo = models.ImageField(storage=PrivateMediaStorage(), upload_to=owner_file_name)

And then provide a permissioning class like this (which lets staff and the owner see it):

    import os
    from django.http import Http404

    class OwnerPkPermissions(object):
        def has_read_permission(self, request, path):
            user = request.user
            if not user.is_authenticated():
                return False
            elif user.is_superuser:
                return True
            elif user.is_staff:
                return True
            else:
                try:
                    owner_pk = int(os.path.split(os.path.split(z)[0])[1])
                except ValueError:
                    raise Http404('File not found')
                return (user.pk==owner_pk)

Caveat - I have not tested this, and exposing user's primary keys is potentially insecure.

"""
#
# Could also implement this simply as:
#
# private_media = FileSystemStorage(location=settings.PRIVATE_MEDIA_ROOT, 
#                                   base_url=settings.PRIVATE_MEDIA_URL,
#                                   )

class PrivateMediaStorage(FileSystemStorage):
    def __init__(self, location=None, base_url=None):
        if location is None:
            location = settings.PRIVATE_MEDIA_ROOT
        if base_url is None:
            base_url = settings.PRIVATE_MEDIA_URL
        return super(PrivateMediaStorage, self).__init__(location, base_url)

