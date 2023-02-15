from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class CSRFExemptMixin:
    """Mixin which will help to use csrf_exempt with CBV"""

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)
