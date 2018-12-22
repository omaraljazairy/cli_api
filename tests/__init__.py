from fedal_cli.services.logger import get_logger
from fedal_cli.tests.fixtures import spanglish

logger = get_logger(loggername='spanglish')

def setup_package():
    """ This will run before any tests run. It will create some data in the database """ 

    logger.debug("create package fixture")
    spanglish.setup_language()
    spanglish.setup_category()
    spanglish.setup_word()
    spanglish.setup_sentence()
    spanglish.setup_verb()
 
def teardown_package():
    """ This will run at the end of all the tests. it will remove the data from the database """

    logger.debug("remove package fixture")
    spanglish.teardown_verb()
    spanglish.teardown_sentence()
    spanglish.teardown_word()
    spanglish.teardown_language()
    spanglish.teardown_category()



