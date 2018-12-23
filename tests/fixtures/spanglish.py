from fedal_cli.services.logger import get_logger
from fedal_cli.configs import settings
import psycopg2


logger = get_logger(loggername='spanglish_fixtures')

def db_conn():
    """ create the db connection and return a postgres object """

    host= settings.DB['HOST']
    port= settings.DB['PORT']
    user= settings.DB['USER']
    password= settings.DB['PASSWORD']
    db= settings.DB['NAME']

    conn_params = {
        'host': host,
        'port': port,
        'user': user,
        'password': password,
        'dbname': db,
    }

    try:
        connect_str = "host=" + host + "port=" + str(port) + "dbname=" + db + "user=" + user + \
                      "password=" + password
        
        # use our connection values to establish a connection
        conn = psycopg2.connect(**conn_params)
        logger.debug("connection db successfull ....")
        
        return conn
    
        # create a psycopg2 cursor that can execute queries
    except Exception as e:

        logger.error("Uh oh, can't connect. {}".format(e))




def setup_language():
    """ create a language with id 1 """
    
    logger.debug("setup language fixture")

    conn = db_conn() 

    try:
        cursor = conn.cursor()
        cursor.execute("""insert into spanglish_language (id, name, iso1) values (1, 'English', 'EN') ;""")
        result = cursor.rowcount
        conn.commit()

        logger.debug("language en created: {}".format(result))

    except Exception as e:

        logger.error("language insertion error. {}".format(e))

    finally:

        conn.close()


def setup_category():
    """ create two categories with id 1 & 2"""
    
    logger.debug("setup category fixture")

    conn = db_conn() 

    try:
        cursor = conn.cursor()
        cursor.execute(""" insert into spanglish_category (id, name, added) values (1, 'Entertainment', NOW()), (2, 'Greeting', NOW()), (3, 'Verb', NOW()); """)
        result = cursor.rowcount
        conn.commit()

        logger.debug("category created: {}".format(result))
        
    except Exception as e:

        logger.error("category insertion error. {}".format(e))

    finally:

        conn.close()



def setup_word():
    """ create two words with id 1 & 2 """
    
    logger.debug("setup word fixture")

    conn = db_conn() 

    try:
        cursor = conn.cursor()
        query = "insert into spanglish_word (id, word, word_en, category_id, language_id, added) " + \
                "values (1, 'hablar', 'talk', 3, 1, NOW()), (2, 'hola', 'hello', 2, 1, NOW()), " + \
                "(3, 'comer', 'eat', 3, 1, NOW()), (4, 'tomar', 'drink', 3, 1, NOW()); "
        cursor.execute(query)
        result = cursor.rowcount
        conn.commit()

        logger.debug("word created: {}".format(result))

    except Exception as e:

        logger.error("word insertion error. {}".format(e))

    finally:

        conn.close()



    
def setup_sentence():
    """ create two sentences with id 1 & 2 """
    
    logger.debug("setup sentence fixture")

    conn = db_conn()

    try:
        cursor = conn.cursor()
        query = "insert into spanglish_sentence (id, sentence, sentence_en, category_id, word_id, language_id, added) " + \
                "values (1, 'hablo testo', 'talk testing', 1, 1, 1, NOW() ), (2, 'habla bla', 'talk bla', 1, 1, 1, NOW() ); "
        cursor.execute(query)
        result = cursor.rowcount
        conn.commit()

        logger.debug("sentence created: {}".format(result))

    except Exception as e:

        logger.error("sentence insertion error. {}".format(e))

    finally:

        conn.close()


    
def setup_verb():
    """ create a verb with id 1 """
    
    logger.debug("setup verb fixture")

    conn = db_conn()
    try:
        cursor = conn.cursor()
        query = "insert into spanglish_verb (id, yo, tu, el_ella_ud, nosotros, vosotros, ellos_ellas_uds, tenses, word_id, added) " + \
                "values (1, 'hablo', 'hablas', 'habla', 'hablamos', 'hablais', 'hablan', 'SIMPLE_PRESENT', 1, NOW() ), " + \
                "(2, 'como', 'comes', 'come', 'comemos', 'comeis', 'comen', 'SIMPLE_PRESENT', 3, NOW() ); "
        cursor.execute(query)
        result = cursor.rowcount
        conn.commit()

        logger.debug("verb created: {}".format(result))

    except Exception as e:

        logger.error("verb insertion error. {}".format(e))

    finally:

        conn.close()



def teardown_language():
    """ delete all records in the language table """
    
    logger.debug("teardown language fixture")

    conn = db_conn() 
    cursor = conn.cursor()
    cursor.execute("""delete from spanglish_language;""")
    result = cursor.rowcount
    conn.commit()

    logger.debug("categories deleted: {}".format(result))
    conn.close()


def teardown_category():
    """ delete all records in the category table """
    
    logger.debug("teardown category fixture")

    conn = db_conn() 
    cursor = conn.cursor()
    cursor.execute("""delete from spanglish_category;""")
    result = cursor.rowcount
    conn.commit()

    logger.debug("categories deleted: {}".format(result))
    conn.close()

def teardown_word():
    """ delete all records in the words table """
    
    logger.debug("teardown word fixture")

    conn = db_conn() 
    cursor = conn.cursor()
    cursor.execute("""delete from spanglish_word;""")
    result = cursor.rowcount
    conn.commit()

    logger.debug("words deleted: {}".format(result))
    conn.close()


def teardown_sentence():
    """ delete all records in the sentence table """
    
    logger.debug("teardown sentence fixture")
    conn = db_conn() 
    cursor = conn.cursor()
    cursor.execute("""delete from spanglish_sentence;""")
    result = cursor.rowcount
    conn.commit()

    logger.debug("sentences deleted: {}".format(result))
    conn.close()
    

def teardown_verb():
    """ delete all records in the verb table """
    
    logger.debug("teardown verb fixture")
    conn = db_conn() 
    cursor = conn.cursor()
    cursor.execute("""delete from spanglish_verb;""")
    result = cursor.rowcount
    conn.commit()

    logger.debug("categories deleted: {}".format(result))
    conn.close()

