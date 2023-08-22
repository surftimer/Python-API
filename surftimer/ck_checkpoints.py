from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from sql import selectQuery, insertQuery
from globals import get_cache, set_cache
from pydantic import BaseModel
import time, json, surftimer.queries


class PlayerCheckpoints(BaseModel):
    steamid: str
    mapname: str
    cp: int
    time: str
    stage_time: str
    stage_attempts: int
    zonegroup: int


router = APIRouter()


# ck_checkpoints
@router.post(
    "surftimer/insertOrUpdateCheckpoints",
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

    if xquery < 1:
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"inserted": xquery, "xtime": time.perf_counter() - tic},
        )

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}


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
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(
        surftimer.queries.sql_selectCheckpoints.format(mapname, steamid32)
    )

    if len(xquery) > 0:
        # xquery = xquery.pop()
        print("Hit, length:", len(xquery))
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content=status.HTTP_404_NOT_FOUND
        )

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
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(
        surftimer.queries.sql_selectCheckpointsinZoneGroup.format(
            mapname, steamid32, zonegroup
        )
    )

    if len(xquery) > 0:
        print("Hit, length:", len(xquery))
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content=status.HTTP_404_NOT_FOUND
        )

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
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(
        surftimer.queries.sql_selectRecordCheckpoints.format(
            steamid32, mapname, mapname
        )
    )

    if len(xquery) > 0:
        print("Hit, length:", len(xquery))
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content=status.HTTP_404_NOT_FOUND
        )

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

    if xquery <= 0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"xtime": time.perf_counter() - tic},
        )

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}


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
    cache_key = f"selectStageTimes:-{mapname}-{steamid32}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(
        surftimer.queries.sql_selectStageTimes.format(mapname, steamid32)
    )

    if len(xquery) > 0:
        print("Hit, length:", len(xquery))
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content=status.HTTP_404_NOT_FOUND
        )

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
    cache_key = f"selectStageAttempts:-{mapname}-{steamid32}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(
        surftimer.queries.sql_selectStageAttempts.format(mapname, steamid32)
    )

    if len(xquery) > 0:
        print("Hit, length:", len(xquery))
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content=status.HTTP_404_NOT_FOUND
        )

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    return xquery
