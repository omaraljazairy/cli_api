import click
from fedal_cli.services import make_request

API = {
        1:'add word',
        2:'add sentence',
        3:'add verb',
        4:'login',
    }  


@click.command()
@click.option('--word', prompt='original word: ', help="non english word")
@click.option('--word_en', prompt='english word: ', help="translated english word")
@click.option('--category', prompt='category [General|Animal|DAY|MONTH|PLACE|VERB|NUMBER|GREETING|COLOR|FOOD|RELATION]: ',
              help="category has to be one of the following: General|Animal|DAY|MONTH|PLACE|VERB|NUMBER|GREETING|COLOR|FOOD|RELATION")
@click.option('--language', default='ES', prompt='language [EN|ES]: ', help="language has to be one of the following: [EN|ES|NL]")
def add_word(word, word_en, category, language):
    """ expects a word parameter """

    print("word received: ", word)
    print("word_en received: ", word_en)
    if category not in ['General','Animal','DAY','MONTH','PLACE','VERB','NUMBER','GREETING','COLOR','FOOD','RELATION']:
        raise Exception('category has to be one of the following: General|Animal|DAY|MONTH|PLACE|VERB|NUMBER|GREETING|COLOR|FOOD|RELATION')
    elif language not in ['EN','ES','NL']:
        raise Exception('language has to be one of the following: EN, ES, NL')
    
    params = {
        'word': word,
        'word_en': word_en,
        'category': category
    }
    make_request(action='POST', api='spanglish_add_word', header={'toke':'aaaaa'}, **{'word':'bla'})
    
    return word
