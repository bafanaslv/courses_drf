from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from courses.models import Courses, Lessons
from courses.serializer import (CourseDetailSerializer, CourseSerializer,
                                LessonSerializer)
from users.permissions import IsModerator, IsOwner


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
        if self.action == 'create':
            self.permission_classes = [~IsModerator, IsAuthenticated,]
        elif self.action == 'destroy':
            self.permission_classes = [~IsModerator, IsOwner,]
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = [IsModerator | IsOwner,]
        elif self.action == 'list':
            self.permission_classes = [IsModerator, IsAuthenticated]
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
    permission_classes = [IsModerator | IsOwner]


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator, IsAuthenticated]
