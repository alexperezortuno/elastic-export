import os
import sys, getopt
from typing import Any

from elasticsearch import Elasticsearch
from core.log import logger
from core.elastic import connect, info, search
from globals import parameters, documentation

if __name__ == "__main__":
    try:
        start: str = None
        end: str = None
        query: str = ""
        es: Elasticsearch = None
        query_string: str = None
        query_type: str = None

        opts, args = getopt.getopt(sys.argv[1:], "hu:p:i:s:e:q:t:", ["help", "url", "port", "index", "start", "end", "query", "type"])

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print(documentation.doc_help())
                sys.exit(0)
            elif opt in ("-p", "--port"):
                parameters.ELASTIC_PORT = arg
            elif opt in ("-i", "--index"):
                parameters.ELASTIC_INDEX = arg
            elif opt in ("-host", "--host"):
                parameters.ELASTIC_URL = arg
            elif opt in ("-s", "--start"):
                start = arg
            elif opt in ("-e", "--end"):
                end = arg
            elif opt in ("-q", "--query"):
                query_string = arg
            elif opt in ("-t", "--type"):
                query_type = arg


        logger.debug(parameters.ELASTIC_URL)
        logger.debug(parameters.ELASTIC_PORT)
        logger.debug(parameters.ELASTIC_INDEX)

        if start != "" and end != "":
            logger.debug(start)
            logger.debug(end)
            logger.debug(query)

        es = connect([f"{parameters.ELASTIC_SCHEME}://{parameters.ELASTIC_URL}:{parameters.ELASTIC_PORT}"])

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
                res = search(es, parameters.ELASTIC_INDEX, start, end, 0, parameters.MAX_SIZE)
                logger.debug(f"{res}" + "\n")
        sys.exit(0)
    except Exception as e:
        logger.error("{0}".format(e))
        sys.exit(1)
    except getopt.GetoptError as err:
        logger.error("{0}".format(err))
        sys.exit(1)
