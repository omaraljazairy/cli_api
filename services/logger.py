import logging
import logging.config
import yaml

def get_logger(loggername=str):
    """ gets the logger name and returns a logger """

    log_conf = open('configs/logger.yaml')
    config = yaml.load(log_conf.read())
    logging.config.dictConfig(config)
    logger = logging.getLogger(loggername)

    return logger    
