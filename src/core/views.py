import datetime
import functools
import inspect
import json
import traceback
from django.db import transaction
from django.http import JsonResponse
from django.views import View


JSON_DUMPS_PARAMS = {
    'ensure_ascii': False
}


def ret(json_object, status=400):
    """
    Отдает JSON с правильными HTTP заголовками и в читаемом в браузере
    виде в случае с кириллицей.
    """
    return JsonResponse(
        json_object,
        status=status,
        safe=not isinstance(json_object, list),
        json_dumps_params=JSON_DUMPS_PARAMS
    )


def error_response(exception):
    """
    Формирует HTTP response с описанием ошибки и Traceback
    """
    # TODO
    # Если DEBUG = True, то не возвращать traceback
    res = {
        'errorMessage': str(exception),
        'traceback': traceback.format_exc()
    }

    return ret(res, status=400)


def base_view(func):
    """
    Декоратор для всех view, который обрабатывает исключения.
    """
    @functools.wraps(func)
    def inner(request, *args, **kwargs):
        try:
            with transaction.atomic():
                return func(request, *args, **kwargs)
        except Exception as ex:
            return error_response(ex)

    return inner


class BaseView(View):
    """
    Базовый класс для всех view, который обрабатывает исключения
    """
    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, **args, **kwargs)
        except Exception as ex:
            return self._response({'errorMessage': ex.message}, status=400)

        if isinstance(response, (dict, list)):
            return self._response(response)
        else:
            return response

    @staticmethod
    def _response(data, *, status=200):
        return JsonResponse(
            data,
            status=status,
            safe=not isinstance(data, list),
            json_dumps_params=JSON_DUMPS_PARAMS
        )

