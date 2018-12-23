import click
from services.requester import make_request
from services.logger import get_logger
import sys


logger = get_logger(loggername='spanglish')
api_name = 'spanglish'

# a dict to show all the options and their api functions.
funcs = {
    1: ('get all sentences', 'get_sentences'),
    2: ('get a sentence', 'get_sentence'),
    3: ('add a sentence', 'add_sentence'),
    4: ('update a sentence', 'update_sentence'),
    5: ('delete sentence', 'delete_sentence'),
}

@click.command()
@click.option('--function_id', default=1, type=click.IntRange(1, len(funcs)),  prompt='function option: ')
def run_function(function_id):
    """ based on the function number chosen by the user, it will execute the function """

    sentence = sys.modules[__name__] # to be used by the getattr

    global funcs
    funcName = funcs[function_id][1] # get the function name from the global dictionary funcs
    getattr(sentence, funcName)() #execute the chosen function



@click.command()
def get_sentences():
    """ return all sentences from the spanglish api """

    api = (api_name, 'sentences')
    response = make_request(api=api, action='get', **{})
    status_code = response.status_code
    content =  response.json() if status_code < 300 else response.text

    msg = str(status_code) + ' : ' + str(content)
    
    logger.debug("response from spanglish get sentences: {}".format(response))
    logger.debug("response statuscode from spanglish get sentences: {}".format(status_code))

    click.echo("response message: %s " % msg)



@click.command()
@click.option('--sentence_id', type=int, prompt='SentenceId')
def get_sentence(sentence_id):
    """ takes the sentence_id as an argument and returns the sentence details """

    args_params = (str(sentence_id),)
    api = (api_name, 'sentence')
    logger.debug("args_params received: {}".format(args_params))

    response = make_request(*args_params, api=api, action='get',  **{})
    status_code = response.status_code
    logger.debug("status_code = {}".format(status_code))
    
    content =  response.json() if status_code < 300 else response.text

    msg = str(status_code) + ' : ' + str(content)
    
    logger.debug("response from spanglish get sentence: {}".format(msg))

    click.echo("response message: %s " % msg)


@click.command()
@click.option('--sentence', type=str, prompt='None English Sentence ', help="the sentence that needs to be translated")
@click.option('--sentence_en', type=str, prompt='English translated sentence ', help="the translation of the sentence")
@click.option('--word', type=str, prompt='Word reference', help="the word where the sentence reference to")
@click.option('--category', type=str, prompt='Category ', help="the category of the sentence")
@click.option('--language', type=str, prompt='Language ', help="the sentence that needs to be translated")
def add_sentence(sentence, sentence_en, word, category, language):
    """ takes the following parameters: sentence, sentence_en, word, category, and language and send it to the api. returns back the result from the api """

    params = {
        'sentence': sentence,
        'sentence_en': sentence_en,
        'word': word,
        'category': category,
        'language': language,
    }

    
    api = ('spanglish', 'sentence')
    response = make_request(api=api, action='POST', **params)
    status_code = response.status_code
    content =  response.json() if status_code < 300 else response.text

    msg = str(status_code) + ' : ' + str(content)
    
    if status_code >= 300:

        click.echo("response error message: %s " % msg)
        raise click.Abort()
    

    logger.debug("response from spanglish add sentence: {}".format(msg))

    click.echo("response message: %s " % msg)


@click.command()
@click.option('--sentence_id', type=int, prompt='SentenceId')
@click.option('--sentence', type=str, default=None, required=False, prompt="Sentence")
@click.option('--sentence_en', type=str, default=None, required=False, prompt="Sentence_EN")
@click.option('--word', type=str, default=None, required=False)
@click.option('--category', type=str, default=None, required=False)
@click.option('--language', type=str, default=None, required=False)
def update_sentence(sentence_id, sentence=None, sentence_en=None, word=None, category=None, language=None):
    """ takes the sentence_id as arguments and returns the update result """

    args_params = (str(sentence_id),)
    params = {
        'sentence' : sentence,
        'sentence_en': sentence_en,
        'word': word,
        'category': category,
        'language': language,
    }
    api = (api_name, 'sentence')
    logger.debug("args_params received: {}".format(args_params))

    response = make_request(*args_params, api=api, action='put',  **params)
    status_code = response.status_code
    content =  response.json() if status_code < 300 else response.text

    msg = str(status_code) + ' : ' + str(content)
    
    if status_code >= 300:

        click.echo("response error message: %s " % msg)
        raise click.Abort()
    

    logger.debug("response from spanglish update sentence: {}".format(msg))

    click.echo("response message: %s " % msg)


@click.command()
@click.option('--sentence_id', type=int, prompt='SentenceId')
def delete_sentence(sentence_id):
    """ takes the sentence_id as arguments and returns the deleted result """

    args_params = (str(sentence_id),)
    params = {}
    api = (api_name, 'sentence')

    logger.debug("args_params received: {}".format(args_params))

    response = make_request(*args_params, api=api, action='delete',  **params)
    status_code = response.status_code
    content = response.text

    msg = str(status_code) + ' : ' + str(content)
    
    if status_code >= 300:

        click.echo("response error message: %s " % msg)
        raise click.Abort()
    

    logger.debug("response from spanglish delete sentence: {}".format(msg))

    click.echo("response message: %s " % msg)
