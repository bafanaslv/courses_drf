from rest_framework.serializers import ModelSerializer, SerializerMethodField

from courses.models import Courses, Lessons


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lessons
        fields = ["name", "course", "description"]


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Courses
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = LessonSerializer(many=True, source="courses", read_only=True)

    def get_count_lessons(self, pk):
        return Lessons.objects.filter(course=pk).count()

    class Meta:
        model = Courses
        fields = ["name", "description", "lessons", "count_lessons"]
