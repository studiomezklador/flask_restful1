from flask import jsonify


def err(status_code=404,
        sub_code=None,
        message='Not found.',
        action=None):
    
    """ 
    FROM: 
    http://stackoverflow.com/questions/21638922/custom-error-message-json-object-with-flask-restful
    """

    response = dict(status=status_code,
                  error_code=sub_code,
                  message=message,
                  action=action)
    response.status_code = status_code

    return response
