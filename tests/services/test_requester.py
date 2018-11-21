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



class TestRequester:


    def setUp(self):

        logger.debug("setUp")

        api = ('spanglish', 'word')
        params = {
            'word': 'mytesto12',
            'word_en': 'mytest12',
            'category': 'General',
            'language': 'ES',
        }
        response = make_request(action='POST', api=api, **params)
        content = response.json()
        logger.debug("word created: %s", content)
        self.id = content['id']
        logger.debug("created word id = %s", self.id)

    
    def test_make_get_with_args_request(self):
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

        logger.debug("created word id = %s", self.id)
        
        assert_equal(200, status_code)
        assert_true(content)
        assert_equal('http://0.0.0.0:8000/spanglish/word/5/', url)



    def test_make_get_with_no_args_request(self):
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
        logger.debug("created word id = %s", self.id)
        
        assert_equal(200, status_code)
        assert_true(content)
        assert_equal('http://0.0.0.0:8000/spanglish/words/', url)



    def test_make_request_with_unknown_action(self):
        """ use an unknown action, expects a dic response with the error """

        api = ('spanglish', 'word')
        params = {
            'word': 'foo',
            'word_en': 'bar',
        }
        args_params = ('10',)

        response = make_request(*args_params, action='FOO', api=api, **params)
        logger.debug("response: %s", response)

        assert_true(response.get('ERROR', False))
        

    def test_make_request_put(self):
        """ expects to update a word and receive status_code 200 """

        api = ('spanglish', 'word')
        params = {
            'word': 'testa12',
            'word_en': 'testa12',
        }
        args_params = (str(self.id),)

        response = make_request(*args_params, action='PUT', api=api, **params)
        content = response.json()
        status_code = response.status_code
        url = response.url

        logger.debug("request => %s", response)
        logger.debug("request status_code: %s", status_code)
        logger.debug("request => %s", url)
        logger.debug("content => %s", content)
        logger.debug("created word id = %s", self.id)
        
        assert_equal(200, status_code)
        assert_true(content)
        assert_equal('http://0.0.0.0:8000/spanglish/word/' + str(self.id) + '/', url)



    def test_make_request_delete(self):
        """ expects to delete a word and receive status_code 200 """

        api = ('spanglish', 'word')
        params = {}
        args_params = (str(self.id),)

        response = make_request(*args_params, action='DELETE', api=api)
        #content = response.json()
        status_code = response.status_code
        #url = response.url

        logger.debug("request => %s", response)
        logger.debug("request status_code: %s", status_code)
        #logger.debug("request => %s", url)
        #logger.debug("content => %s", content)

        assert_equal(204, status_code)
        #assert_true(content)
        #assert_equal('http://0.0.0.0:8000/spanglish/word/10/', url)


    def tearDown(self):

        logger.debug("tearDown")
        logger.debug("created word id = %s", self.id)
        #logger.debug("created word test_id to be deleted = %s", self.test_id)
        api = ('spanglish', 'word')
        params = {}
        args_params = (str(self.id),)
        response = make_request(*args_params, action='DELETE', api=api, **params)
        status_code = response.status_code

        logger.debug("request => %s", response)

        #args_params = (str(self.test_id),)
        #response = make_request(*args_params, action='DELETE', api=api, **params)
        #status_code = response.status_code


        #logger.debug("request => %s", response)
