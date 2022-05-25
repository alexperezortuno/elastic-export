import sys, getopt

from elasticsearch import Elasticsearch
from core.log import logger
from core.elastic import connect, info, search
from core.tools import create_if_not_exist
from core.types.elasticParams import ElasticParams
from globals import documentation
from settings import QUERY_GREATER_THAN, QUERY_LESS_THAN, ELASTIC_QUERY_STRING, ELASTIC_QUERY, FILE_OUTPUT_NAME, \
    FILE_FORMAT, SCROLL_STR, FILE_OUTPUT_PATH, SIZE, ELASTIC_SCHEME, ELASTIC_URL, ELASTIC_PORT, ELASTIC_INDEX, \
    MAX_CONTENT, MAX_SIZE

if __name__ == "__main__":
    try:
        params = ElasticParams(gte=QUERY_GREATER_THAN,
                               lte=QUERY_LESS_THAN,
                               query_string=ELASTIC_QUERY_STRING,
                               query=ELASTIC_QUERY,
                               size=SIZE,
                               max_size=MAX_SIZE,
                               output_path=FILE_OUTPUT_PATH,
                               scroll=SCROLL_STR,
                               max_content=MAX_CONTENT)
        es: Elasticsearch = None
        query_type: str = ''
        file_output_name: str = FILE_OUTPUT_NAME
        file_format: str = FILE_FORMAT
        output_path: str = FILE_OUTPUT_PATH
        elastic_scheme: str = ELASTIC_SCHEME
        elastic_url: str = ELASTIC_URL
        elastic_port: int = ELASTIC_PORT
        elastic_index: str = ELASTIC_INDEX

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
                                    "size=",
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
                params.query_string = arg
            if opt == "-q" or opt == "--query":
                params.query = arg
            if opt == "-t" or opt == "--type":
                query_type = arg
            if opt == "-o" or opt == "--output":
                file_output_name = arg
            if opt == "-f" or opt == "--format":
                file_format = arg
            if opt == "-gt" or opt == "--greater_than":
                params.gte = arg
            if opt == "-lt" or opt == "--less_than":
                params.lte = arg
            if opt == "--scroll":
                params.scroll = arg
            if opt == "-l" or opt == "--limit":
                params.limit = int(arg)
            if opt == "-d" or opt == "--output_path":
                params.output_path = arg
            if opt == "-c" or opt == "--columns":
                params.headers = arg.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
            if opt == "--showquery":
                params.showquery = arg.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
            if opt == "--rawquery":
                params.rawquery = arg
            if opt == "--max_size":
                params.max_size = arg
            if opt == "--max_content":
                params.max_content = arg

        es = connect([f"{elastic_scheme}://{elastic_url}:{elastic_port}"])
        logger.debug(
            f"Parameters {params.query_string}:{params.query}:{file_output_name}:{file_format}:{params.scroll}:{output_path}:{params.headers}:{params.showquery}")

        if es is None:
            raise Exception("Elasticsearch not connected")

        params.file = create_if_not_exist(f'{file_output_name}.{file_format}', output_path)

        if es is not None:
            logger.debug(es)
            if query_type != '':
                if query_type == "info":
                    res = info(es)
                    logger.debug(f"{res}" + "\n")
            else:
                logger.debug(f"{params.gte}")
                res = search(es,
                             elastic_index,
                             params)
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
