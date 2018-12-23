from fedal_cli.apis.spanglish import verb
from fedal_cli.services.logger import get_logger
from fedal_cli.services.requester import make_request
from click.testing import CliRunner
from unittest import TestCase
import random

logger = get_logger(loggername='spanglish')


class TestSpanglishVerb(TestCase):




    def test_verb_dict(self):
        """ test if the verb module has a funcs dict with 5 objects """

        verb_funcs = getattr(verb, 'funcs')
        logger.debug("verb funcs are: {}".format(verb_funcs))

        self.assertEqual(type(verb_funcs), dict)
        self.assertTrue(len(verb_funcs), 5)



    def test_get_verbs(self):
        """ making a call to the get_verbs will exit successfully with code 0 """

        get_verbs = getattr(verb, 'get_verbs')
        runner = CliRunner()
        result = runner.invoke(get_verbs, [])

        logger.debug("result get_verbs output: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)


    def test_get_verb(self):
        """ pass the verb_id as an argument and gets the verb details. it will exit with code 0 """

        get_verb = getattr(verb, 'get_verb')

        runner = CliRunner()
        result = runner.invoke(get_verb, ['--verb_id', 2])

        logger.debug("result output: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)
        

    def test_add_verb(self):
        """ 
        provide all the parameters required to create a verb and expect the script
        to exit with code 0.
        """

        add_verb = getattr(verb, 'add_verb')

        word = 'tomar'
        yo = 'tomo'
        tu = 'tomas'
        el_ella_ud = 'toma'
        nosotros = 'tomamos'
        vosotros = 'tomais'
        ellos_ellas_uds = 'toman'
        tenses = 'SIMPLE_PRESENT'

        runner = CliRunner()
        result = runner.invoke(add_verb, ['--word', word, '--yo', yo, '--tu', tu, '--el_ella_ud', el_ella_ud, '--nosotros', nosotros,
                                          '--vosotros', vosotros, '--ellos_ellas_uds', ellos_ellas_uds, '--tenses', tenses ])

        logger.debug("result output: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)



    def test_update_verb(self):
        """ 
        provide all the parameters required to update a verb and expect the script
        to exit with code 0.
        """

        update_verb = getattr(verb, 'update_verb')

        verb_id = 2
        word = 'comer'
        yo = 'comero'
        tu = 'comerso'
        el_ella_ud = 'comeo'
        nosotros = 'comemoso'
        vosotros = 'commeiso'
        ellos_ellas_uds = 'comeno'
        tenses = 'SIMPLE_PRESENT'

        runner = CliRunner()
        result = runner.invoke(update_verb, ['--verb_id', verb_id, '--word', word, '--yo', yo, '--tu', tu, '--el_ella_ud', el_ella_ud, '--nosotros', nosotros,
                                          '--vosotros', vosotros, '--ellos_ellas_uds', ellos_ellas_uds, '--tenses', tenses ])

        logger.debug("result output: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)



    def test_delete_verb(self):
        """ try to delete the verb with id 1 and expect to exit with code 0 """

        delete_verb = getattr(verb, 'delete_verb')

        runner = CliRunner()
        result = runner.invoke(delete_verb, ['--verb_id', 1])

        logger.debug("delete result output: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)


    
