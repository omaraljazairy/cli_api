
import click
from services.requester import make_request
from services.logger import get_logger
import sys


logger = get_logger(loggername='spanglish')
api_name = 'spanglish'

# a dict to show all the options and their api functions.
funcs = {
    1: ('get all categories', 'get_categories'),
    2: ('get a category', 'get_category'),
    3: ('add a category', 'add_category'),
    4: ('update a category', 'update_category'),
    5: ('delete category', 'delete_category'),

    6: ('get all languages', 'get_languages'),
    7: ('get a language', 'get_language'),
    8: ('add a language', 'add_language'),
    9: ('update a language', 'update_language'),
    10: ('delete a language', 'delete_language'),

    11: ('get all words', 'get_words'),
    12: ('get a word', 'get_word'),
    13: ('add a word', 'add_word'),
    14: ('update a word', 'update_word'),
    15: ('delete word', 'delete_word'),

    16: ('get all verbs', 'get_verbs'),
    17: ('get a verb', 'get_verb'),
    18: ('add a verb', 'add_verb'),
    19: ('update a verb', 'update_verb'),
    20: ('delete verb', 'delete_verb'),


    21: ('get all sentences', 'get_sentences'),
    22: ('get a sentence', 'get_sentence'),
    23: ('add a sentence', 'add_sentence'),
    24: ('update a sentence', 'update_sentence'),
    25: ('delete sentence', 'delete_sentence'),

}

@click.command()
@click.option('--function_id', default=1, type=click.IntRange(1, len(funcs)),  prompt='function option: ')
def run_function(function_id):
    """ based on the function number chosen by the user, it will execute the function """

    spanglish = sys.modules[__name__] # to be used by the getattr

    global funcs
    funcName = funcs[function_id][1] # get the function name from the global dictionary funcs
    getattr(spanglish, funcName)() #execute the chosen function



@click.command()
def get_categories():
    """ return all categories from the spanglish api """

    api = (api_name, 'categories')
    #params = {'base': base, 'currency': currency, 'amount': amount}
    response = make_request(api=api, action='get', **{})
    status_code = response.status_code
    content =  response.json()

    logger.debug("response from spanglish categories: {}".format(response))
    logger.debug("response statuscode from spanglish categories: {}".format(status_code))
    logger.debug("response content from spanglish categories: {}".format(content))

    click.echo("response message: %s " % content)
    


@click.command()
@click.option('--category_id', type=int)
def get_category(category_id):
    """ takes the category_id as an argument and returns the category details """

    args_params = (str(category_id),)
    api = (api_name, 'category')
    logger.debug("args_params received: {}".format(args_params))

    response = make_request(*args_params, api=api, action='get',  **{})
    status_code = response.status_code
    content =  response.json()

    logger.debug("response from spanglish category: {}".format(response))
    logger.debug("response statuscode from spanglish category: {}".format(status_code))
    logger.debug("response content from spanglish category: {}".format(content))

    click.echo("response message: %s " % content)
    
    
