from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from sql import selectQuery, insertQuery
from globals import get_cache, set_cache
from pydantic import BaseModel
from decimal import Decimal
import simplejson as json
import time, surftimer.queries


class PlayerCheckpoints(BaseModel):
    """Body for adding or updating **Checkpoint** time"""

    steamid: str
    mapname: str
    cp: int
    time: Decimal
    stage_time: str
    stage_attempts: int
    zonegroup: int


router = APIRouter()


# ck_checkpoints
@router.post(
    "/surftimer/insertOrUpdateCheckpoints",
    name="Insert or Update Checkpoints",
    tags=["ck_checkpoints"],
)
async def insertOrUpdateCheckpoints(
    request: Request,
    response: Response,
    data: PlayerCheckpoints,
):
    tic = time.perf_counter()

    sql = surftimer.queries.sql_InsertOrUpdateCheckpoints.format(
        data.steamid,
        data.mapname,
        data.cp,
        data.time,
        data.stage_time,
        data.stage_attempts,
        data.zonegroup,
        data.time,
        data.stage_time,
        data.stage_attempts,
    )
    xquery = insertQuery(sql)
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


@router.get(
    "/surftimer/selectCheckpoints",
    name="Get Checkpoints",
    tags=["ck_checkpoints"],
)
async def selectCheckpoints(
    request: Request, response: Response, mapname: str, steamid32: str
):
    """`char[] sql_selectCheckpoints = ....`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectCheckpoints:{mapname}-{steamid32}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_selectCheckpoints.format(mapname, steamid32)
    )

    if len(xquery) > 0:
        # xquery = xquery.pop()
        print("Hit, length:", len(xquery))
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    return xquery


@router.get(
    "/surftimer/selectCheckpointsinZoneGroup",
    name="Get Checkpoints in Zonegroup",
    tags=["ck_checkpoints"],
)
async def selectCheckpointsinZoneGroup(
    request: Request,
    response: Response,
    mapname: str,
    steamid32: str,
    zonegroup: int,
):
    """`char[] sql_selectCheckpointsinZoneGroup = ....`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectCheckpointsinZoneGroup:{mapname}-{steamid32}-{zonegroup}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_selectCheckpointsinZoneGroup.format(
            mapname, steamid32, zonegroup
        )
    )

    if len(xquery) > 0:
        print("Hit, length:", len(xquery))
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    return xquery


@router.get(
    "/surftimer/selectRecordCheckpoints",
    name="Get Record Checkpoints",
    tags=["ck_checkpoints"],
)
async def selectRecordCheckpoints(
    request: Request, response: Response, steamid32: str, mapname: str
):
    """`char[] sql_selectRecordCheckpoints = ....`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectRecordCheckpoints:{steamid32}-{mapname}-{mapname}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_selectRecordCheckpoints.format(
            steamid32, mapname, mapname
        )
    )

    if len(xquery) > 0:
        print("Hit, length:", len(xquery))
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    return xquery


@router.delete(
    "/surftimer/deleteCheckpoints",
    name="Delete Checkpoint",
    tags=["ck_checkpoints"],
)
async def deleteCheckpoints(
    request: Request,
    response: Response,
    mapname: str,
):
    """```char sql_deleteCheckpoints[] = ....```"""
    tic = time.perf_counter()

    xquery = insertQuery(surftimer.queries.sql_deleteCheckpoints.format(mapname))

    content_data = {"deleted": xquery, "xtime": time.perf_counter() - tic}
    if xquery < 1:
        # response.body = json.dumps(content_data).encode('utf-8')
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return response

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    response.body = json.dumps(content_data).encode("utf-8")
    response.headers["content-type"] = "application/json"
    response.status_code = status.HTTP_200_OK
    return response


@router.get(
    "/surftimer/selectStageTimes",
    name="Get Stage Times",
    tags=["ck_checkpoints"],
)
async def selectStageTimes(
    request: Request, response: Response, mapname: str, steamid32: str
):
    """`char[] sql_selectStageTimes = ....`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectStageTimes:{mapname}-{steamid32}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_selectStageTimes.format(mapname, steamid32)
    )

    if len(xquery) > 0:
        print("Hit, length:", len(xquery))
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    return xquery


@router.get(
    "/surftimer/selectStageAttempts",
    name="Get Stage Attempts",
    tags=["ck_checkpoints"],
)
async def selectStageAttempts(
    request: Request, response: Response, mapname: str, steamid32: str
):
    """`char[] sql_selectStageAttempts = ....`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectStageAttempts:{mapname}-{steamid32}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_selectStageAttempts.format(mapname, steamid32)
    )

    if len(xquery) > 0:
        print("Hit, length:", len(xquery))
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    return xquery


@router.delete(
    "/surftimer/deleteWipePlayerCheckpoints",
    name="Wipe Player Checkpoint",
    tags=["ck_checkpoints", "strays", "Wipe"],
)
async def deleteWipePlayerCheckpoints(
    request: Request,
    response: Response,
    steamid32: str,
):
    """```char sql_stray_deleteWipePlayerCheckpoints[] = ....```"""
    tic = time.perf_counter()

    xquery = insertQuery(
        surftimer.queries.sql_stray_deleteWipePlayerCheckpoints.format(steamid32)
    )

    content_data = {"deleted": xquery, "xtime": time.perf_counter() - tic}
    if xquery < 1:
        # response.body = json.dumps(content_data).encode('utf-8')
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return response

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    response.body = json.dumps(content_data).encode("utf-8")
    response.headers["content-type"] = "application/json"
    response.status_code = status.HTTP_200_OK
    return response


@router.get(
    "/surftimer/selectCPR",
    name="Get Player Checkpoints for !cpr",
    tags=["ck_checkpoints", "strays"],
)
async def stray_selectCPR(
    request: Request,
    response: Response,
    steamid32: str,
    mapname: str,
):
    """`char[] sql_stray_selectCPR = ....`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectCPR:{steamid32}-{mapname}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_stray_selectCPR.format(steamid32, mapname)
    )

    if len(xquery) > 0:
        print("Hit, length:", len(xquery))
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    return xquery


@router.get(
    "/surftimer/ccp_getPlayerPR",
    name="Get Player CCP info",
    tags=["ck_checkpoints", "strays"],
)
async def ccp_getPlayerPR(
    request: Request,
    response: Response,
    mapname: str,
    steamid32: str,
):
    """`char[] sql_stray_ccp_getPlayerPR = ....`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"ccp_getPlayerPR:{mapname}-{steamid32}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_stray_ccp_getPlayerPR.format(steamid32, mapname)
    )

    if len(xquery) > 0:
        print("Hit, length:", len(xquery))
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    return xquery
