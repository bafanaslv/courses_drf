from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from courses.apps import CoursesConfig
from courses.views import (CourseViewSet, LessonCreateApiView,
                           LessonDestroyApiView, LessonListApiView,
                           LessonRetrieveApiView, LessonUpdateApiView)

app_name = CoursesConfig.name

router = SimpleRouter()
router.register("", CourseViewSet, basename="course")

urlpatterns = [
    path("lessons/", LessonListApiView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/", LessonRetrieveApiView.as_view(), name="lessons_retrieve"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lessons_create"),
    path(
        "lessons/<int:pk>/delete/",
        LessonDestroyApiView.as_view(),
        name="lessons_delete",
    ),
    path(
        "lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lessons_update"
    ),
]

urlpatterns += router.urls
