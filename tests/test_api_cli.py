from fedal_cli.configs import settings as conf
from fedal_cli.services.requester import make_request
from fedal_cli.services.tokens import get_token, get_token_cached_times_diff
import click
from click.testing import CliRunner
from nose.tools import assert_true, assert_equal
from fedal_cli.services.logger import get_logger
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
        

        
        
