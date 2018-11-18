from fedal_cli.configs import settings as conf
from fedal_cli.services.requester import make_request
from fedal_cli.services.tokens import get_token, get_token_cached_times_diff, set_token, verify_token, refresh_token
from nose.tools import assert_true, assert_equal, assert_false, assert_raises
from fedal_cli.services.logger import get_logger
import redis
from datetime import datetime, timedelta

cache = redis.Redis(host=conf.CACHE['REDIS']['URL'], password=conf.CACHE['REDIS']['PASSWORD'])
logger = get_logger(loggername='test')

class TestTokens:


    def setUp(self):
        """ set up test before every function is executed """

        cache.delete('token')
        cache.delete('refresh')
        cache.delete('last_verified')

        logger.debug("all cached keys are deleted")
        logger.debug("setup_func executed")
        


    def test_get_token(self):
        """ expects to return a token from the token api. the token should be stored in the cache """

        token = get_token()
        
        cached_token = cache.get('token').decode('ASCII')
        refreshed_token = cache.get('refresh').decode('ASCII')

        assert_equal(token, cached_token)
        #assert_true(True)


    def test_get_token_existing_token_and_verified(self):
        """ 
        sets a token and a last_verified records in the cache. expects to return a token from the token api. 
        the token should be stored in the cache. 
        """

        test_token = 'test_token'
        cache.set('token', test_token, ex=conf.CACHE['REDIS']['TTL'])
        cache.set('last_verified', datetime.now())
                
        token = get_token()

        logger.debug("test_token created and token retrieved from get_token: %s - %s", test_token, token)
        
        assert_equal(token, test_token)


    def test_get_token_not_valid_token_not_verified(self):
        """ 
        set a token and a last_verified more than 10 minutes. expects to get a new token becasue 
        the token doesn't exist.
        """

        test_token = 'test_token'
        last_verified = datetime.now() + timedelta(minutes=-11)
        
        cache.set('token', test_token, ex=conf.CACHE['REDIS']['TTL'])
        cache.set('last_verified', last_verified)

        time_diff = get_token_cached_times_diff(cached_key='last_verified', unit='minutes')
        
        new_token = get_token()
        logger.debug("timediff min: %s", time_diff)
        logger.debug("old token: %s - new token: %s", test_token, new_token)

        assert_false(test_token == new_token)


    def test_get_token_existing_token_not_verified(self):
        """ 
        create a new token, change the last_verified to be more than 10 min. call get_token again.
        token returned should be the same in the cache.
        """

        # create a new token
        token1 = get_token()

        #change the last verified to be more than 10 minutes
        last_verified = datetime.now() + timedelta(minutes=-11)
        cache.set('last_verified', last_verified)

        token2 = get_token()
        logger.debug("token1: %s - token2: %s", token1, token2)

        assert_equal(token1, token2)
        


    def test_get_token_invalid_token_get_new_from_refresh(self):
        """
        create a new token, change the token and the last_verified. expect to use
        the refresh to get a new token and no referesh will be in the cache.
        """

        # create a new token
        token1 = get_token()

        # modify the token and change the last_verified in the cache
        # so the verify api will be called, the response will be false and
        # refresh api to be used

        last_verified = datetime.now() + timedelta(minutes=-11)

        cache.set('token','invalis_token')
        cache.set('last_verified', last_verified)

        token2 = get_token()
        refresh_token = cache.get('refresh')

        logger.debug("new_token: %s", token2)
        logger.debug("refresh_token: %s", refresh_token)

        assert_false(token1 == token2)
        assert_false(refresh_token)
        
        
    def test_set_token_ok(self):
        """ 
        makes a request to the set_token method. expects a token and a refresh token to be 
        created and saved in the cache. expect the token is not the same as the refresh token.
        """

        request_set_token = set_token()
        cached_token = cache.get('token').decode('ASCII')
        refreshed_token = cache.get('refresh').decode('ASCII')
        last_verified = cache.get('last_verified')

        logger.debug("token from set_token: %s", cached_token)
        logger.debug("refresh token from set_token: %s", refreshed_token)
        logger.debug("last_verified from set_token: %s", last_verified)

       
        assert_true(cached_token != refreshed_token)
        assert_true(bool(last_verified))



    def test_set_token_error(self):
        """ 
        makes a request to the set_token method with the test user. expects an error. 
        """

        with assert_raises(Exception):
            set_token(user='test')



    def test_verify_token_ok(self):
        """ makes a new token, and verifies it. expects to get True """

        request_set_token = set_token()
        token = cache.get('token').decode('ASCII')
        verify_token_response = verify_token(token=token)

        logger.debug("verify_token_response: %s", verify_token_response)

        assert_true(verify_token_response)
        


    def test_verify_token_False(self):
        """ makes a verify token request with an invalid token. expects to get False """

        verify_token_response = verify_token(token='bla')

        logger.debug("verify_token_response: %s", verify_token_response)

        assert_false(verify_token_response)


    def test_refresh_token_ok(self):
        """ 
        makes a request to the set_token to create a token. expects a token. calls the refresh
        refresh token with the refreshed_token and expects to get a new token.
        """

        request_set_token = set_token()
        cached_token = cache.get('token').decode('ASCII')
        refreshed_token = cache.get('refresh').decode('ASCII')
        last_verified = cache.get('last_verified')

        logger.debug("token from set_token: %s", cached_token)
        logger.debug("refresh token from set_token: %s", refreshed_token)
        logger.debug("last_verified from set_token: %s", last_verified)

        new_token = refresh_token()
        logger.debug("new_token: %s", new_token)
        
        
        assert_true(cached_token != new_token)
        assert_true(bool(last_verified))

   
    def test_refresh_token_error(self):
        """ 
        makes a refresh token request when there is no refreshed token stored in the cache.
        expects a False response 
        """

        refresh_token_response = refresh_token()

        logger.debug("refresh_token_response: %s", refresh_token_response)

        assert_false(refresh_token_response)
        
        
    def test_get_token_cached_times_diff_seconds(self):
        """ 
        create a test cache record for a token creation date and compares with the datetime
        of now. expects to get the difference in seconds.
        """

        yesterday_date = datetime.now() + timedelta(days=-1)
        cache.set('test_token_creation', yesterday_date)
        logger.debug("get_test_token_creation: %s", cache.get('test_token_creation'))

        get_timediff_seconds = get_token_cached_times_diff(cached_key='test_token_creation', unit='seconds')

        logger.debug("get_timediff_seconds: %s", get_timediff_seconds)

        deleted_key = cache.delete('test_token_creation')
        logger.debug("deleted_key: %s", deleted_key)

        assert_equal(get_timediff_seconds, 86400)



    def test_get_token_cached_times_diff_minutes(self):
        """ 
        create a test cache record for a token creation date and compares with the datetime
        of now. expects to get the difference in minutes.
        """

        yesterday_date = datetime.now() + timedelta(days=-1)
        cache.set('test_token_creation', yesterday_date)
        logger.debug("get_test_token_creation: %s", cache.get('test_token_creation'))

        get_timediff_minutes = get_token_cached_times_diff(cached_key='test_token_creation', unit='minutes')

        logger.debug("get_timediff_minutes: %s", get_timediff_minutes)

        deleted_key = cache.delete('test_token_creation')
        logger.debug("deleted_key: %s", deleted_key)
        
        assert_equal(get_timediff_minutes, 1440)


    def test_get_token_cached_times_diff_hours(self):
        """ 
        create a test cache record for a token creation date and compares with the datetime
        of now. expects to get the difference in hours.
        """

        yesterday_date = datetime.now() + timedelta(days=-1)
        cache.set('test_token_creation', yesterday_date)
        logger.debug("get_test_token_creation: %s", cache.get('test_token_creation'))

        get_timediff_hours = get_token_cached_times_diff(cached_key='test_token_creation', unit='hours')

        logger.debug("get_timediff_hours: %s", get_timediff_hours)

        deleted_key = cache.delete('test_token_creation')
        logger.debug("deleted_key: %s", deleted_key)
        
        assert_equal(get_timediff_hours, 24)



    def test_get_token_cached_times_diff_default(self):
        """ 
        create a last_verified record in the cache and call the 
        token_cache_times_diff without providing a unit. expect to get a 
        timedelta type object.
        """


        yesterday_date = datetime.now() + timedelta(days=-1)
        cache.set('last_verified', yesterday_date)
        logger.debug("get_test_token_creation: %s", cache.get('last_verified'))

        get_time_diff = get_token_cached_times_diff(cached_key='last_verified')

        logger.debug("get_time_diff: %s", get_time_diff)
        logger.debug("type(get_time_diff): %s", type(get_time_diff))
        #created_date = datetime.strptime(created, '%Y-%m-%d %H:%M:%S.%f')
        assert_true(type(get_time_diff) == timedelta)
         
        
    def tearDown(self):
        "tear down at the end of every test by removing the cache"

        logger.debug("teardown_func executed")

        cache.delete('token')
        cache.delete('refresh')
        cache.delete('last_verified')

        logger.debug("all cached keys are deleted")
