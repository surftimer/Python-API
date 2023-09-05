from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from decimal import Decimal
import simplejson as json
from sql import selectQuery, insertQuery
from globals import (
    set_cache,
    get_cache,
)
import time, surftimer.queries


class NewBonus(BaseModel):
    steamid32: str
    name: str
    mapname: str
    runtime: Decimal
    zonegroup: int
    velStartXY: int
    velStartXYZ: int
    velStartZ: int


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
    tags=["ck_bonus"],
)
def insertBonus(
    request: Request,
    response: Response,
    data: NewBonus,
):
    """Inserts a new `Bonus` record to the table\n
    ```char sql_insertBonus[] = ....```"""
    tic = time.perf_counter()

    sql = surftimer.queries.sql_insertBonus.format(
        data.steamid32,
        data.name,
        data.mapname,
        data.runtime,
        data.zonegroup,
        data.velStartXY,
        data.velStartXYZ,
        data.velStartZ,
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

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}


@router.put(
    "/surftimer/updateBonus",
    name="Update Bonus Time",
    tags=["ck_bonus"],
)
def updateBonus(
    request: Request,
    response: Response,
    data: NewBonus,
):
    """```char sql_updateBonus[] = ....```"""
    tic = time.perf_counter()

    sql = surftimer.queries.sql_updateBonus.format(
        data.runtime,
        data.name,
        data.velStartXY,
        data.velStartXYZ,
        data.velStartZ,
        data.steamid32,
        data.mapname,
        data.zonegroup,
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
    tags=["ck_bonus"],
)
def selectBonusCount(request: Request, response: Response, mapname: str):
    """Retrieves all the bonuses for the map provided\n
    ```char sql_selectBonusCount[] = ....```"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectBonusCount:{mapname}"
    cached_data = get_cache(cache_key)
    if cached_data:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data, use_decimal=True, parse_nan=True)
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
    tags=["ck_bonus"],
)
def selectPersonalBonusRecords(
    request: Request, response: Response, steamid32: str, mapname: str
):
    """```char sql_selectPersonalBonusRecords[] = ....```"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectPersonalBonusRecords:{steamid32}-{mapname}"
    cached_data = get_cache(cache_key)

    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")

        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data, use_decimal=True, parse_nan=True)
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
    tags=["ck_bonus"],
)
def selectPlayerRankBonus(
    request: Request,
    response: Response,
    data: PlayerRankBonus,
):
    """```char sql_selectPlayerRankBonus[] = ....```"""
    tic = time.perf_counter()

    cache_key = (
        f"selectPlayerRankBonus:{data.steamid32}-{data.mapname}-{data.zonegroup}"
    )

    # # Check if data is cached in Redis
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data, use_decimal=True, parse_nan=True)
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
    tags=["ck_bonus"],
)
def selectFastestBonus(
    request: Request,
    response: Response,
    mapname: str,
):
    """```char sql_selectFastestBonus[] = ....```"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectFastestBonus:{mapname}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data, use_decimal=True, parse_nan=True)
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
    tags=["ck_bonus"],
)
def selectAllBonusTimesinMap(
    request: Request,
    response: Response,
    mapname: str,
):
    """```char sql_selectAllBonusTimesinMap[] = ....```"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectAllBonusTimesinMap:{mapname}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data, use_decimal=True, parse_nan=True)
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
    tags=["ck_bonus"],
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

    # Check if data is cached in Redis
    cache_key = f"selectTopBonusSurfers:{mapname}-{style}-{zonegroup}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data, use_decimal=True, parse_nan=True)
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
    tags=["ck_bonus"],
)
def deleteBonus(
    request: Request,
    response: Response,
    mapname: str,
):
    """```char sql_deleteBonus[] = ....```"""
    tic = time.perf_counter()

    xquery = insertQuery(surftimer.queries.sql_deleteBonus.format(mapname))

    if xquery <= 0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"xtime": time.perf_counter() - tic},
        )

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}
