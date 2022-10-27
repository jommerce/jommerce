from .models import Session, AnonymousUser
from django.http import HttpRequest
from django.utils import timezone
from django.conf import settings


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        try:
            session = Session.objects.get(pk=request.COOKIES.get(settings.AUTH_SESSION_COOKIE_NAME, None))
        except Session.DoesNotExist:
            request.session = Session()
            request.user = AnonymousUser()
        else:
            if session.expire_date <= timezone.now():
                session.delete()
                request.session = Session()
            else:
                request.session = session
            request.user = session.user or AnonymousUser()

        response = self.get_response(request)

        request.session.save()

        if request.session.user:
            response.set_cookie(
                settings.AUTH_SESSION_COOKIE_NAME,
                request.session.id,
                expires=request.session.expire_date,
                domain=settings.AUTH_SESSION_COOKIE_DOMAIN,
                path=settings.AUTH_SESSION_COOKIE_PATH,
                secure=settings.AUTH_SESSION_COOKIE_SECURE,
                httponly=settings.AUTH_SESSION_COOKIE_HTTPONLY,
                samesite=settings.AUTH_SESSION_COOKIE_SAMESITE,
            )
        return response
