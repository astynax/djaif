from django.contrib.auth import authenticate, login
from djaif.settings import SUPERUSER, PASSWORD


def auto_login(get_response):
    def middleware(request):  # noqa: WPS430

        if not request.user.is_authenticated:
            user = authenticate(  # noqa: S106
                username=SUPERUSER, password=PASSWORD,
            )
            login(request, user)

        return get_response(request)

    return middleware
