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
api_url = conf.API['uri']


class TestRequester:


        
    def test_make_request_get_with_args(self):
        """ test the make request method with a get action and a tuple of args """

        args_params = ('5',)
        api = ('test', 'foo')
        response =  make_request(*args_params, action='GET', api=api, **{})
        status_code = response.status_code
        url = response.url
        headers = response.headers
        elapsed = response.elapsed
        request = response.request

        logger.debug("request => %s", response)
        logger.debug("request status_code: %s", status_code)
        logger.debug("request => %s", url)
        logger.debug("headers => %s", headers)
        logger.debug("elapsed => %s", elapsed)
        logger.debug("request => %s", request.method)
        
        assert_equal(request.method, 'GET')
        assert_equal(type(status_code), int)
        assert_true(headers['Content-Type'] == 'text/html')
        assert_equal(api_url + '/bar/5/', url)




    def test_make_request_get_with_no_args(self):
        """ test the make request method with a get action and no args. """

        api = ('test', 'foo')
        response =  make_request(action='GET', api=api, **{})
        headers = response.headers
        status_code = response.status_code
        url = response.url
        elapsed = response.elapsed
        request = response.request

        logger.debug("request => %s", response)
        logger.debug("request status_code: %s", status_code)
        logger.debug("request => %s", url)
        logger.debug("header => %s", headers)
        logger.debug("elapsed => %s", elapsed)
        logger.debug("request => %s", request.method)
        
        assert_equal(request.method, 'GET')
        assert_equal(type(status_code), int)
        assert_true(headers['Content-Type'] == 'text/html')
        assert_equal(api_url + '/bar/', url)



    def test_make_request_with_unknown_action(self):
        """ use an unknown action, expects a dic response with the error """

        api = ('test', 'foo')
        params = {
            'name': 'foo',
        }
        args_params = ('1',)

        response = make_request(*args_params, action='FOO', api=api, **params)
        logger.debug("response: %s", response)

        assert_true(response.get('ERROR', False))
        

    def test_make_request_put(self):
        """ expects to use the patch action and returns a status_code """

        api = ('test', 'foo')
        params = {
            'name': 'test',
        }
        args_params = ('2',)

        response = make_request(*args_params, action='PUT', api=api, **params)
        headers = response.headers
        status_code = response.status_code
        url = response.url
        elapsed = response.elapsed
        request = response.request

        logger.debug("request => %s", response)
        logger.debug("request status_code: %s", status_code)
        logger.debug("request => %s", url)
        logger.debug("headers => %s", headers)
        logger.debug("elapsed => %s", elapsed)
        logger.debug("request => %s", request.method)
        
        assert_equal(request.method, 'PATCH')
        assert_equal(type(status_code), int)
        assert_true(headers['Content-Type'] == 'text/html')
        assert_equal(api_url + '/bar/2/', url)


    def test_make_request_post(self):
        """ expects to use the post action and returns the POST action with a status_code """

        api = ('test', 'foo')
        params = {
            'name': 'test',
        }
        args_params = ('12',)

        response = make_request(*args_params, action='POST', api=api, **params)
        headers = response.headers
        status_code = response.status_code
        url = response.url
        elapsed = response.elapsed
        request = response.request

        logger.debug("request => %s", response)
        logger.debug("request status_code: %s", status_code)
        logger.debug("request => %s", url)
        logger.debug("headers => %s", headers)
        logger.debug("elapsed => %s", elapsed)
        logger.debug("request => %s", request.method)
        
        assert_equal(request.method, 'POST')
        assert_equal(type(status_code), int)
        assert_true(headers['Content-Type'] == 'text/html')
        assert_equal(api_url + '/bar/', url)



    def test_make_request_delete(self):
        """ expects to return a delete action and status_code """

        api = ('test', 'foo')
        params = {
            'name': 'test',
        }
        args_params = ('12',)

        response = make_request(*args_params, action='DELETE', api=api, **params)
        headers = response.headers
        status_code = response.status_code
        url = response.url
        elapsed = response.elapsed
        request = response.request

        logger.debug("request => %s", response)
        logger.debug("request status_code: %s", status_code)
        logger.debug("request => %s", url)
        logger.debug("headers => %s", headers)
        logger.debug("elapsed => %s", elapsed)
        logger.debug("request => %s", request.method)
        
        assert_equal(request.method, 'DELETE')
        assert_equal(type(status_code), int)
        assert_true(headers['Content-Type'] == 'text/html')
        assert_equal(api_url + '/bar/12/', url)
