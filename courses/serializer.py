from rest_framework.serializers import ModelSerializer, SerializerMethodField
from courses.models import Courses, Lessons


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Courses
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lessons
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    count_lesson_with_same_course = SerializerMethodField()

    def get_count_lesson_with_same_course(self, pk):
        return Lessons.objects.filter(course=pk).count()

    class Meta:
        model = Lessons
        fields = ("name", "description", "count_lesson_with_same_course",)
