from rest_framework.serializers import ValidationError

ALLOWED_LINK = "https://www.youtube.com/"
HTTP_LINK_NAME = "youtube"


class AllowedLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        video_url = value.get(self.field)
        if video_url and not video_url.startswith(ALLOWED_LINK):
            raise ValidationError(f"Разрешена ссылка только на {HTTP_LINK_NAME}.")
