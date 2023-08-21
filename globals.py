import json, redis
from decimal import Decimal
from fastapi.security import HTTPBearer
from fastapi import Request
from datetime import datetime
from auth import VerifyToken

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
