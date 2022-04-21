import sys, getopt

from elasticsearch import Elasticsearch
from core.log import logger
from core.elastic import connect, info, search
from core.tools import create_if_not_exist
from globals import documentation
from settings import QUERY_GREATER_THAN, QUERY_LESS_THAN, ELASTIC_QUERY_STRING, ELASTIC_QUERY, FILE_OUTPUT_NAME, \
    FILE_FORMAT, SCROLL_STR, FILE_OUTPUT_PATH, MAX_SIZE, ELASTIC_SCHEME, ELASTIC_URL, ELASTIC_PORT, ELASTIC_INDEX

if __name__ == "__main__":
    try:
        greater_than: str = QUERY_GREATER_THAN
        less_than: str = QUERY_LESS_THAN
        query: str = ""
        es: Elasticsearch = None
        query_string: str = ELASTIC_QUERY_STRING
        query: str = ELASTIC_QUERY
        query_type: str = ''
        file_output_name: str = FILE_OUTPUT_NAME
        file_format: str = FILE_FORMAT
        scroll_str: str = SCROLL_STR
        file: str = ''
        output_path: str = FILE_OUTPUT_PATH
        headers: bool = False
        showquery: bool = False
        max_size: int = MAX_SIZE
        elastic_scheme: str = ELASTIC_SCHEME
        elastic_url: str = ELASTIC_URL
        elastic_port: int = ELASTIC_PORT
        elastic_index: str = ELASTIC_INDEX
        rawquery: str = ''

        opts, args = getopt.getopt(sys.argv[1:],
                                   "hu:p:i:g:l:qs:q:t:o:f:s:d:c:show:m:r:",
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
                                    "rawquery="
                                    ])

        for opt, arg in opts:
            if opt == "-h" or opt == "--help":
                print(documentation.doc_help())
                sys.exit(0)
            if opt == "-p" or opt == "--port":
                elastic_port = arg
            if opt == "-i" or opt == "--index":
                elastic_index = arg
            if opt == "-u" or opt == "--url" or opt == "-host" or opt == "--host":
                elastic_url = arg
            if opt == "--query_string":
                query_string = arg
            if opt == "-q" or opt == "--query":
                query = arg
            if opt == "-t" or opt == "--type":
                query_type = arg
            if opt == "-o" or opt == "--output":
                file_output_name = arg
            if opt == "-f" or opt == "--format":
                file_format = arg
            if opt == "-g" or opt == "--greater_than":
                greater_than = arg
            if opt == "-l" or opt == "--less_than":
                less_than = arg
            if opt == "--scroll":
                scroll_str = arg
            if opt == "-m" or opt == "--max_size":
                max_size = int(arg)
            if opt == "-d" or opt == "--output_path":
                output_path = arg
            if opt == "-c" or opt == "--columns":
                headers = arg.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
            if opt == "--showquery":
                showquery = arg.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
            if opt == "--rawquery":
                rawquery = arg

        es = connect([f"{elastic_scheme}://{elastic_url}:{elastic_port}"])
        logger.debug(
            f"Parameters {query_string}:{query}:{query_type}:{file_output_name}:{file_format}:{scroll_str}:{output_path}:{headers}:{showquery}")

        if es is None:
            raise Exception("Elasticsearch not connected")

        file = create_if_not_exist(f'{file_output_name}.{file_format}', output_path)

        if es is not None:
            logger.debug(es)
            if query_type != '':
                if query_type == "info":
                    res = info(es)
                    logger.debug(f"{res}" + "\n")
            else:
                res = search(es,
                             elastic_index,
                             greater_than,
                             less_than,
                             max_size,
                             query,
                             query_string,
                             scroll_str,
                             None,
                             file,
                             headers,
                             None,
                             showquery,
                             rawquery)
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
