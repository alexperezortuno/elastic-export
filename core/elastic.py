import os

import pandas as pd
import json
from urllib.parse import unquote
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from typing import List, Optional
from core.log import logger
from core.types.elasticParams import ElasticParams

UNITS_MAPPING = [
    (1 << 50, ' PB'),
    (1 << 40, ' TB'),
    (1 << 30, ' GB'),
    (1 << 20, ' MB'),
    (1 << 10, ' KB'),
    (1, (' byte', ' bytes')),
]


def get_size(filepath: str, unit: str) -> float:
    size = os.path.getsize(filepath)
    if unit == 'b':
        return size
    elif unit == 'kb':
        return size / float(1 << 7)
    elif unit == 'KB':
        return size / float(1 << 10)
    elif unit == 'mb':
        return size / float(1 << 17)
    elif unit == 'MB':
        return size / float(1 << 20)
    elif unit == 'gb':
        return size / float(1 << 27)
    elif unit == 'GB':
        return size / float(1 << 30)
    elif unit == 'tb':
        return size / float(1 << 37)
    elif unit == 'TB':
        return size / float(1 << 40)


def pretty_size(bytesParm, units=None) -> str:
    """Get human-readable file sizes.
    simplified version of https://pypi.python.org/pypi/hurry.filesize/
    """
    global suffix, factor

    if units is None:
        units = UNITS_MAPPING
    for factor, suffix in units:
        if bytesParm >= factor:
            break
    amount = int(bytesParm / factor)

    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount) + suffix


def connect(hosts) -> Elasticsearch:
    try:
        client = Elasticsearch(hosts,
                               max_retries=3,
                               request_timeout=30,
                               http_compress=True,
                               headers={"Content-Type": "application/json"})
        # client.info()
        return client
    except Exception as e:
        logger.error(f"Failed to connect to Elasticsearch: {e}")
        return None


def index_exists(es, index):
    return es.indices.exists(index)


def info(es: Elasticsearch):
    try:
        return es.info()
    except Exception as e:
        logger.error(f"Failed to get Elasticsearch info: {e}")
        return None


def search(es: Elasticsearch,
           index: str,
           parameters: ElasticParams) -> Optional[pd.DataFrame]:
    """
    Search for documents in Elasticsearch.
    :param es: Elasticsearch
    :param index: string
    :param parameters: ElasticParams
    :return:
    """
    # print(f"Searching for {parameters.gte}")
    try:
        date_gte = datetime.strptime(parameters.gte, "%Y-%m-%dT%H:%M:%S") if parameters.gte else None
        date_lte = datetime.strptime(parameters.lte, "%Y-%m-%dT%H:%M:%S") if parameters.lte else None
        must = []

        f = Q('range',
              **{'@timestamp':
                  {
                      'gte': date_gte.strftime('%Y-%m-%d %H:%M:%S'),
                      'lt': date_lte.strftime('%Y-%m-%d %H:%M:%S'),
                      'format': 'yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis'
                  }
              })

        q = Q('bool', must=must, filter=[f])

        body: dict = {
            'size': parameters.size,
            'query': q.to_dict(),
        }

        if parameters.query_string != '':
            body.get('query').get('bool')['must'] = [{'query_string': {'query': parameters.query_string}}]

        if parameters.query != '':
            q = parameters.query.split(',')
            for i in q:
                must_string = i.split('=')
                # body.get('query').get('bool')['must'].append(Q('match', **{must_string[0]: must_string[1]}))

        if parameters.rawquery != '':
            body['query'] = json.loads(unquote(parameters.rawquery))

        if parameters.showquery:
            print(json.dumps(body, indent=4))
            # with open(file_name, 'w', encoding='utf-8') as f:
            #     json.dump(body, f, ensure_ascii=False, indent=4)
            return None

        if parameters.scroll_id is None:
            response = es.search(index=index,
                                 body=body,
                                 size=parameters.size,
                                 sort=parameters.sort,
                                 scroll=parameters.scroll)
        else:
            response = es.scroll(scroll=parameters.scroll, scroll_id=parameters.scroll_id)

        if len(response.get('hits').get('hits')) > 0:
            if parameters.max_size is not None and parameters.max_size <= int(get_size(parameters.file, 'MB')):
                return None

            l: List = response.get('hits').get('hits')
            data_list: List = []

            for i in l:
                data_list.append(i['_source'].values())

            # file = open(parameters.file)
            # file.seek(0, os.SEEK_END)

            # print(f"{pretty_size(file.tell())}")

            data = pd.DataFrame(data_list, columns=i['_source'].keys())
            data.to_csv(parameters.file, mode='a', header=parameters.headers, index=False)
            parameters.count += len(data_list)
            parameters.scroll_id = response.get('_scroll_id')

            return search(es,
                          index,
                          parameters)

        return response
    except Exception as e:
        logger.error(f"Failed to search Elasticsearch: {e}")
        return None
