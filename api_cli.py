import click
from apis.currency import get_code

apis = {
    1: 'currency',
    2: 'spanglish',
    }

def main():
    """ 
    prints a list of the apis and their option number to be selected. 
    waits for a user input to be one of the options number. 
    
    """

    for k,v in apis.items():
        click.echo("%s - %s" % (k,v))

    run_api()    


@click.command()
@click.option('--api', default=1, prompt='api option: ')
def run_api(api):
    """ based on the option number chosen by the user, it will execute the api function """
    
    click.echo("api option : %s is chosen" % apis.get(int(api), False))

    if api == 1:
        get_code()
        
    elif api == 2:
        args = {'word':'hello', 'hola amigo': 'hello my friend'}
        print("api 2 selected")
    else:
        print("unkknown selection")
    



if __name__ == "__main__":
    main()

