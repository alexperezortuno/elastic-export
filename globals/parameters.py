import ast
import os

ELASTIC_URL: str = os.environ.get('ELASTIC_URL', 'http://localhost')
ELASTIC_PORT: int = ast.literal_eval(os.environ.get('ELASTIC_PORT', '9200'))
ELASTIC_SCHEME: str = os.environ.get('ELASTIC_SCHEME', 'http')
ELASTIC_INDEX: str = os.environ.get('ELASTIC_INDEX', 'test')
MAX_SIZE: int = ast.literal_eval(os.environ.get('MAX_SIZE', '5000'))
LOG_FORMAT: str = os.environ.get('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOG_LEVEL: str = os.environ.get('LOG_LEVEL', 'INFO')
FILE_OUTPUT_NAME: str = os.environ.get('FILE_OUTPUT_NAME', 'output')
FILE_FORMAT: str = os.environ.get('FILE_FORMAT', 'csv')
QUERY: str = os.environ.get('QUERY', '*')
SCROLL_SIZE: str = os.environ.get('SCROLL_SIZE', '1m')
