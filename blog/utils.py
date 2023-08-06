from .models import *


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        auth = self.request.user.is_authenticated
        if auth:
            context['profile_slug'] = self.request.user.username
        context['auth'] = auth
        return context
