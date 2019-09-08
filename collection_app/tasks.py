import requests
from celery import Celery
from celery.result import AsyncResult

from collection_app.request_manager import RequestManager

app = Celery(
    namespace='tasks',
    backend='rpc://',
    broker='pyamqp://guest@localhost//',
)

app.config_from_object('collection_app.celeryconfig')


@app.task
def make_request(url: str) -> AsyncResult:
    """Make request using requests session from RequestManager"""

    rm = RequestManager()

    try:
        result = rm.session.get(url)
        result.raise_for_status()
        return result.json()
    except requests.HTTPError as err:
        raise err
