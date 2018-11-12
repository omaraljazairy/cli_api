from configs import configs as conf
import requests
import redis
from services.logger import get_logger
from datetime import datetime, timedelta

logger = get_logger(loggername='requester')
cache = redis.Redis(host=conf.CACHE['REDIS']['URL'], password=conf.CACHE['REDIS']['PASSWORD'])


def make_request( *args, action='str', api=dict,  **kwargs):
    """ 
    makes the http request and returns a response. It takes the following args:
    1- *args: this is an optional args tuple used for the get parameters request. 
            values will be split by a / at the end of the api.
    2- action: this is mandatory str type value that determines the action used in the request.
               possible actions are GET, POST, PUT and DELETE. The value is case insensative.
    3- api: this is a mandatory dict type value that determines the api and it's path to be used.
    4- **kwargs: a key value pair of values used for the params arg in the request. 

    """


    api = conf.API[api[0]][api[1]] # get the api url from the config
    logger.debug("api: %s", api)
    api_request = conf.URL + api # append the api path to the url
    token =  'Bearer '.__add__(get_token()) # get the token from the get_token method.

    # create a header object which can hold other values than the token
    header = {
        "Authorization": token,
    }

    logger.debug("api_request: %s ", api_request)
    logger.debug("action: %s", action)
    logger.debug("header: %s", header)


    if action.upper() == 'GET':

        # if the *args arg contains any values, it will be converted to a string with a / seperater
        api_request = api_request + '/'.join(args) + '/' if args else api_request # + args_params
        response = requests.get(api_request, params=kwargs, headers=header)

        logger.debug("response: %s", response)

        return response

    elif action.upper() == 'POST':

        response = requests.post(api_request, params=kwargs, headers=header)
        logger.debug("response: %s", response)

        return response


    elif action.upper() == 'PUT':

        api_request = api_request + '/'.join(args) + '/' if args else api_request # + args_params
        response = requests.post(api_request, params=kwargs, headers=header)
        logger.debug("response: %s", response)

        return response


    elif action.upper() == 'DELETE':

        api_request = api_request + '/'.join(args) + '/' if args else api_request # + args_params
        response = requests.post(api_request, params=kwargs, headers=header)
        logger.debug("response: %s", response)

        return response

    else:

        return {"ERROR":" Unknown Action"}



def get_token():
    """ 
    returns the token an active to to be used in the request header. It checks first for the
    token in the cache. If it's available, it will return it. If not not, it will call the token api
    to and get the access token and refreshed token. Both will be stored in the cache.  

    """

    token = cache.get('token')
    timediff = get_token_cached_times_diff(cached_key='last_verified')
    logger.debug("timediff: %s", timediff)
    #token_time_diff = datetime.now() - created.decode('ASCII')
    #logger.debug("token_time_diff: %s", token_time_diff)
    # if the token is found in the cache, return it as a decoded string
    if token:
        return token.decode('ASCII')

    else:
        # make a login request to get a token and store it in the cache      

        api_request = conf.URL + conf.API['token']
        response = requests.post(api_request, data={'username': conf.AUTH['user'], 'password': conf.AUTH['password']})
        data = response.json()
        status_code = response.status_code

        logger.debug("response login request status_code: %s ", status_code)
        
        if status_code == 200:
            cache.set('token', data['access'], ex=conf.CACHE['REDIS']['TTL'])
            cache.set('refresh', data['refresh'], ex=conf.CACHE['REDIS']['TTL'])

            token = cache.get('token')
            return token.decode('ASCII')

        else:
            raise Exception("token can not be retrieved")


    

#TODO
#refresh method

def get_token_cached_times_diff(cached_key=str, unit=str):
    """ return the number of seconds between now and the token creation or verification time """

    
    created = cache.get(cached_key).decode('ASCII')
    created_date = datetime.strptime(created, '%Y-%m-%d %H:%M:%S.%f')
    created_diff = datetime.now() - created_date
    seconds_diff = int(created_diff.total_seconds())
    minutes_diff = int(seconds_diff / 60)
    hours_diff = int(minutes_diff / 60)

    
    logger.debug("datetime value from cache: %s, type: %s", created, type(created))
    logger.debug("created: %s", created)
    logger.debug("created_date: %s", created_date)
    logger.debug("created_diff: %s", created_diff)

    if unit == 'seconds':

        #seconds_diff = int(created_diff.total_seconds())
        logger.debug("created_diff seconds: %s", seconds_diff)
        return seconds_diff


    elif unit == 'minutes':

        #minutes = int(created_diff.total_seconds() / 60)
        logger.debug("created_diff minutes: %s", minutes_diff)
        return minutes_diff

    elif unit == 'hours':

        logger.debug("created_diff hours: %s", hours_diff)
        return hours_diff
        

    else:
        logger.debug("created_diff: %s", created_diff)
        return created_diff


'''
http POST 0.0.0.0:8000/api/token/refresh/ refresh=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU0MTcxMDk2OCwianRpIjoiNjg3MDY0ODkxN2JiNGIzNjk5NjU4ODUzY2NiOGJiM2MiLCJ1c2VyX2lkIjoyfQ.T1DZ9OWhCTNCezsAlE34knnQO1aC3HrMwtz0pPWADa8
HTTP/1.1 200 OK
Allow: POST, OPTIONS
Content-Length: 218
Content-Type: application/json
Date: Wed, 07 Nov 2018 21:05:00 GMT
Server: WSGIServer/0.2 CPython/3.6.4
Vary: Accept
X-Frame-Options: SAMEORIGIN

{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTQxNzA5OTAwLCJqdGkiOiI5YTg2Nzg1M2UxOTA0ZGE5ODk5NzU2N2RlNTY3ZjBiOSIsInVzZXJfaWQiOjJ9.zeFovVcOlgqedFsUOfoDpeJYjoyJ8_k_Nei9SV7QH88"
}
'''
