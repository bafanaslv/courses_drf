from django.db import models

from config import settings

NULLABLE = {"blank": True, "null": True}


class Courses(models.Model):
    name = models.CharField(max_length=150, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    image = models.ImageField(
        upload_to="courses/media",
        verbose_name="изображение",
        help_text="загрузите изображение",
        **NULLABLE,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="владелец",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"

    def str(self):
        return f"Курс: {self.name}"


class Lessons(models.Model):
    name = models.CharField(max_length=150, verbose_name="название")
    course = models.ForeignKey(
        Courses, related_name="courses", on_delete=models.CASCADE, verbose_name="курс"
    )
    description = models.TextField(verbose_name="описание")
    image = models.ImageField(
        upload_to="lessons/media",
        verbose_name="изображение",
        help_text="загрузите изображение",
        **NULLABLE,
    )
    video = models.ImageField(
        upload_to="video/media",
        verbose_name="видеоурок",
        help_text="загрузите видеоурок",
        **NULLABLE,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="владелец",
        **NULLABLE,
    )

    def str(self):
        return f"Урок: {self.name}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
