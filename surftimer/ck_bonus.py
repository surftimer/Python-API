from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sql import selectQuery, insertQuery
from globals import (
    redis_client,
    config,
    append_request_log,
    set_cache,
    get_cache,
    PlayerOptions,
)
import time, json, surftimer.queries


class PlayerRankBonus(BaseModel):
    """To be used for `selectPlayerRankBonus` endpoint"""

    steamid32: str
    mapname: str
    zonegroup: int


router = APIRouter()


# ck_bonus
@router.post(
    "/surftimer/insertBonus",
    name="Add Bonus Time",
    tags=["SurfTimer", "ck_bonus"],
)
def insertBonus(
    request: Request,
    response: Response,
    steamid32: str,
    name: str,
    mapname: str,
    runtime: int,
    zonegroup: int,
    velStartXY: int,
    velStartXYZ: int,
    velStartZ: int,
):
    """Inserts a new record to the table\n
    ```char sql_insertLatestRecords[] = ....```"""
    tic = time.perf_counter()
    append_request_log(request)

    sql = surftimer.queries.sql_insertBonus.format(
        steamid32,
        name,
        mapname,
        runtime,
        zonegroup,
        velStartXY,
        velStartXYZ,
        velStartZ,
    )
    xquery = insertQuery(sql)
    # xquery = 0
    # time.sleep(3)

    if xquery < 1:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"inserted": xquery, "xtime": time.perf_counter() - tic},
        )

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")
    # output = ResponseInsertQuery(xquery)

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}


@router.put(
    "/surftimer/updateBonus",
    name="Update Bonus Time",
    tags=["SurfTimer", "ck_bonus"],
)
def updateBonus(
    request: Request,
    response: Response,
    steamid32: str,
    name: str,
    mapname: str,
    runtime: str,
    zonegroup: int,
    velStartXY: int,
    velStartXYZ: int,
    velStartZ: int,
):
    """```char sql_updateBonus[] = ....```"""
    tic = time.perf_counter()
    append_request_log(request)

    sql = surftimer.queries.sql_updateBonus.format(
        runtime,
        name,
        velStartXY,
        velStartXYZ,
        velStartZ,
        steamid32,
        mapname,
        zonegroup,
    )
    xquery = insertQuery(sql)

    if xquery < 1:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"inserted": xquery, "xtime": time.perf_counter() - tic},
        )

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}


@router.get(
    "/surftimer/selectBonusCount",
    name="Get Bonus Count",
    tags=["SurfTimer", "ck_bonus"],
)
def selectBonusCount(request: Request, response: Response, mapname: str):
    """Retrieves all the bonuses for the map provided\n
    ```char sql_selectBonusCount[] = ....```"""
    tic = time.perf_counter()

    append_request_log(request)

    # Check if data is cached in Redis
    cache_key = f"selectBonusCount_{mapname}"
    cached_data = get_cache(cache_key)
    if cached_data:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(surftimer.queries.sql_selectBonusCount.format(mapname))

    if len(xquery) <= 0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"xtime": time.perf_counter() - tic},
        )

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/selectPersonalBonusRecords",
    name="Get Personal Bonus Records",
    tags=["SurfTimer", "ck_bonus"],
)
def selectPersonalBonusRecords(
    request: Request, response: Response, steamid32: str, mapname: str
):
    """```char sql_selectPersonalBonusRecords[] = ....```"""
    tic = time.perf_counter()

    append_request_log(request)

    # Check if data is cached in Redis
    cache_key = f"selectPersonalBonusRecords:{steamid32}-{mapname}"
    cached_data = get_cache(cache_key)

    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")

        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(
        surftimer.queries.sql_selectPersonalBonusRecords.format(steamid32, mapname)
    )

    if len(xquery) <= 0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"xtime": time.perf_counter() - tic},
        )

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/selectPlayerRankBonus",
    name="Get Player Rank Bonus",
    tags=["SurfTimer", "ck_bonus"],
)
def selectPlayerRankBonus(
    request: Request,
    response: Response,
    data: PlayerRankBonus,
):
    """```char sql_selectPlayerRankBonus[] = ....```"""
    tic = time.perf_counter()

    append_request_log(request)
    cache_key = (
        f"selectPlayerRankBonus:{data.steamid32}-{data.mapname}-{data.zonegroup}"
    )

    # # Check if data is cached in Redis
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(
        surftimer.queries.sql_selectPlayerRankBonus.format(
            data.steamid32,
            data.mapname,
            data.zonegroup,
            data.mapname,
            data.zonegroup,
        )
    )

    if len(xquery) <= 0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"xtime": time.perf_counter() - tic},
        )

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/selectFastestBonus",
    name="Get Fastest Bonus",
    tags=["SurfTimer", "ck_bonus"],
)
def selectFastestBonus(
    request: Request,
    response: Response,
    mapname: str,
):
    """```char sql_selectFastestBonus[] = ....```"""
    tic = time.perf_counter()

    append_request_log(request)

    # Check if data is cached in Redis
    cache_key = f"selectFastestBonus:{mapname}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(surftimer.queries.sql_selectFastestBonus.format(mapname))

    if len(xquery) <= 0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"xtime": time.perf_counter() - tic},
        )

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/selectAllBonusTimesinMap",
    name="Get All Bonus Times For Map",
    tags=["SurfTimer", "ck_bonus"],
)
def selectAllBonusTimesinMap(
    request: Request,
    response: Response,
    mapname: str,
):
    """```char sql_selectAllBonusTimesinMap[] = ....```"""
    tic = time.perf_counter()

    append_request_log(request)

    # Check if data is cached in Redis
    cache_key = f"selectAllBonusTimesinMap:{mapname}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(surftimer.queries.sql_selectAllBonusTimesinMap.format(mapname))

    if len(xquery) <= 0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"xtime": time.perf_counter() - tic},
        )

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/selectTopBonusSurfers",
    name="Get All Top Bonus Surfers",
    tags=["SurfTimer", "ck_bonus"],
)
def selectTopBonusSurfers(
    request: Request,
    response: Response,
    mapname: str,
    style: int,
    zonegroup: int,
):
    """```char sql_selectTopBonusSurfers[] = ....```"""
    tic = time.perf_counter()

    append_request_log(request)

    # Check if data is cached in Redis
    cache_key = f"selectTopBonusSurfers:{mapname}-{style}-{zonegroup}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(
        surftimer.queries.sql_selectTopBonusSurfers.format(
            mapname,
            style,
            style,
            zonegroup,
        )
    )

    if len(xquery) <= 0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"xtime": time.perf_counter() - tic},
        )

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.delete(
    "/surftimer/deleteBonus",
    name="Delete Bonus",
    tags=["SurfTimer", "ck_bonus"],
)
def deleteBonus(
    request: Request,
    response: Response,
    mapname: str,
):
    """```char sql_deleteBonus[] = ....```"""
    tic = time.perf_counter()

    append_request_log(request)

    xquery = insertQuery(surftimer.queries.sql_deleteBonus.format(mapname))

    if xquery <= 0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"xtime": time.perf_counter() - tic},
        )

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}