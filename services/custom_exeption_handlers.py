from rest_framework.views import exception_handler

import sys
import json

def custom_exeption_handlers(exc, context):
    response = exception_handler(exc, context)

    print("Goodbye cruel world", file=sys.stderr)

    if response is not None:
        if type(exc).__name__ == "MethodNotAllowed":
            response.data['response_msg'] = "Method Not Allow"
            response.data['response_code'] = 400
            del response.data['detail']
            response.status_code = 400
        else:
            response.data['response_msg'] = response.data['detail']
            response.data['response_code'] = response.status_code
            del response.data['detail']

    return response
