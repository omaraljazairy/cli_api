import click
from services.logger import get_logger
from services.requester import make_request
import sys

logger = get_logger(loggername='currency')
api_name = 'currency'

funcs = {
    1: ('currency code', 'get_code'),
    2: ('currency amount converter', 'convert_currency'),
    3: ('currency current rate', 'get_rate'),
    4: ('currency rate for all currencies', 'get_all_rates'),
}

@click.command()
@click.option('--function_id', default=1, type=click.IntRange(1, len(funcs)),  prompt='function option: ')
def run_function(function_id):
    """ based on the function number chosen by the user, it will execute the function """

    currency = sys.modules[__name__] # to be used by the getattr

    global funcs
    funcName = funcs[function_id][1] # get the function name from the global dictionary funcs
    getattr(currency, funcName)() #execute the chosen function
    


@click.command()
@click.option('--currency', type=click.Choice(['EUR', 'USD', 'CAD', 'GBP']), default='EUR', prompt='currency code ')
def get_code(currency):
    """ 
    expects one parameter, currency. it will give back the symbol of the curreny. default is EUR. example ?currency=USD 
    """

    api = (api_name, 'code')
    params = {'currency' : currency}
    response = make_request(action='get', api=api, **params)
    status_code = response.status_code
    content =  response.json()
    logger.debug("response currency {}".format(content))
    logger.debug("response currency statuscode {}".format(status_code))
    click.echo("currency code is %s" % content, nl=True)
    

@click.command()
@click.option('--base', default='EUR', prompt='base currency ')
@click.option('--currency', prompt='currency to convert to ')
@click.option('--amount', prompt='amount to be converted ')
def convert_currency(base, currency, amount):
    """
    exptect three parameters, base, currency and amount. gives back the rate. default is 1 EUR to USD. 
    example : base=USD&currency=GBP&amount=5000
    """

    api = (api_name, 'convert')
    params = {
        'base': base,
        'currency': currency,
        'amount': amount,
    }

    logger.debug("params: {}".format(params))

    response = make_request(action='get', api=api, **params)
    status_code = response.status_code
    content =  response.json()
    logger.debug("response currency converter statuscode {}".format(status_code))
    logger.debug("the amount {} {} in {} is {}".format(amount, base, currency, content))

    click.echo("the amount %s %s in %s is %s" % (amount, base, currency, content), nl=True)




@click.command()
@click.option('--base', default='EUR', prompt='base currency ')
@click.option('--currency', prompt='currency to rate for ')
def get_rate(base, currency):
    """ takes two parameters, the base currency and the currency and returns the current rate only """


    api = (api_name, 'rate')
    params = {
        'base': base,
        'currency': currency,
    }

    logger.debug("params: {}".format(params))

    response = make_request(action='get', api=api, **params)
    status_code = response.status_code
    content =  response.json()

    logger.debug("currency rate converter statuscode {}".format(status_code))
    logger.debug("today's currency for the {} in {} is {}".format(base, currency, content))

    click.echo("today's currency for the %s in %s is %s" % (base, currency, content), nl=True)



@click.command()
@click.option('--base', default='EUR', prompt='base currency ')
def get_all_rates(base):
    """ take one parameter and returns all the current rate for all currencies """


    api = (api_name, 'rates')
    params = {
        'base': base,
    }

    logger.debug("params: {}".format(params))

    response = make_request(action='get', api=api, **params)
    status_code = response.status_code
    content =  response.json()

    logger.debug("currency rates statuscode {}".format(status_code))
    logger.debug("today's currencies for the {} are {}".format(base, content))

    click.echo("today's currencies for the %s are %s" % (base, content), nl=True)

