import click
from services.requester import make_request
from services.logger import get_logger
import sys


logger = get_logger(loggername='spanglish')
api_name = 'spanglish'

# a dict to show all the options and their api functions.
funcs = {
    1: ('get all words', 'get_words'),
    2: ('get a word', 'get_word'),
    3: ('add a word', 'add_word'),
    4: ('update a word', 'update_word'),
    5: ('delete word', 'delete_word'),
}

@click.command()
@click.option('--function_id', default=1, type=click.IntRange(1, len(funcs)),  prompt='function option: ')
def run_function(function_id):
    """ based on the function number chosen by the user, it will execute the function """

    word = sys.modules[__name__] # to be used by the getattr

    global funcs
    funcName = funcs[function_id][1] # get the function name from the global dictionary funcs
    getattr(word, funcName)() #execute the chosen function



@click.command()
def get_words():
    """ return all words from the spanglish api """

    api = (api_name, 'words')
    response = make_request(api=api, action='get', **{})
    status_code = response.status_code
    content =  response.json() if status_code < 300 else response.text

    msg = str(status_code) + ' : ' + str(content)
    
    logger.debug("response from spanglish get words: {}".format(response))
    logger.debug("response statuscode from spanglish get words: {}".format(status_code))

    click.echo("response message: %s " % msg)
    

@click.command()
@click.option('--word_id', type=int, prompt='WordId')
def get_word(word_id):
    """ takes the word_id as an argument and returns the word details """

    args_params = (str(word_id),)
    api = (api_name, 'word')
    logger.debug("args_params received: {}".format(args_params))

    response = make_request(*args_params, api=api, action='get',  **{})
    status_code = response.status_code
    logger.debug("status_code = {}".format(status_code))
    
    content =  response.json() if status_code < 300 else response.text

    msg = str(status_code) + ' : ' + str(content)
    
    logger.debug("response from spanglish get word: {}".format(msg))

    click.echo("response message: %s " % msg)
    


@click.command()
@click.option('--word', type=str, prompt='None English Word ', help="the word that needs to be translated")
@click.option('--word_en', type=str, prompt='English translated word ', help="the translation of the word")
@click.option('--category', type=str, prompt='Category ', help="the category of the word")
@click.option('--language', type=str, prompt='language ', help="the word that needs to be translated")
def add_word(word, word_en, category, language):
    """ takes one parameter, name, and send it to the api. returns back the result from the api """

    params = {
        'word': word,
        'word_en': word_en,
        'category': category,
        'language': language,
    }

    api = ('spanglish', 'word')
    response = make_request(api=api, action='POST', **params)
    status_code = response.status_code
    content =  response.json() if status_code < 300 else response.text

    msg = str(status_code) + ' : ' + str(content)
    
    if status_code >= 300:

        click.echo("response error message: %s " % msg)
        raise click.Abort()
    

    logger.debug("response from spanglish add word: {}".format(msg))

    click.echo("response message: %s " % msg)


@click.command()
@click.option('--word_id', type=int, prompt='WordId')
@click.option('--word', type=str, default=None, required=False, prompt="Word")
@click.option('--word_en', type=str, default=None, required=False, prompt="Word_en")
@click.option('--category', type=str, default=None, required=False, prompt="Category")
@click.option('--language', type=str, default=None, required=False, prompt="Language")
def update_word(word_id, word=None, word_en=None, category=None, language=None):
    """ takes the word_id as arguments and returns the update result """

    args_params = (str(word_id),)
    params = {
        'word' : word,
        'word_en': word_en,
        'category': category,
        'language': language,
    }
    api = (api_name, 'word')
    logger.debug("args_params received: {}".format(args_params))

    response = make_request(*args_params, api=api, action='put',  **params)
    status_code = response.status_code
    content =  response.json() if status_code < 300 else response.text

    msg = str(status_code) + ' : ' + str(content)
    
    if status_code >= 300:

        click.echo("response error message: %s " % msg)
        raise click.Abort()
    

    logger.debug("response from spanglish update word: {}".format(msg))

    click.echo("response message: %s " % msg)


@click.command()
@click.option('--word_id', type=int, prompt='WordId')
def delete_word(word_id):
    """ takes the word_id as arguments and returns the deleted result """

    args_params = (str(word_id),)
    params = {}
    api = (api_name, 'word')

    logger.debug("args_params received: {}".format(args_params))

    response = make_request(*args_params, api=api, action='delete',  **params)
    status_code = response.status_code
    content = response.text

    msg = str(status_code) + ' : ' + str(content)
    
    if status_code >= 300:

        click.echo("response error message: %s " % msg)
        raise click.Abort()
    

    logger.debug("response from spanglish delete word: {}".format(msg))

    click.echo("response message: %s " % msg)
