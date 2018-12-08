from fedal_cli.apis.spanglish import language
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
        language = 'NL'
        params = {'iso1': language}
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



    def test_language_dict(self):
        """ test if the language module has a funcs dict with 5 objects """

        language_funcs = getattr(language, 'funcs')
        logger.debug("language funcs are: {}".format(language_funcs))

        self.assertEqual(type(language_funcs), dict)
        self.assertTrue(len(language_funcs), 5)
        

    def test_get_languages(self):
        """ expects to get all the languages and result output should be 0 """

        get_languages = getattr(language, 'get_languages')
        runner = CliRunner()
        result = runner.invoke(get_languages, [])

        logger.debug("result.output get_languages: {}".format(result.output))
        
        self.assertTrue(result.exit_code == 0)


    def test_get_language(self):
        """ test expects to get back the language and exits with code 0 """

        get_language = getattr(language, 'get_language')
        
        runner = CliRunner()
        result = runner.invoke(get_language, ['--language_id', self.language_id ])

        logger.debug("result.output get_languages: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)


    def test_get_language_error(self):
        """ test expects the script to be aborted because of an unexistance language """

        get_language = getattr(language, 'get_language')
        
        runner = CliRunner()
        result = runner.invoke(get_language, ['--language_id', '10000' ])

        logger.debug("result.output get_languages: {}".format(result.output))

        self.assertTrue(result.exit_code == 1)


    def test_add_language(self):
        """ expect it to not add a language but still exit with code 0 """

        add_language = getattr(language, 'add_language')

        runner = CliRunner()
        result = runner.invoke(add_language, ['--iso1', 'AR' ])

        logger.debug("result.output add_languages: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)


    def test_delete_language(self):
        """ expect it to not delete a language and still exit with code 0 """

        delete_language = getattr(language, 'delete_language')

        runner = CliRunner()
        result = runner.invoke(delete_language, ['--language_id', 1000 ])

        logger.debug("result.output delete_languages: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)
        
    
    
        
    def tearDown(self):
        """ runs after every test """

        logger.debug("tearDown")
        args_params = (str(self.language_id),)
        api = ('spanglish', 'language')
        response = make_request(*args_params, api=api, action='DELETE', **{})
        status_code = response.status_code
        logger.debug("response status_code: %s", status_code)

