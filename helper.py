from base64 import standard_b64decode, standard_b64encode
from datetime import datetime
from config import SHORTNER_API, SHORTNER_SITE, X_SHORTNER_API, X_SHORTNER_SITE
import pytz
import requests

def str_to_b64(__str: str) -> str:
    str_bytes = __str.encode("ascii")
    bytes_b64 = standard_b64encode(str_bytes)
    b64 = bytes_b64.decode("ascii")
    return b64


def b64_to_str(b64: str) -> str:
    bytes_b64 = b64.encode("ascii")
    bytes_str = standard_b64decode(bytes_b64)
    __str = bytes_str.decode("ascii")
    return __str


def get_current_time():
    tz = pytz.timezone("Asia/Kolkata")
    return int(datetime.now(tz).timestamp())


def shorten_url(url):
    def request_short_url(site, api):
        site_url = f"https://{site}/api?api={api}&url={url}&format=text"
        response = requests.get(site_url)
        response.raise_for_status()
        return response.text.strip()

    try:
        return request_short_url(SHORTNER_SITE, SHORTNER_API)
    except requests.RequestException as e:
        print(f"Error with primary shortener: {e}")
        try:
            return request_short_url(X_SHORTNER_SITE, X_SHORTNER_API)
        except requests.RequestException as ex:
            print(f"Error with fallback shortener: {ex}")
            return None
