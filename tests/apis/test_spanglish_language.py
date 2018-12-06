from fedal_cli.apis import spanglish
from fedal_cli.services.logger import get_logger
from fedal_cli.services.requester import make_request
from click.testing import CliRunner
from unittest import TestCase
import random

logger = get_logger(loggername='spanglish')

class TestSpanglishLanguage(TestCase):


    def setUp(self):
        """ runs before any test """

        logger.debug("setUp")
        language = 'test'
        params = {'language': language}
        api = ('spanglish', 'language')
        response = make_request(api=api, action='POST', **params)
        content = response.json()
        status_code = response.status_code
        logger.debug("response status_code: %s", status_code)
        logger.debug("response content: %s", content)
        if status_code == 201:
            self.language_id = content['id']
        else:
            self.language_id = 0

        logger.debug("language_id created: %d", self.language_id)




    def test_get_languages(self):
        """ expects to get all the languages and result output should be 0 """

        self.assertTrue(True)

    def tearDown(self):
        """ runs after every test """

        logger.debug("tearDown")
        args_params = (str(self.language_id),)
        api = ('spanglish', 'language')
        response = make_request(*args_params, api=api, action='DELETE', **{})
        status_code = response.status_code
        logger.debug("response status_code: %s", status_code)

