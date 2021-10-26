from django.contrib.sessions.models import Session
import logging

from config.settings import DB

db_logger = logging.getLogger(DB)

# This method enables only one user per session
# In essence, there cannot be two different users using the same session
class OneSessionPerUserMiddleware:
    def __init__(self, get_response):
        db_logger.info("OneSessionPerUserMiddleware: __init__")
        self.get_response = get_response

    def __call__(self, request):
        db_logger.info("OneSessionPerUserMiddleware: __call__")

        if request.user.is_authenticated:
            stored_session_key = request.user.logged_in_user.session_key
            current_session_key = request.session.session_key
            if stored_session_key and stored_session_key != current_session_key:
                Session.objects.get(session_key=stored_session_key).delete()
            request.user.logged_in_user.session_key = current_session_key
            request.user.logged_in_user.save()
        response = self.get_response(request)

        return response
