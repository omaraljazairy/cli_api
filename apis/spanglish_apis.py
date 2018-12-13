import click
from services.requester import make_request
from services.logger import get_logger
import sys
import importlib
#from spanglish import category

logger = get_logger(loggername='spanglish')

# a dict to show all the options and their api functions.
funcs = {
    1: ('Categories', 'apis.spanglish.category'),
    2: ('Languages', 'apis.spanglish.language'),
    3: ('Words', 'apis.spanglish.word'),
    4: ('Verbs', 'apis.spanglish.verb'),
    5: ('Sentences', 'apis.spanglish.sentence'),
}


@click.command()
@click.option('--function_id', default=1, type=click.IntRange(1, len(funcs)),  prompt='function option: ')
def run_function(function_id):
    """ based on the function number chosen by the user, it will execute the function """

    global funcs

    logger.debug("module chosen: {}".format(funcs[function_id][1]))
    module = importlib.import_module(funcs[function_id][1])

    for function_id, name in enumerate(module.funcs.values(), 1):
        print(function_id, name[0])


    module.run_function()
