import sys
import logging
import logging.handlers
import logging.config

DISABLE__STD = False

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

intelliAurom_verbose = False


def log(s):
    if intelliAurom_verbose:
        logger.info(s)


def say(s):
    print s


def ssay(s):
    if intelliAurom_verbose:
        print s
        logger.info(s)


def log_error(s):
    if intelliAurom_verbose:
        logger.error(s)


def log_warning(s):
    if intelliAurom_verbose:
        logger.warning(s)


def log_debug(s):
    if intelliAurom_verbose:
        logger.debug(s)


def std_write(s):
    if (intelliAurom_verbose) and (not DISABLE__STD):
        sys.stdout.write(s)
        sys.stdout.flush()
