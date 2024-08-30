from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from courses.models import Subscription
from users.models import User


@shared_task
def send_mail_update_course(course_id):
    """Функция отправки уведомлений при обновлении курса"""
    # Полученаем подписчиков
    subscribers = Subscription.objects.filter(course=course_id)
    if subscribers:
        for sub in subscribers:
            to_email = sub.user.email
            subject = "Обновления материалов курса"
            message = "Курс обновлен"
            send_mail(
                subject=subject,
                message=message,
                recipient_list=[to_email],
                from_email=EMAIL_HOST_USER,
                fail_silently=True,
            )


@shared_task
def check_login():
    """Проверяет и деактивирует пользователей, которые не заходили в систему в течении 30 дней."""
    users = User.objects.filter(
        last_login__lte=timezone.now() - timedelta(days=30), is_active=True
    )
    for user in users:
        # обходим суперпользователя
        if not user.is_superuser:
            user.is_active = False
            user.save()
