from fedal_cli.apis.currency import get_code, convert_currency, get_rate, get_all_rates
from fedal_cli.services.logger import get_logger
from click.testing import CliRunner
from unittest import TestCase
logger = get_logger(loggername='currency')

class TestCurrency(TestCase):


    def test_get_code_ok(self):
        """ provide param currency and gets back the symbol of the currency """

        runner = CliRunner()
        result = runner.invoke(get_code, ['--currency', 'EUR'])
        logger.debug("result.output: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)
        self.assertEqual('currency code is €', result.output)



    def test_convert_currency(self):
        """ pass three paramters and expects a string returned with the value as a result """

        runner = CliRunner()
        result = runner.invoke(convert_currency, ['--base', 'EUR', '--currency', 'USD', '--amount', '1000'])
        logger.debug("result.output: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)



    def test_get_rate(self):
        """ pass two params and get back the result """

        runner = CliRunner()
        result = runner.invoke(get_rate, ['--base', 'EUR', '--currency', 'USD'])
        logger.debug("result.output: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)


    def test_get_all_rates(self):
        """ pass one param and get back all the currencies """

        runner = CliRunner()
        result = runner.invoke(get_all_rates, ['--base', 'EUR'])
        logger.debug("result.output: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)
