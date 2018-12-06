import click
from services.requester import make_request
from services.logger import get_logger
import sys
import importlib
#from spanglish import category

logger = get_logger(loggername='spanglish')

# a dict to show all the options and their api functions.
funcs = {
    1: ('Categories', 'category'),
    2: ('Languages', 'language'),
    3: ('Words', 'word'),
    4: ('Verbs', 'verb'),
    5: ('Sentences', 'sentence'),
}


@click.command()
@click.option('--function_id', default=1, type=click.IntRange(1, len(funcs)),  prompt='function option: ')
def run_function(function_id):
    """ based on the function number chosen by the user, it will execute the function """

    #category = __import__('apis.spanglish.category')
    category = importlib.import_module('apis.spanglish.category')
    #sys.modules['spanglish.category'] # to be used by the getattr

    for function_id, name in enumerate(category.funcs.values(), 1):
        print(function_id, name[0])


    category.run_function()
