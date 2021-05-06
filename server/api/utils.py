import base64
import os
from collections.abc import Iterable
import json
from contextlib import contextmanager
from io import BytesIO
from typing import List

import matplotlib.pyplot as plt
from flask import abort, make_response, jsonify
# https://stackoverflow.com/questions/21638922/custom-error-message-json-object-with-flask-restful
from werkzeug.exceptions import HTTPException
from app.extensions import logger
from flask import request, current_app, abort, make_response, jsonify
import jwt
from datetime import datetime, timedelta
import smtplib

error_mapper = {
    500: 'Unexpected server exception',
    400: 'Missing on or more fields',
    401: 'Unauthorized',
    404: 'Not found',
    409: 'Already exists'
}


def is_valid_model_name(name):
    return name in ['markowitz', 'blackLitterman', 'mean_gini', 'Kmeans']



def reset_pass_mail(to_addr, subject, content) -> None:
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.header import Header

    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USER = os.getenv('GMAIL_USER')
    FROM_ADDR = SMTP_USER
    SMTP_PASSWORD = os.getenv('GMAIL_PASSWORD')

    msg = MIMEMultipart('alternative')
    msg.set_charset('utf8')

    msg['FROM'] = FROM_ADDR
    msg['Subject'] = Header(subject, "utf-8")
    msg['To'] = to_addr
    _attach = MIMEText(content, 'html', 'UTF-8')
    msg.attach(_attach)
    try:
        server = smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(FROM_ADDR, [to_addr], msg.as_string())
        server.quit()
        server.close()
    except Exception as e:
        print('Error sending password reset mail')
        print(e)



def exceptions_mapper(status, suffix=''):
    if not isinstance(suffix, str) and isinstance(suffix, Iterable):
        suffix = f': {", ".join(suffix)}'
    elif len(suffix) > 0:
        suffix = f': {suffix}'
    if status not in error_mapper:
        return error_mapper[500], "Status not found."
    return status, error_mapper[status] + suffix


def plt_to_src(fig):
    io = BytesIO()
    fig.savefig(io, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    data = base64.encodebytes(io.getvalue()).decode('utf-8')
    html_img_src = f'data:image/png;base64,{data}'
    return html_img_src


def json_abort(status_code, message="", exception=None):
    if exception:
        # If the exception is already of type HTTPException, meaning from previous call to abort
        # collect the message and simply raise the abort again(do not call abort again, only reraise)
        if isinstance(exception, HTTPException):
            try:
                res = json.loads(exception.get_response().get_data().decode())
                status_code = res.get('code')
                message = res.get('message')
            except Exception:
                logger.exception('Invalid response format')
            raise  # To reraise the exception thrown from abort(..) call below
        else:
            # Note that if not isinstance(exception, HTTPException), then I simply have an exception,
            # meaning I should call abort, but before, remember, I'm inside except block
            # so I should call logger.exception, note that if isinstance(exception, HTTPException)
            # for now I simply want an info.
            logger.exception(message)

    else:
        logger.error('json_abort, no exception, message: ' + message)

    # We always want here call to abort
    abort(make_response(jsonify({"message": message, "code": status_code}), status_code))
    # abort(make_response(jsonify(message=message), status_code))


def token_required(f):
    from models.users import User
    def wrapper(*args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization')
            access_token = auth_header.split(' ')[1]
            token = jwt.decode(access_token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            curr_user = User.query.get(token['uid'])
            if not curr_user:
                raise jwt.InvalidTokenError("Member not found")

        except Exception as e:
            json_abort(401, "Invalid/Expired token", e)
        return f(*args, **kwargs, curr_user=curr_user)

    wrapper.__doc__ = f.__doc__
    wrapper.__name__ = f.__name__
    return wrapper


def get_tokens(user_id, app):
    _access_token = jwt.encode({'uid': user_id,
                                'exp': datetime.utcnow() + timedelta(minutes=720),
                                'iat': datetime.utcnow()},
                               app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
    return _access_token
