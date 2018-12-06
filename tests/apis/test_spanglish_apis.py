from fedal_cli.apis import spanglish_apis
from fedal_cli.services.logger import get_logger
from click.testing import CliRunner
from unittest import TestCase

logger = get_logger(loggername='spanglish')

class TestSpanglishCategory(TestCase):

            
    def test_funcs_dict_tuple(self):
        """ expects the attribute funcs to be a dict with tuples """

        funcs = getattr(spanglish_apis, 'funcs')
        values = {type(v) for v in funcs.values()}
        value_type = list(values)[0]
        
        logger.debug("funcs: {}".format(funcs))
        logger.debug("values: {}".format(values))
        logger.debug("type values: {}".format(value_type))

        self.assertTrue(type(funcs) == dict) # expect type to be a dict
        self.assertEqual(len(values), 1) # expects one type only
        self.assertEqual(value_type, tuple ) # expect the type to be tuple
        self.assertTrue(len(funcs) == 5)
    


    def test_run_function(self):
        """ expect it to continue without an error """

        rf = getattr(spanglish_apis, 'run_function')
        runner = CliRunner()
        result = runner.invoke(rf, ['--function_id', 1])

        logger.debug("result.output run_functions: {}".format(result.output))
        logger.debug("result.exitcode run_functions: {}".format(result.exit_code))

        self.assertTrue(result.exit_code == 2)
