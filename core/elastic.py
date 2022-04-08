import pandas as pd
import json
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from typing import List, Optional
from core.log import logger


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
           gte: str = None,
           lte: str = None,
           size: int = 10,
           query: str = '',
           query_string: str = '',
           scroll: str = '1m',
           scroll_id: str = None,
           file_name: str = None,
           headers: bool = False,
           sort: List[str] = None,
           showquery: bool = False) -> Optional[pd.DataFrame]:
    """
    Search for documents in Elasticsearch.
    :param es: string
    :param index: string
    :param gte: string
    :param lte: string
    :param size: int
    :param query: string
    :param query_string: string
    :param scroll: string
    :param scroll_id: string
    :param file_name: string
    :param headers: bool
    :param sort: List[str]
    :param showquery: bool
    :return:
    """
    try:
        date_gte = datetime.strptime(gte, "%Y-%m-%dT%H:%M:%S") if gte else None
        date_lte = datetime.strptime(lte, "%Y-%m-%dT%H:%M:%S") if lte else None
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
            'size': size,
            'query': q.to_dict(),
        }

        if query_string != '':
            body.get('query').get('bool')['must'] = [{'query_string': {'query': query_string}}]

        if query != '':
            q = query.split(',')
            for i in q:
                must_string = i.split('=')
                # body.get('query').get('bool')['must'].append(Q('match', **{must_string[0]: must_string[1]}))

        if showquery:
            print(json.dumps(body, indent=4))
            # with open(file_name, 'w', encoding='utf-8') as f:
            #     json.dump(body, f, ensure_ascii=False, indent=4)
            return None

        if scroll_id is None:
            response = es.search(index=index, body=body, size=size, sort=sort, scroll=scroll)
        else:
            response = es.scroll(scroll=scroll, scroll_id=scroll_id)

        if len(response.get('hits').get('hits')) > 0:
            l: List = response.get('hits').get('hits')
            data_list: List = []

            for i in l:
                data_list.append(i['_source'].values())

            data = pd.DataFrame(data_list, columns=i['_source'].keys())
            data.to_csv(file_name, mode='a', header=headers, index=False)

            return search(es,
                          index,
                          gte,
                          lte,
                          size,
                          query,
                          query_string,
                          scroll,
                          response.get('_scroll_id'),
                          file_name,
                          False,
                          sort,
                          showquery)

        return response
    except Exception as e:
        logger.error(f"Failed to search Elasticsearch: {e}")
        return None
