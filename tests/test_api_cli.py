from fedal_cli.configs import configs as conf
from services.requester import make_request, get_token, get_token_cached_times_diff
import click
from click.testing import CliRunner
from nose.tools import assert_true, assert_equal
from services.logger import get_logger
import redis
from datetime import datetime, timedelta

cache = redis.Redis(host=conf.CACHE['REDIS']['URL'], password=conf.CACHE['REDIS']['PASSWORD'])
logger = get_logger(loggername='test')




class TestCLI:

    def xtest_make_get_with_args_request(self):
        """ test the make request method with a get action and a tuple of args """

        args_params = ('5',)
        api = ('spanglish', 'word')
        response =  make_request(*args_params, action='GET', api=api, **{})
        content = response.json()
        status_code = response.status_code
        url = response.url

        logger.debug("request => %s", response)
        logger.debug("request status_code: %s", status_code)
        logger.debug("request => %s", url)
        logger.debug("content => %s", content)

        assert_equal(200, status_code)
        assert_true(content)
        assert_equal('http://0.0.0.0:8000/spanglish/word/5/', url)



    def xtest_make_get_with_no_args_request(self):
        """ test the make request method with a get action and no args. """

        api = ('spanglish', 'words')
        response =  make_request(action='GET', api=api, **{})
        content = response.json()
        status_code = response.status_code
        url = response.url

        logger.debug("request => %s", response)
        logger.debug("request status_code: %s", status_code)
        logger.debug("request => %s", url)
        logger.debug("content => %s", content)

        assert_equal(200, status_code)
        assert_true(content)
        assert_equal('http://0.0.0.0:8000/spanglish/words/', url)



    def xtest_make_request_post(self):
        """ expects to create a new word receive status_code 201 """

        api = ('spanglish', 'word')
        params = {
            'word': 'testo',
            'word_en': 'test',
            'category': 'General',
            'language': 'ES',
        }
        response = make_request(action='GET', api=api, **params)

        logger.debug("request => %s", response)
        logger.debug("request status_code: %s", status_code)
        logger.debug("request => %s", url)
        logger.debug("content => %s", content)

        assert_equal(201, status_code)
        assert_true(content)
        assert_equal('http://0.0.0.0:8000/spanglish/word/', url)
        

        
        
    def test_get_token(self):
        """ expects to have return a token from the token api or the refresh """

        token = get_token()

        
        cached_token = cache.get('token').decode('ASCII')
        refreshed_token = cache.get('refresh').decode('ASCII')

        assert_equal(token, cached_token)

        
        
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
