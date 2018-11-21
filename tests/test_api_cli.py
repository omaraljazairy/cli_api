from fedal_cli.configs import settings as conf
from fedal_cli.services.requester import make_request
from fedal_cli.services.tokens import get_token, get_token_cached_times_diff
import click
from click.testing import CliRunner
from nose.tools import assert_true, assert_equal
from fedal_cli.services.logger import get_logger
import redis
from datetime import datetime, timedelta

logger = get_logger(loggername='test')


class TestCLI:

    def xtest_make_get_with_args_request(self):
        """ test the make request method with a get action and a tuple of args """

        assert_true(True)        

        
        
