from celery import shared_task

from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from courses.models import Subscription


@shared_task
def send_mail_update_course(course_id):
    """Функция отправки уведомлений при обновлении курса"""
    # Полученаем подписчиков
    subscribers = Subscription.objects.filter(course=course_id)

    print(subscribers)
    if subscribers:
        for sub in subscribers:
            to_email = sub.user.email
            subject = 'Обновления материалов курса'
            message = 'Курс обновлен'
            send_mail(
                subject=subject,
                message=message,
                recipient_list=[to_email],
                from_email=EMAIL_HOST_USER,
                fail_silently=True
            )