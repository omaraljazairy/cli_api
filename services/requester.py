from configs import settings as conf, apis
import requests
from services.logger import get_logger
from datetime import datetime, timedelta
from services.tokens import get_token

logger = get_logger(loggername='requester')


def make_request( *args, action='str', api=dict,  **kwargs):
    """ 
    makes the http request and returns a response. It takes the following args:
    1- *args: this is an optional args tuple used for the get parameters request. 
            values will be split by a / at the end of the api. all values have to be a string.
    2- action: this is mandatory str type value that determines the action used in the request.
               possible actions are GET, POST, PUT and DELETE. The value is case insensative.
    3- api: this is a mandatory dict type value that determines the api and it's path to be used.
    4- **kwargs: a key value pair of values used for the params arg in the request. 

    """


    api = apis.API[api[0]][api[1]] # get the api url from the config
    logger.debug("api: %s", api)
    api_request = conf.API_URL + api # append the api path to the url
    token =  'Bearer '.__add__(get_token()) # get the token from the get_token method.

    # create a header object which can hold other values than the token
    header = {
        "Authorization": token,
    }

    logger.debug("========== request setup =========")
    logger.debug("api_request: %s ", api_request)
    logger.debug("action: %s", action)
    logger.debug("header: %s", header)
    logger.debug("args: %s", args)
    logger.debug("params: %s", kwargs)

    logger.debug("========== end request setup =========")

    if action.upper() == 'GET':

        # if the *args arg contains any values, it will be converted to a string with a / seperater
        
        api_request = api_request + '/'.join(args) + '/' if args else api_request # + args_params
        logger.debug("get api_request: %s", api_request)
        response = requests.get(api_request, params=kwargs, headers=header)

        logger.debug("response: %s", response)

        return response

    elif action.upper() == 'POST':

        response = requests.post(api_request, data=kwargs, headers=header)
        logger.debug("response: %s", response)

        return response


    elif action.upper() == 'PUT':

        api_request = api_request + '/'.join(args) + '/' if args else api_request # + args_params
        response = requests.patch(api_request, data=kwargs, headers=header)
        logger.debug("response: %s", response)

        return response


    elif action.upper() == 'DELETE':

        api_request = api_request + '/'.join(args) + '/' if args else api_request # + args_params
        response = requests.delete(api_request, headers=header)
        logger.debug("response: %s", response)

        return response

    else:

        logger.error("unknown action: %s provided", action)
        return {"ERROR":" Unknown Action"}



