import click
from services.requester import make_request
from services.logger import get_logger
import sys


logger = get_logger(loggername='spanglish')
api_name = 'spanglish'

# a dict to show all the options and their api functions.
funcs = {
    1: ('get all verbs', 'get_verbs'),
    2: ('get a verb', 'get_verb'),
    3: ('add a verb', 'add_verb'),
    4: ('update a verb', 'update_verb'),
    5: ('delete verb', 'delete_verb'),
}

@click.command()
@click.option('--function_id', default=1, type=click.IntRange(1, len(funcs)),  prompt='function option: ')
def run_function(function_id):
    """ based on the function number chosen by the user, it will execute the function """

    verb = sys.modules[__name__] # to be used by the getattr

    global funcs
    funcName = funcs[function_id][1] # get the function name from the global dictionary funcs
    getattr(verb, funcName)() #execute the chosen function



@click.command()
def get_verbs():
    """ return all verbs from the spanglish api """

    api = (api_name, 'verbs')
    response = make_request(api=api, action='get', **{})
    status_code = response.status_code
    content =  response.json() if status_code < 300 else response.text

    msg = str(status_code) + ' : ' + str(content)
    
    logger.debug("response from spanglish get verbs: {}".format(response))
    logger.debug("response statuscode from spanglish get verbs: {}".format(status_code))

    click.echo("response message: %s " % msg)



@click.command()
@click.option('--verb_id', type=int, prompt='VerbId')
def get_verb(verb_id):
    """ takes the verb_id as an argument and returns the verb details """

    args_params = (str(verb_id),)
    api = (api_name, 'verb')
    logger.debug("args_params received: {}".format(args_params))

    response = make_request(*args_params, api=api, action='get',  **{})
    status_code = response.status_code
    logger.debug("status_code = {}".format(status_code))
    
    content =  response.json() if status_code < 300 else response.text

    msg = str(status_code) + ' : ' + str(content)
    
    logger.debug("response from spanglish get verb: {}".format(msg))

    click.echo("response message: %s " % msg)
    

@click.command()
@click.option('--word', type=str, prompt='The verb', help="the verb that from the word list with the category verb")
@click.option('--yo', type=str, prompt='Yo', default=None, required=False, help="The Yo Indicative")
@click.option('--tu', type=str, prompt='Tu ', help="The Tu Indicative")
@click.option('--el_ella_ud', type=str, default=None, required=False, prompt='el_ella_ud ', help="The el_ella_ud Indicative")
@click.option('--nosotros', type=str, default=None, required=False, prompt='nosotros ', help="The nosotros Indicative")
@click.option('--vosotros', type=str, default=None, required=False, prompt='vosotros ', help="The vosotros Indicative")
@click.option('--ellos_ellas_uds', type=str, default=None, required=False, prompt='ellos_ellas_uds ', help="The ellos_ellas_uds Indicative")
@click.option('--tenses', type=str, prompt='tenses', default='SIMPLE_PRESENT', help="The tenses of the verb")
def add_verb(word, tu, tenses, yo=None, el_ella_ud=None, nosotros=None, vosotros=None, ellos_ellas_uds=None ):
    """ takes three required parameters and five non required and send it to the api. returns back the result from the api """

    params = {
        'word': word,
        'yo': yo,
        'tu': tu,
        'el_ella_ud': el_ella_ud,
        'nosotros': nosotros,
        'vosotros': vosotros,
        'ellos_ellas_uds': ellos_ellas_uds,
        'tenses': tenses,
    }

    
    api = ('spanglish', 'verb')
    response = make_request(api=api, action='POST', **params)
    status_code = response.status_code
    content =  response.json() if status_code < 300 else response.text

    msg = str(status_code) + ' : ' + str(content)
    
    if status_code >= 300:

        click.echo("response error message: %s " % msg)
        raise click.Abort()
    

    logger.debug("response from spanglish add verb: {}".format(msg))

    click.echo("response message: %s " % msg)



@click.command()
@click.option('--verb_id', type=int, prompt='Verb Id', help="the verb id")
@click.option('--word', type=str, default=None, required=False, prompt='The verb', help="the verb that from the word list with the category verb")
@click.option('--yo', type=str, prompt='Yo', default=None, required=False, help="The Yo Indicative")
@click.option('--tu', type=str, prompt='Tu ', default=None, required=False, help="The Tu Indicative")
@click.option('--el_ella_ud', type=str, default=None, required=False, prompt='el_ella_ud ', help="The el_ella_ud Indicative")
@click.option('--nosotros', type=str, default=None, required=False, prompt='nosotros ', help="The nosotros Indicative")
@click.option('--vosotros', type=str, default=None, required=False, prompt='vosotros ', help="The vosotros Indicative")
@click.option('--ellos_ellas_uds', type=str, default=None, required=False, prompt='ellos_ellas_uds ', help="The ellos_ellas_uds Indicative")
@click.option('--tenses', type=str, prompt='tenses', required=False, default='SIMPLE_PRESENT', help="The tenses of the verb")
def update_verb(verb_id, word=None, tu=None, tenses=None, yo=None, el_ella_ud=None, nosotros=None, vosotros=None, ellos_ellas_uds=None ):
    """ takes three required parameters and five non required and send it to the api. returns back the result from the api """

    params = {
        'word': word,
        'yo': yo,
        'tu': tu,
        'el_ella_ud': el_ella_ud,
        'nosotros': nosotros,
        'vosotros': vosotros,
        'ellos_ellas_uds': ellos_ellas_uds,
        'tenses': tenses,
    }

    args_params = (str(verb_id),)
    api = (api_name, 'verb')
    logger.debug("args_params received: {}".format(args_params))

    response = make_request(*args_params, api=api, action='put',  **params)
    status_code = response.status_code
    content =  response.json() if status_code < 300 else response.text

    msg = str(status_code) + ' : ' + str(content)
    
    if status_code >= 300:

        click.echo("response error message: %s " % msg)
        raise click.Abort()
    

    logger.debug("response from spanglish update verb: {}".format(msg))

    click.echo("response message: %s " % msg)




@click.command()
@click.option('--verb_id', type=int, prompt='VerbId')
def delete_verb(verb_id):
    """ takes the verb_id as arguments and returns the deleted result """

    args_params = (str(verb_id),)
    params = {}
    api = (api_name, 'verb')

    logger.debug("args_params received: {}".format(args_params))

    response = make_request(*args_params, api=api, action='delete',  **params)
    status_code = response.status_code
    content = response.text

    msg = str(status_code) + ' : ' + str(content)
    
    if status_code >= 300:

        click.echo("response error message: %s " % msg)
        raise click.Abort()
    

    logger.debug("response from spanglish delete verb: {}".format(msg))

    click.echo("response message: %s " % msg)
