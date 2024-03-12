from django.conf import settings
from django.shortcuts import render
import traceback
import logging

logger = logging.getLogger("django")

class CustomExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            debug = settings.DEBUG
            message = str(e)
            traceback_description = traceback.format_exc()
            logger.error(f"{message} \n {traceback_description}")
            if not debug:
                message = "Something went wrong. Please try again. If issue occurs again, please contact technical team."
                traceback_description = ""
            return render(request, "user/error.html", {"message": message, "traceback_description": traceback_description})
        
