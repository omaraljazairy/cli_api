import click
from services.requester import make_request
from services.logger import get_logger
import sys


logger = get_logger(loggername='spanglish')
api_name = 'spanglish'

# a dict to show all the options and their api functions.
funcs = {
    1: ('get all languages', 'get_languages'),
    2: ('get a language', 'get_language'),
    3: ('add a language', 'add_language'),
    4: ('update a language', 'update_language'),
    5: ('delete a language', 'delete_language'),
}

@click.command()
@click.option('--function_id', default=1, type=click.IntRange(1, len(funcs)),  prompt='function option: ')
def run_function(function_id):
    """ based on the function number chosen by the user, it will execute the function """

    language = sys.modules[__name__] # to be used by the getattr

    global funcs
    funcName = funcs[function_id][1] # get the function name from the global dictionary funcs
    getattr(language, funcName)() #execute the chosen function



@click.command()
def get_languages():
    """ return all languages from the spanglish api """

    api = (api_name, 'languages')

    response = make_request(api=api, action='get', **{})
    status_code = response.status_code
    content =  response.text

    msg = str(status_code) + ' : ' + content
    
    logger.debug("response from spanglish languages: {}".format(response))
    logger.debug("response statuscode from spanglish languages: {}".format(status_code))

    click.echo("response message: %s " % msg)


@click.command()
@click.option('--language_id', type=int, prompt="language id", help="the language id that needs to be fetched")
def get_language(language_id):
    """ get info about one language by providing the language_id """

    api = (api_name, 'language')
    args_params = (str(language_id), )
    
    response = make_request(*args_params, api=api, action='get',  **{})
    status_code = response.status_code
    content =  response.text

    msg = str(status_code) + ' : ' + content
    
    if status_code >= 300:

        click.echo("response error message: %s " % msg)
        raise click.Abort()
    

    logger.debug("response from spanglish get_language: {}".format(response))
    logger.debug("response msg from spanglish get_language: {}".format(msg))

    click.echo("response message: %s " % msg)
    

@click.command()
@click.option('--iso1', type=str, prompt='iso1', help="the iso1 of the language")
def add_language(iso1):
    """ takes one parameter, iso1, and send it to the api. returns back the result from the api """

    params = {'iso1': iso1}
    api = (api_name, 'language')
    
    response = make_request(api=api, action='post',  **params)
    status_code = response.status_code
    content =  response.text

    msg = str(status_code) + ' : ' + content
    
    logger.debug("response from spanglish add language: {}".format(response))
    logger.debug("response statuscode from spanglish add language: {}".format(status_code))

    click.echo("response message: %s " % msg)



@click.command()
@click.option('--language_id', type=int, prompt="language id", help="the language id that needs to be deleteted")
def delete_language(language_id):
    """ delete the language by providing the language_id """

    api = (api_name, 'language')
    args_params = (str(language_id), )
    
    response = make_request(*args_params, api=api, action='delete',  **{})
    status_code = response.status_code
    content =  response.text

    msg = str(status_code) + ' : ' + content
    
    logger.debug("response from spanglish delete_language: {}".format(response))
    logger.debug("response msg from spanglish delete_language: {}".format(msg))

    click.echo("response message: %s " % msg)
