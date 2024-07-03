from base64 import standard_b64decode, standard_b64encode
import datetime
import requests
import pytz
from config import SHORTNER_API, SHORTNER_SITE, A_SHORTNER_API, A_SHORTNER_SITE, B_SHORTNER_API, B_SHORTNER_SITE, C_SHORTNER_API, C_SHORTNER_SITE

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
    return int(datetime.datetime.now(tz).timestamp())

# Determine current hour for rotation based on the current time
def get_current_hour():
    tz = pytz.timezone("Asia/Kolkata")
    return datetime.datetime.now(tz).hour

# Define the rotating shortener site and API selection function
def get_rotating_shortener_info():
    current_hour = get_current_hour()
    rotation_period = (current_hour // 6) % 3
    
    if rotation_period == 0:
        return A_SHORTNER_SITE, A_SHORTNER_API
    elif rotation_period == 1:
        return B_SHORTNER_SITE, B_SHORTNER_API
    elif rotation_period == 2:
        return C_SHORTNER_SITE, C_SHORTNER_API

# Update your existing function to use the rotating shortener site and API
def shorten_url(url):
    def request_short_url(site, api):
        if not site.startswith('http://') and not site.startswith('https://'):
            site = 'https://' + site  # Ensure the site URL starts with a proper scheme
        site_url = f"{site}/api?api={api}&url={url}&format=text"
        response = requests.get(site_url)
        response.raise_for_status()
        return response.text.strip()

    try:
        return request_short_url(SHORTNER_SITE, SHORTNER_API)
    except requests.HTTPError as e:
        if e.response.status_code == 403:
            # Skip the 403 Forbidden error for the primary shortener and move to the fallback
            pass
        else:
            print(f"Error with primary shortener: {e}")
    except requests.RequestException as e:
        print(f"Error with primary shortener: {e}")

    try:
        rotating_site, rotating_api = get_rotating_shortener_info()
        return request_short_url(rotating_site, rotating_api)
    except requests.RequestException as ex:
        print(f"Error with fallback shortener: {ex}")
        return None
