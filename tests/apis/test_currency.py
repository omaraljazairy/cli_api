from fedal_cli.apis import currency
from fedal_cli.services.logger import get_logger
from click.testing import CliRunner
from unittest import TestCase
logger = get_logger(loggername='currency')

class TestCurrency(TestCase):


    def test_get_code_ok(self):
        """ provide param currency and gets back the symbol of the currency """

        gc = getattr(currency, 'get_code')
        runner = CliRunner()
        result = runner.invoke(gc, ['--currency', 'EUR'])
        logger.debug("result.output: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)
        self.assertEqual('currency code is €', result.output)



    def test_convert_currency(self):
        """ pass three paramters and expects a string returned with the value as a result """

        cc = getattr(currency, 'convert_currency')
        runner = CliRunner()
        result = runner.invoke(cc, ['--base', 'EUR', '--currency', 'USD', '--amount', '1000'])
        logger.debug("result.output: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)



    def test_get_rate(self):
        """ pass two params and get back the result """

        gr = getattr(currency, 'get_rate')
        runner = CliRunner()
        result = runner.invoke(gr, ['--base', 'EUR', '--currency', 'USD'])
        logger.debug("result.output: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)


    def test_get_all_rates(self):
        """ pass one param and get back all the currencies """

        gar = getattr(currency, 'get_all_rates')
        runner = CliRunner()
        result = runner.invoke(gar, ['--base', 'EUR'])
        logger.debug("result.output: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)


    def test_run_function(self):
        """ provide one of the four options and there should not be an exit code because a click method will be invoked """

        gar = getattr(currency, 'run_function')
        runner = CliRunner()
        result = runner.invoke(gar, ['--function_id', 1], catch_exceptions=False)
        logger.debug("result.output: {}".format(result.output))
        logger.debug("result.exit_code: {}".format(result.exit_code))
        logger.debug("result: {}".format(result))

        self.assertFalse(result.exit_code == 0)


    def test_funcs_dict_tuple(self):
        """ expects the attribute funcs to be a dict with tuples """

        funcs = getattr(currency, 'funcs')
        values = {type(v) for v in funcs.values()}
        value_type = list(values)[0]
        
        logger.debug("funcs: {}".format(funcs))
        logger.debug("values: {}".format(values))
        logger.debug("type values: {}".format(value_type))

        self.assertTrue(type(funcs) == dict)
        self.assertEqual(len(values), 1)
        self.assertEqual(value_type, tuple )
