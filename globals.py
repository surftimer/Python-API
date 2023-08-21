import json, redis, time
from decimal import Decimal
from fastapi.security import HTTPBearer
from fastapi import Request
from datetime import datetime
from auth import VerifyToken
from pydantic import BaseModel


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
    """Convert all instances of `Decimal` to `String`\n
    `"runtime": 14.7363` > `"runtime": "14.736300"`\n
    `"runtime": 11.25` > `"runtime": "11.250000"`"""
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError



class PlayerOptions(BaseModel):
    """To be used for `updatePlayerOptions` endpoint"""

    timer: int
    hide: int
    sounds: int
    chat: int
    viewmodel: int
    autobhop: int
    checkpoints: int
    gradient: int
    speedmode: int
    centrespeed: int
    centrehud: int
    teleside: int
    module1c: int
    module2c: int
    module3c: int
    module4c: int
    module5c: int
    module6c: int
    sidehud: int
    module1s: int
    module2s: int
    module3s: int
    module4s: int
    module5s: int
    prestrafe: int
    cpmessages: int
    wrcpmessages: int
    hints: int
    csd_update_rate: int
    csd_pos_x: int
    csd_pos_y: int
    csd_r: int
    csd_g: int
    csd_b: int
    prespeedmode: int
    steamid32: str
