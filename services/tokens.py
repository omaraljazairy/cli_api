from fedal_cli.configs import settings as conf
import requests
import redis
from fedal_cli.services.logger import get_logger
from datetime import datetime, timedelta

logger = get_logger(loggername='tokens')
cache = redis.Redis(host=conf.CACHE['REDIS']['URL'], password=conf.CACHE['REDIS']['PASSWORD'])


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
        logger.debug("token found in the cache")
        if get_token_cached_times_diff(cached_key='token', unit='minutes') < 10:
            logger.debug("token was verified in less then 10 minutes")
            return token.decode('ASCII')
        else:
            logger.debug("token was checked more then 10 minutes. going to verify it")
            api_request = conf.URL + conf.API['token']['verify']            
            response = request.post(api_request, data={'token': token})
            if response.status_code == 200:
                logger.debug("response from verify is 200")
                return token
            else:
                logger.debug("response is not 200. token is not valid anymore. going to get a new one from the refresh api")
                api_request = conf.URL + conf.API['token']['refresh']
                response = request.post(api_request, data={'refresh': cache.get('refresh')})
                if response.status_code == 200:
                    logger.debug("response is 200. storing the token in the cache and removing the refresh token")
                    cache.set('token', data['access'], ex=conf.CACHE['REDIS']['TTL'])
                    cache.delete('refresh')
                
            

    else:
        # make a login request to get a token and store it in the cache      

        logger.debug("token not in cache")
    

def set_token(user='omar'):
    """ 
    fetches a new token from the token api and stores it in the cache with the keys token and refresh 
    it will throw an exception if the status code not 200.
    """

    api_request = conf.URL + conf.API['token']['token']
    response = requests.post(api_request, data={'username': user, 'password': conf.AUTH[user]})
    data = response.json()
    status_code = response.status_code

    logger.debug("response login request status_code: %s ", status_code)
       
    if status_code == 200:
        try:
            cache.set('token', data['access'], ex=conf.CACHE['REDIS']['TTL'])
            cache.set('refresh', data['refresh'], ex=conf.CACHE['REDIS']['TTL'])
            cache.set('last_verified', datetime.now())

            token = cache.get('token')
            return token.decode('ASCII')
        except Exception as e:
            logger.error("redis could not save into cache. message: %s", str(e))
            
    else:
        err_msg = data
        logger.error("could not get a new token: %s - %s", status_code, data)
        raise Exception("token can not be set")



def refresh_token(refresh_token=str):
    """ 
    takes the refresh_token and calls the refresh api to get a new token. the new token will be saved in the cache
    and returned. the refreshed token will be removed from the cache.
    it will return False if the refresh api doesn't return 200.
    """

    logger.debug("received refreshed_token: %s", refresh_token)
    api_request = conf.URL + conf.API['token']['refresh']
    response = requests.post(api_request, data={'refresh': refresh_token})
    data = response.json()
    status_code = response.status_code
    logger.debug("response: %s", data)

    if response.status_code == 200:
        logger.debug("response is 200. storing the token in the cache and removing the refresh token")

        try:
            cache.set('token', data['access'], ex=conf.CACHE['REDIS']['TTL'])
            cache.delete('refresh')
            logger.debug("token saved and refresh is removed from cache")

            token = cache.get('token')
            return token.decode('ASCII')

        except Exception as e:
            logger.error("redis could not save into cache. message: %s", str(e))
            

    else:
        err_msg = data
        logger.error("refresh token could not be retrieved: %s", err_msg)
        return False



def verify_token(token=str):
    """ 
    takes a token parameter and verifies it. it will return true if it's correctly verified, otherwise
    it will return False.
    """

    api_request = conf.URL + conf.API['token']['verify']
    response = requests.post(api_request, data={'token': token})

    logger.debug("statuscode from verify: %s", response.status_code)
    
    if response.status_code == 200:
        logger.debug("response from verify is 200")
        try:
            cache.set('last_verified', datetime.now())
            return True
        except Exception as e:
            logger.error("redis could not save into cache. message: %s", str(e))
            
    else:
        logger.debug("response is not 200. token is not valid anymore. going to get a new one from the refresh api")
        return False

    
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
