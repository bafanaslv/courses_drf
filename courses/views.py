from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from courses.models import Courses, Lessons
from courses.serializer import (CourseDetailSerializer, CourseSerializer,
                                LessonSerializer)
from users.permissions import IsModerator, IsOwner


class CourseViewSet(ModelViewSet):
    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Courses.objects.all()
        else:
            return Courses.objects.filter(owner=self.request.user)

    serializer_class = CourseSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModerator, IsAuthenticated)
        elif self.action in ["update", "retrieve", "list"]:
            self.permission_classes = (IsModerator | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (
                IsAuthenticated,
                ~IsModerator | IsOwner,
            )
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    """Создавть могут авторизованные пользователи, которые не являеюся модераторами."""

    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

    permission_classes = [IsOwner]


class LessonListApiView(ListAPIView):
    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Lessons.objects.all()
        else:
            return Lessons.objects.filter(owner=self.request.user)

    serializer_class = LessonSerializer


class LessonRetrieveApiView(RetrieveAPIView):
    """Просматривать отдельного могут авторизованный пользователь, который является владельцем или модератором."""

    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Lessons.objects.all()
        else:
            return Lessons.objects.filter(owner=self.request.user)

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateApiView(UpdateAPIView):
    """Изменять могут авторизованный пользователь, который является владельцем или модератором."""

    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Lessons.objects.all()
        else:
            return Lessons.objects.filter(owner=self.request.user)

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyApiView(DestroyAPIView):
    """Удалять могут авторизованный пользователь, который является владельцем и не модератором."""

    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Lessons.objects.all()
        else:
            return Lessons.objects.filter(owner=self.request.user)

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | ~IsModerator]
