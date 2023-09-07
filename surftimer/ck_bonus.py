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

    content_data = {"inserted": xquery, "xtime": time.perf_counter() - tic}
    if xquery < 1:
        # response.body = response.body = json.dumps(content_data).encode('utf-8')
        response.status_code = status.HTTP_304_NOT_MODIFIED
        response.headers['content-type'] = 'application/json'
        return response

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    response.body = response.body = json.dumps(content_data).encode('utf-8')
    response.status_code = status.HTTP_201_CREATED
    response.headers['content-type'] = 'application/json'
    return response

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

    content_data = {"updated": xquery, "xtime": time.perf_counter() - tic}
    if xquery < 1:
        # response.body = json.dumps(content_data).encode('utf-8')
        response.headers['content-type'] = 'application/json'
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return response

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    response.body = json.dumps(content_data).encode('utf-8')
    response.headers['content-type'] = 'application/json'
    response.status_code = status.HTTP_200_OK
    return response

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
        return Response(status_code=status.HTTP_204_NO_CONTENT)
        # return JSONResponse(
        #     status_code=status.HTTP_404_NOT_FOUND,
        #     content={"xtime": time.perf_counter() - tic},
        # )

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
    steamid32: str,
    mapname: str,
    zonegroup: int,
):
    """```char sql_selectPlayerRankBonus[] = ....```"""
    tic = time.perf_counter()

    cache_key = (
        f"selectPlayerRankBonus:{steamid32}-{mapname}-{zonegroup}"
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
            steamid32,
            mapname,
            zonegroup,
            mapname,
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

    content_data = {"deleted": xquery, "xtime": time.perf_counter() - tic}
    if xquery < 1:
        # response.body = json.dumps(content_data).encode('utf-8')
        response.headers['content-type'] = 'application/json'
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return response

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    response.body = json.dumps(content_data).encode('utf-8')
    response.headers['content-type'] = 'application/json'
    response.status_code = status.HTTP_200_OK
    return response


## Stray queries scattered in SurfTimer code
@router.get(
    "/surftimer/selectPlayerSpecificBonusData",
    name="Get Player Specific Bonus Data",
    tags=["ck_bonus", "strays"],
)
def selectPlayerSpecificBonusData(
    request: Request,
    response: Response,
    steamid32: str,
    mapname: str,
    zonegroup: int,
):
    """```char sql_stray_selectPlayerSpecificBonusData[] = ....```"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectPlayerSpecificBonusData:{steamid32}-{mapname}-{zonegroup}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data, use_decimal=True, parse_nan=True)
        )

    xquery = selectQuery(
        surftimer.queries.sql_stray_selectPlayerSpecificBonusData.format(
            steamid32,
            mapname,
            zonegroup,
        )
    )

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code=status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/selectTotalBonusCompletesCount",
    name="Get Count Bonus Finished",
    tags=["ck_bonus", "strays"],
)
def selectTotalBonusCompletesCount(
    request: Request,
    response: Response,
    mapname: str,
    zonegroup: int,
):
    """```char sql_stray_selectTotalBonusCompletes[] = ....```"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectTotalBonusCompletesCount:{mapname}-{zonegroup}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data, use_decimal=True, parse_nan=True)
        )

    xquery = selectQuery(
        surftimer.queries.sql_stray_selectTotalBonusCompletes.format(
            mapname,
            zonegroup,
        )
    )

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code=status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery

@router.get(
    "/surftimer/selectPlayersBonusRank",
    name="Get Player Bonus Rank",
    tags=["ck_bonus", "strays"],
)
def selectPlayersBonusRank(
    request: Request,
    response: Response,
    steamid32: str,
    mapname: str,
    zonegroup: int,
):
    """```char sql_stray_selectPlayersBonusRank[] = ....```"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectPlayersBonusRank:{steamid32}-{mapname}-{zonegroup}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data, use_decimal=True, parse_nan=True)
        )

    xquery = selectQuery(
        surftimer.queries.sql_stray_selectPlayersBonusRank.format(
            steamid32,
            mapname,
            zonegroup,
            mapname,
            zonegroup
        )
    )

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code=status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery