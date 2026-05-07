import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from utils.config import DEFAULT_HEADERS, REQUEST_TIMEOUT

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class ApiClient:
    """Wrapper sobre requests com retry automático e logging das chamadas."""

    def __init__(self, base_headers: dict | None = None):
        self.session = requests.Session()
        self.session.headers.update(base_headers or DEFAULT_HEADERS)

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _log_request(self, method: str, url: str, **kwargs):
        logger.info(f"[{method}] {url}")
        if kwargs.get("json"):
            logger.info(f"  Body: {kwargs['json']}")

    def get(self, url: str, **kwargs):
        self._log_request("GET", url, **kwargs)
        return self.session.get(url, timeout=REQUEST_TIMEOUT, **kwargs)

    def post(self, url: str, **kwargs):
        self._log_request("POST", url, **kwargs)
        return self.session.post(url, timeout=REQUEST_TIMEOUT, **kwargs)

    def put(self, url: str, **kwargs):
        self._log_request("PUT", url, **kwargs)
        return self.session.put(url, timeout=REQUEST_TIMEOUT, **kwargs)

    def delete(self, url: str, **kwargs):
        self._log_request("DELETE", url, **kwargs)
        return self.session.delete(url, timeout=REQUEST_TIMEOUT, **kwargs)

    def close(self):
        self.session.close()
