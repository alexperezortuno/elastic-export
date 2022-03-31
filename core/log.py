import logging
from globals.parameters import LOG_LEVEL, LOG_FORMAT

import coloredlogs

logger = logging.getLogger(__name__)
coloredlogs.install(level=LOG_LEVEL, logger=logger)
coloredlogs.install(fmt=LOG_FORMAT)
