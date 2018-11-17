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


    def xtest_get_token(self):
        """ expects to have return a token from the token api or the refresh """

        token = get_token()

        
        cached_token = cache.get('token').decode('ASCII')
        refreshed_token = cache.get('refresh').decode('ASCII')

        assert_equal(token, cached_token)
        #assert_true(True)


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

        cache.delete('token')
        cache.delete('refrsh')
        cache.delete('last_verified')
        
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

        cache.delete('token')
        cache.delete('refrsh')
        cache.delete('last_verified')

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

        new_token = refresh_token(refresh_token=refreshed_token)
        logger.debug("new_token: %s", new_token)
        
        cache.delete('token')
        cache.delete('refrsh')
        cache.delete('last_verified')
        
        assert_true(cached_token != new_token)
        assert_true(bool(last_verified))

   
    def test_refresh_token_error(self):
        """ makes a refresh token request with an invalid token. expects a False response """

        refresh_token_response = refresh_token(refresh_token='bla')

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
