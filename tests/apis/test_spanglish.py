from fedal_cli.apis import spanglish
from fedal_cli.services.logger import get_logger
from fedal_cli.services.requester import make_request
from click.testing import CliRunner
from unittest import TestCase
import random

logger = get_logger(loggername='spanglish')

class TestCurrency(TestCase):

    #@classmethod
    #def string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    #    return ''.join(random.choice(chars) for _ in range(size))


    def setUp(self):
        """ runs before any test """

        logger.debug("setUp")
        random_number = random.randint(1,101)
        logger.debug("random_number generated: %s", random_number)
        category_name = 'test'.__add__(str(random_number))
        params = {'name': category_name}
        api = ('spanglish', 'category')
        response = make_request(api=api, action='POST', **params)
        content = response.json()
        status_code = response.status_code
        logger.debug("response status_code: %s", status_code)
        logger.debug("response content: %s", content)
        if status_code == 201:
            self.category_id = content['id']
        else:
            self.category_id = 0

        logger.debug("category_id created: %d", self.category_id)
        

        
    def test_funcs_dict_tuple(self):
        """ expects the attribute funcs to be a dict with tuples """

        funcs = getattr(spanglish, 'funcs')
        values = {type(v) for v in funcs.values()}
        value_type = list(values)[0]
        
        logger.debug("funcs: {}".format(funcs))
        logger.debug("values: {}".format(values))
        logger.debug("type values: {}".format(value_type))

        self.assertTrue(type(funcs) == dict) # expect type to be a dict
        self.assertEqual(len(values), 1) # expects one type only
        self.assertEqual(value_type, tuple ) # expect the type to be tuple
        self.assertTrue(len(funcs) == 25)


    def test_get_categories(self):
        """ provide no params and get a list of all categories """

        get_categories = getattr(spanglish, 'get_categories')
        runner = CliRunner()
        result = runner.invoke(get_categories, [])

        logger.debug("result.output: {}".format(result.output))
        
        self.assertTrue(result.exit_code == 0)


    def test_get_category(self):
        """ provide a parameter in the request and expect exit_code 0 """

        get_category = getattr(spanglish, 'get_category')
        runner = CliRunner()
        result = runner.invoke(get_category, ['--category_id', 3])

        logger.debug("result.output: {}".format(result.output))
        
        self.assertTrue(result.exit_code == 0)


        
    def tearDown(self):
        """ runs after every test """

        logger.debug("tearDown")
        args_params = (str(self.category_id),)
        api = ('spanglish', 'category')
        response = make_request(*args_params, api=api, action='DELETE', **{})
        status_code = response.status_code
        logger.debug("response status_code: %s", status_code)

