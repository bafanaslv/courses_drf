from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Courses, Lessons, Subscription
from users.models import User


class CourseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='foxship@yandex.ru')
        self.course = Courses.objects.create(name="Физика", description="Любимый предмет", owner=self.user)
        self.lesson = Lessons.objects.create(name="Оптика", description="Один из лучших", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("courses:lessons_retrieve", args=(self.course.pk,))
        response = self.client.get(url)
        #  print(response.json())
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), self.course.name
        )

    def test_course_create(self):
        url = reverse("courses:course-list")
        data = {
            "name": "Физика",
            "description": "Любимый"
        }
        response = self.client.post(url, data)
        #  print(response.json())
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Courses.objects.all().count(), 2
        )

    def test_course_update(self):
        url = reverse("courses:course-detail", args=(self.course.pk,))
        data = {
            "name": "Физика",
            "description": "Любимый"
        }
        response = self.client.patch(url, data)
        #  print(response.json())
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "Английский"
        )

    def test_course_delete(self):
        url = reverse("courses:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Courses.objects.all().count(), 0
        )

    def test_course_list(self):
        url = reverse('materials:course-list')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='foxship@yandex.ru')
        self.course = Courses.objects.create(name="Физика", description='Любимый курс')
        self.lesson = Lessons.objects.create(name="Механика", course=self.course, description='Интересный', owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("courses:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), self.lesson.name
        )

    def test_lesson_create(self):
        url = reverse("courses:lesson_create")
        data = {
            "name": "Present Perfect",
            'course': self.course.pk
        }
        response = self.client.post(url, data)
        #  print(response.json())
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lessons.objects.all().count(), 2
        )

    def test_lesson_update(self):
        url = reverse("courses:lesson_update", args=(self.lesson.pk,))
        data = {
            "name": "Present Perfect",
            'course': self.course.pk
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "Present Perfect"
        )

    def test_lesson_delete(self):
        url = reverse("courses:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lessons.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse('courses:lesson_list')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='admin@example.com')
        self.course = Courses.objects.create(name="Английский")
        self.lesson = Lessons.objects.create(name="Present Simple", course=self.course, owner=self.user)
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        Subscription.objects.all().delete()
        url = reverse('materials:subscription_create')
        data = {
            'course': self.course.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Subscription.objects.all()[0].course, self.course
        )

    def test_subscription_delete(self):
        url = reverse('materials:subscription_create')
        response = self.client.post(url, {'course': self.course.pk})
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Subscription.objects.count(), 0
        )
