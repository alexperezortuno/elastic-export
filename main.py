import os
import sys, getopt
from typing import Any

from elasticsearch import Elasticsearch
from core.log import logger
from core.elastic import connect, info, search
from core.tools import create_if_not_exist
from globals import documentation
from settings import *

if __name__ == "__main__":
    try:
        greater_than: str = None
        less_than: str = None
        query: str = ""
        es: Elasticsearch = None
        query_string: str = None
        query_type: str = None
        file_output_name: str = FILE_OUTPUT_NAME
        file_format: str = FILE_FORMAT
        scroll_size: int = SCROLL_SIZE
        file: str = None

        opts, args = getopt.getopt(sys.argv[1:],
                                   "hu:p:i:g:l:q:t:o:f:s:",
                                   ["help",
                                    "url",
                                    "port",
                                    "index",
                                    "greater_than",
                                    "less_than",
                                    "query",
                                    "type",
                                    "output",
                                    "format",
                                    "scroll"])

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print(documentation.doc_help())
                sys.exit(0)
            elif opt in ("-p", "--port"):
                ELASTIC_PORT = arg
            elif opt in ("-i", "--index"):
                ELASTIC_INDEX = arg
            elif opt in ("-host", "--host"):
                ELASTIC_URL = arg
            elif opt in ("-q", "--query"):
                query_string = arg
            elif opt in ("-t", "--type"):
                query_type = arg
            elif opt in ("-o", "--output"):
                file_output_name = arg
            elif opt in ("-f", "--format"):
                file_format = arg
            elif opt in ("-g", "--greater_than"):
                greater_than = arg
            elif opt in ("-l", "--less_than"):
                less_than = arg
            elif opt in ("-s", "--scroll"):
                scroll_size = int(arg)

        es = connect([f"{ELASTIC_SCHEME}://{ELASTIC_URL}:{ELASTIC_PORT}"])

        file = create_if_not_exist(f'{file_output_name}.{file_format}')

        if es is None:
            raise Exception("Elasticsearch not connected")

        if query_string is None:
            query_string = {"match_all": {}}

        if es is not None:
            logger.debug(es)
            if query_type is not None:
                if query_type == "info":
                    res = info(es)
                    logger.debug(f"{res}" + "\n")
            else:
                res = search(es,
                             ELASTIC_INDEX,
                             greater_than,
                             less_than,
                             MAX_SIZE,
                             query_string,
                             scroll_size,
                             None,
                             file,
                             )
                logger.debug(f"{res}" + "\n")
        sys.exit(0)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user... Exiting")
        sys.exit(0)
    except Exception as e:
        logger.error("{0}".format(e))
        sys.exit(1)
    except getopt.GetoptError as err:
        logger.error("{0}".format(err))
        sys.exit(1)
