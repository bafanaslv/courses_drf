from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from courses.models import Courses, Lessons
from courses.serializer import (CourseDetailSerializer, CourseSerializer,
                                LessonSerializer)
from users.permissions import IsModerator


class CourseViewSet(ModelViewSet):
    queryset = Courses.objects.all()
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
        if self.action in ["create", "destroy"]:
            self.permission_classes = (~IsModerator,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModerator,)
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator, IsAuthenticated]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListApiView(ListAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator, IsAuthenticated]


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator, IsAuthenticated]


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator, IsAuthenticated]


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator, IsAuthenticated]
