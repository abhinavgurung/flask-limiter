
from flask import Flask, jsonify, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps
from werkzeug.exceptions import TooManyRequests
import logging
import traceback
from flask import request

app = Flask(__name__)


limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["4 per day", "4 per hour"],
    storage_uri="memory://",
)

def handle_too_many_requests_error(error):
    """Handle 429 error which rise due to too many requests"""
    logging.error(
        "Too many requests logging ----------------- ")
    # logging.error(traceback.format_exc())
    print('printing request endpoint')
    print(request.endpoint)
    print('request endpoint printed')

    if not is_authenticated():
        return {"message:": "UnAuthorized"}, 401

    return {"message:": "custom too many requests"}, 429


app.register_error_handler(TooManyRequests, handle_too_many_requests_error)

# # Custom decorator for authentication
# def authenticated_request(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not is_authenticated():
#             print('not authenticated returning 401')
#             return jsonify({"message": "Unauthorized"}), 401

        
#         # check rate limit after authentication
#         else:
#             print('checking limiter check')
#             resp = limiter.check()
#             if resp and resp[1]:
#                 print('returning 429...')
#                 return jsonify({"message": "Rate limit exceeded"}), 429

#         return f(*args, **kwargs)
#     return decorated_function

# def authenticated_request(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not is_authenticated():
#             print('not authenticated returning 401')
#             return jsonify({"message": "Unauthorized"}), 401
        
#         # Proceed if authenticated
#         result = f(*args, **kwargs)
        
#         # Check rate limit after executing the endpoint function
#         print('checking limiter check')
#         resp = limiter.check()
#         print(resp)
#         print(resp[1])
#         if resp and resp[1]:
#             print('returning 429...')
#             return jsonify({"message": "Rate limit exceeded"}), 429
        
#         return result

#     return decorated_function

def authenticated_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            return jsonify({"message": "Unauthorized"}), 401
        
        # Execute the endpoint function
        result = f(*args, **kwargs)
        
        # Check rate limit after executing the endpoint function
        resp = limiter.check()
        if resp and resp[1]:
            return jsonify({"message": "Rate limit exceeded"}), 429
        
        return result

    return decorated_function


def is_authenticated():
    return True

@app.route('/example')
@authenticated_request
def example_route():
    return jsonify({"message": "This is an example route"})

@app.route('/test')
def test_route():
    return jsonify({"message": "This is an test"})