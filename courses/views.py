from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from courses.models import Courses, Lessons, Subscription
from courses.paginations import CoursesPaginator, LessonsPaginator
from courses.serializer import (
    CourseDetailSerializer,
    CourseSerializer,
    LessonSerializer,
    SubscriptionSerializer,
)
from users.permissions import IsModerator, IsOwner


class CourseViewSet(ModelViewSet):
    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Courses.objects.all()
        else:
            return Courses.objects.filter(owner=self.request.user)

    serializer_class = CourseSerializer
    pagination_class = CoursesPaginator

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
    """Создавть могут авторизованные пользователи, которые не являеюся модераторами.
    Также проверяется принадлежность курса пользователю. Если пользователь не является влдельцем курса, то ошибка.
    """

    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        lesson = serializer.save()
        courses_object_list = list(Courses.objects.filter(owner=self.request.user))
        courses_list = []
        for course in courses_object_list:
            courses_list.append(course.id)
        if lesson.course.id not in courses_list:
            raise ValidationError(
                f"Вы не являетесь владельцем курса {lesson.course.name}!"
            )
        lesson.save()

    permission_classes = [IsOwner]


class LessonListApiView(ListAPIView):
    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Lessons.objects.all()
        else:
            return Lessons.objects.filter(owner=self.request.user)

    serializer_class = LessonSerializer
    pagination_class = LessonsPaginator


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
    """Изменять могут авторизованный пользователь, который является владельцем или модератором.
    Также проверяется принадлежность курса пользователю. Если пользователь не является влдельцем курса, то ошибка.
    """

    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Lessons.objects.all()
        else:
            return Lessons.objects.filter(owner=self.request.user)

    def perform_update(self, serializer):
        lesson = serializer.save()
        courses_object_list = list(Courses.objects.filter(owner=self.request.user))
        courses_list = []
        for course in courses_object_list:
            courses_list.append(course.id)
        if lesson.course.id not in courses_list:
            raise ValidationError(
                f"Вы не являетесь владельцем курса {lesson.course.name}!"
            )
        lesson.save()

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


class SubscriptionAPIView(APIView):
    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course = get_object_or_404(Courses, pk=course_id)
        subs_item = Subscription.objects.all().filter(user=user).filter(course=course)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка отключена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка включена"
        return Response({"message": message})
