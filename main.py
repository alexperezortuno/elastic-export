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
        greater_than: str = QUERY_GREATER_THAN
        less_than: str = QUERY_LESS_THAN
        query: str = ""
        es: Elasticsearch = None
        query_string: str = ELASTIC_QUERY_STRING
        query: str = ELASTIC_QUERY
        query_type: str = None
        file_output_name: str = FILE_OUTPUT_NAME
        file_format: str = FILE_FORMAT
        scroll_size: int = SCROLL_SIZE
        file: str = None
        output_path: str = FILE_OUTPUT_PATH
        headers: bool = False
        showquery: bool = False
        max_size: int = MAX_SIZE

        opts, args = getopt.getopt(sys.argv[1:],
                                   "hu:p:i:g:l:qs:q:t:o:f:s:d:c:show:m:",
                                   ["help=",
                                    "url=",
                                    "port=",
                                    "index=",
                                    "greater_than=",
                                    "less_than=",
                                    "query_string=",
                                    "query=",
                                    "type=",
                                    "output=",
                                    "format=",
                                    "scroll=",
                                    "output_path=",
                                    "columns=",
                                    "showquery=",
                                    "max_size=",
                                    ])

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print(documentation.doc_help())
                sys.exit(0)
            elif opt in ("-p", "--port"):
                ELASTIC_PORT = arg
            elif opt in ("-i", "--index"):
                ELASTIC_INDEX = arg
            elif opt in ("-u", "--url", "-host", "--host"):
                ELASTIC_URL = arg
            elif opt  == "-qs" or opt == "--query_string":
                query_string = arg
            elif opt == "-q" or opt == "--query":
                query = arg
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
            elif opt in ("-m", "--max_size"):
                max_size = int(arg)
            elif opt in ("-d", "--output_path"):
                output_path = arg
            elif opt in ("-c", "--columns"):
                headers = arg.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
            elif opt == "--showquery":
                showquery = arg.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']

        es = connect([f"{ELASTIC_SCHEME}://{ELASTIC_URL}:{ELASTIC_PORT}"])
        logger.debug(f"Parameters {query_string}:{query}:{query_type}:{file_output_name}:{file_format}:{scroll_size}:{output_path}:{headers}:{showquery}")

        if es is None:
            raise Exception("Elasticsearch not connected")

        file = create_if_not_exist(f'{file_output_name}.{file_format}', output_path)

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
                             max_size,
                             query,
                             query_string,
                             scroll_size,
                             None,
                             file,
                             headers,
                             None,
                             showquery)
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
