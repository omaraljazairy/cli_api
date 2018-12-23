from fedal_cli.apis.spanglish import sentence
from fedal_cli.services.logger import get_logger
from fedal_cli.services.requester import make_request
from click.testing import CliRunner
from unittest import TestCase
import random

logger = get_logger(loggername='spanglish')


class TestSpanglishSentence(TestCase):


    def test_sentence_dict(self):
        """ test if the sentence module has a funcs dict with 5 objects """

        sentence_funcs = getattr(sentence, 'funcs')
        logger.debug("sentence funcs are: {}".format(sentence_funcs))

        self.assertEqual(type(sentence_funcs), dict)
        self.assertTrue(len(sentence_funcs), 5)


    def test_get_sentences(self):
        """ making a call to the get_sentences will exit successfully with code 0 """

        get_sentences = getattr(sentence, 'get_sentences')
        runner = CliRunner()
        result = runner.invoke(get_sentences, [])

        logger.debug("result output: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)



    def test_get_sentence(self):
        """ pass the sentence_id as an argument and gets the sentence details. it will exit with code 0 """

        get_sentence = getattr(sentence, 'get_sentence')

        runner = CliRunner()
        result = runner.invoke(get_sentence, ['--sentence_id', 2])

        logger.debug("result output: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)


    def test_add_sentence(self):
        """ 
        provide all the parameters required to create a sentence and expect the script
        to exit with code 0.
        """

        add_sentence = getattr(sentence, 'add_sentence')

        sentence_es = 'Vamos Rafa'
        sentence_en = 'Come on Rafa'
        category = 'Entertainment'
        language = 'EN'
        word = 'hablar'

        runner = CliRunner()
        result = runner.invoke(add_sentence, ['--sentence', sentence_es, '--sentence_en', sentence_en, '--category', category, '--language', language, '--word', word])

        logger.debug("result output: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)



    def test_update_sentence(self):
        """ try to update the sentence_en and expect to exit with code 0 """

        update_sentence = getattr(sentence, 'update_sentence')

        runner = CliRunner()
        result = runner.invoke(update_sentence, ['--sentence_id', 1, '--sentence', 'blbl', '--sentence_en', 'bloo', '--word', 'Hola'])

        logger.debug("update result output: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)



    def test_delete_sentence(self):
        """ try to delete the sentence with id 1 and expect to exit with code 0 """

        delete_sentence = getattr(sentence, 'delete_sentence')

        runner = CliRunner()
        result = runner.invoke(delete_sentence, ['--sentence_id', 2])

        logger.debug("delete result output: {}".format(result.output))

        self.assertTrue(result.exit_code == 0)
