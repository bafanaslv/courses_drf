from rest_framework.serializers import ModelSerializer, SerializerMethodField
from courses.models import Courses, Lessons, Subscription
from courses.validators import AllowedLinkValidator


class LessonSerializer(ModelSerializer):
    validators = [AllowedLinkValidator(field="video")]

    class Meta:
        model = Lessons
        fields = ["id", "name", "course", "description", "video", "owner"]


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Courses
        fields = "__all__"


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = LessonSerializer(many=True, source="courses", read_only=True)
    subscription = SubscriptionSerializer(
        many=True, source="subscription_course", read_only=True
    )

    def get_count_lessons(self, pk):
        return Lessons.objects.filter(course=pk).count()

    class Meta:
        model = Courses
        fields = [
            "id",
            "name",
            "description",
            "lessons",
            "count_lessons",
            "subscription",
        ]
