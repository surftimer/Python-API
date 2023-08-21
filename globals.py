import json, redis, time
from decimal import Decimal
from fastapi.security import HTTPBearer
from fastapi import Request
from datetime import datetime



token_auth_scheme = HTTPBearer()

# Config
with open("config.json", "r") as f:
    config = json.load(f)

# Requests Log
with open("requests.json") as fp:
    log = json.load(fp)


# Initiate Redis connection
redis_client = redis.Redis(
    host=config["REDIS"]["HOST"],
    port=config["REDIS"]["PORT"],
    password=config["REDIS"]["PASSWORD"],
)


# Whitelisted IPs
WHITELISTED_IPS = config["WHITELISTED_IPS"]


def append_request_log(request: Request):
    """Logs some general info about the request recieved in `requests.json`"""
    log.append(
        {
            "url": str(request.url),
            "ip": request.client.host,
            "method": request.method,
            "headers": dict(request.headers),
            "time": str(datetime.now()),
        }
    )
    with open("requests.json", "w") as json_file:
        json.dump(log, json_file, indent=4, separators=(",", ": "))


def set_cache(cache_key: str, data):
    """Cache the data in Redis\n
    `Decimal` values are converted to `String`"""
    redis_client.set(
        cache_key,
        json.dumps(data, default=json_decimal),
        ex=config["REDIS"]["EXPIRY"],
    )

    return True


def get_cache(cache_key: str):
    """Try and get cached data from Redis"""
    cached_data = redis_client.get(cache_key)
    if cached_data:
        # Return cached data
        # print(json.loads(cached_data))
        return cached_data
    else:
        return None


def json_decimal(obj):
    """Convert all instances of `Decimal` to `String`
    `"runtime": 14.7363` > `"runtime": "14.736300"`
    `"runtime": 11.25` > `"runtime": "11.250000"`"""
    if isinstance(obj, Decimal):
        return str(obj)
    elif isinstance(obj, list):
        for i in range(len(obj)):
            if isinstance(obj[i], dict):
                for key, value in obj[i].items():
                    if isinstance(value, Decimal):
                        obj[i][key] = str(value)
        return obj
    # If it's neither a Decimal nor a list of dictionaries, return it as is
    return str(obj)