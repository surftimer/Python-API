from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from sql import selectQuery, insertQuery
from globals import get_cache, set_cache
from pydantic import BaseModel
from decimal import Decimal
import simplejson as json
import time, surftimer.queries


router = APIRouter()


@router.get(
    "/surftimer/selectReplayCPTicksAll",
    name="Get Replay Checkpoints Ticks",
    tags=["ck_replays"],
)
async def selectReplayCPTicksAll(
    request: Request,
    response: Response,
    mapname: str,
    style: int,
):
    """`char[] sql_selectReplayCPTicksAll = ....`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectReplayCPTicksAll:{mapname}-{style}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_selectReplayCPTicksAll.format(mapname, style)
    )

    if len(xquery) <= 0:
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    return xquery


@router.post(
    "/surftimer/insertReplayCPTicks",
    name="Add Replay Checkpoint Ticks",
    tags=["ck_replays"],
)
async def insertReplayCPTicks(
    request: Request,
    response: Response,
    mapname: str,
    cp: int,
    frame: int,
    style: int,
):
    """```c
    char[] sql_insertReplayCPTicks = ....
    ```"""
    tic = time.perf_counter()

    xquery = insertQuery(
        surftimer.queries.sql_insertReplayCPTicks.format(mapname, cp, frame, style)
    )

    content_data = {"inserted": xquery, "xtime": time.perf_counter() - tic}
    if xquery < 1:
        # response.body = json.dumps(content_data).encode('utf-8')
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return response

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    response.body = json.dumps(content_data).encode("utf-8")
    response.status_code = status.HTTP_201_CREATED
    return response


@router.put(
    "/surftimer/updateReplayCPTicks",
    name="Update Replay Checkpoint Ticks",
    tags=["ck_replays"],
)
async def updateReplayCPTicks(
    request: Request,
    response: Response,
    mapname: str,
    cp: int,
    frame: int,
    style: int,
):
    """```c
    char[] sql_updateReplayCPTicks = ....
    ```"""
    tic = time.perf_counter()

    xquery = insertQuery(
        surftimer.queries.sql_updateReplayCPTicks.format(frame, mapname, cp, style)
    )

    content_data = {"updated": xquery, "xtime": time.perf_counter() - tic}
    if xquery < 1:
        # response.body = json.dumps(content_data).encode('utf-8')
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return response

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    response.body = json.dumps(content_data).encode("utf-8")
    response.headers["content-type"] = "application/json"
    response.status_code = status.HTTP_200_OK
    return response
