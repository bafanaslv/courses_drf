from courses.models import Lessons
from users.permissions import IsModerator


class QuerysetMixin:
    """Миксин для получения прав на объекты уроков."""

    def get_queryset(self, **kwargs):
        if IsModerator().has_permission(**kwargs):
            return Lessons.objects.all()
        else:
            return Lessons.objects.filter(owner=self.kwargs["pk"])
