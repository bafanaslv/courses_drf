from rest_framework.serializers import ModelSerializer

from courses.models import Courses, Lessons


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Courses
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lessons
        fields = "__all__"
