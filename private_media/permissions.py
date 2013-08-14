
class DefaultPrivatePermissions(object):
    
    def has_read_permission(self, request, path):
        """
        Just return True if the user is an authenticated staff member.
        Extensions could base the permissions on the path too.
        """
        user = request.user
        if not user.is_authenticated():
            return False
        elif user.is_superuser:
            return True
        elif user.is_staff:
            return True
        else:
            return False

