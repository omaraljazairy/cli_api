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
        self.random_number = random.randint(1,101)
        logger.debug("random_number generated: %s", self.random_number)
        category_name = 'test'.__add__(str(self.random_number))
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
        result = runner.invoke(get_category, ['--category_id', self.category_id])

        logger.debug("result.output: {}".format(result.output))
        
        self.assertTrue(result.exit_code == 0)



    def test_get_category_error(self):
        """ provide a category_id that doesn't exist and expect an error """

        get_category = getattr(spanglish, 'get_category')

        random_number = self.random_number + 999
                
        runner = CliRunner()
        result = runner.invoke(get_category, ['--category_id', random_number])

        logger.debug("result.output: {}".format(result.output))
        logger.debug("result.exit_code: {}".format(result.exit_code))
        
        self.assertTrue(result.exit_code == 1)


    def test_add_category(self):
        """ provide a name for the category and expect the function to exit with 0 """

        add_category = getattr(spanglish, 'add_category')

        random_number = self.random_number + 10000
        category_name = 'test'.__add__(str(random_number))

        logger.debug("category_name: {}".format(category_name))

        runner = CliRunner()
        result = runner.invoke(add_category, ['--name', category_name ])
        logger.debug("result.output: {}".format(result.output))
        
        self.assertTrue(result.exit_code == 0)


    def test_add_category_error(self):
        """ provide a duplicate name for the category and expect the function to exit with error """

        add_category = getattr(spanglish, 'add_category')

        category_name = 'test'.__add__(str(self.random_number))

        logger.debug("category_name: {}".format(category_name))

        runner = CliRunner()
        result = runner.invoke(add_category, ['--name', category_name ])
        logger.debug("result.output: {}".format(result.output))
        
        self.assertTrue(result.exit_code == 1)



    def test_update_category(self):
        """ expects to update a category using the self.category_id and a random name from the setUp function """

        update_category = getattr(spanglish, 'update_category')

        random_number = self.random_number + 1000
        category_name = 'test'.__add__(str(random_number))

        logger.debug("category_name: {}".format(category_name))

        runner = CliRunner()
        result = runner.invoke(update_category, ['--category_id', self.category_id, '--category_name', category_name])

        logger.debug("result.output from update_category: {}".format(result.output))
        
        self.assertTrue(result.exit_code == 0)


    def test_update_category_error(self):
        """ expects to update a non existing category_id and return an error """

        update_category = getattr(spanglish, 'update_category')

        random_number = self.random_number + 1000
        category_name = 'test'.__add__(str(random_number))

        logger.debug("category_name: {}".format(category_name))

        runner = CliRunner()
        result = runner.invoke(update_category, ['--category_id', random_number, '--category_name', category_name])

        logger.debug("result.output from update_category: {}".format(result.output))
        
        self.assertTrue(result.exit_code == 1)



    def test_delete_category(self):
        """ provide the category_id as parameter in the request and expect exit_code 0 """

        delete_category = getattr(spanglish, 'delete_category')
        runner = CliRunner()
        result = runner.invoke(delete_category, ['--category_id', self.category_id])

        logger.debug("result.output: {}".format(result.output))
        
        self.assertTrue(result.exit_code == 0)


    def test_delete_category_error(self):
        """ provide a non existing category_id as parameter and expect exit_code 1 """

        delete_category = getattr(spanglish, 'delete_category')
        runner = CliRunner()
        result = runner.invoke(delete_category, ['--category_id', 0])

        logger.debug("result.output: {}".format(result.output))
        
        self.assertTrue(result.exit_code == 1)


        
    def tearDown(self):
        """ runs after every test """

        logger.debug("tearDown")
        args_params = (str(self.category_id),)
        api = ('spanglish', 'category')
        response = make_request(*args_params, api=api, action='DELETE', **{})
        status_code = response.status_code
        logger.debug("response status_code: %s", status_code)

