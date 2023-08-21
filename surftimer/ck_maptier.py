from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from sql import selectQuery, insertQuery
from globals import redis_client, config, append_request_log, get_cache, set_cache
import time, json
import surftimer.queries

router = APIRouter()


# ck_maptier
@router.get(
    "/surftimer/selectMapTier",
    name="Get Map Tier",
    tags=["SurfTimer", "ck_maptier"],
)
def selectMapTier(
    request: Request,
    response: Response,
    mapname: str,
):
    """`char[] sql_selectMapTier = ....`"""
    tic = time.perf_counter()
    append_request_log(request)

    # Check if data is cached in Redis
    cache_key = f"selectMapTier_{mapname}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")

        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(surftimer.queries.sql_selectMapTier.format(mapname))

    if xquery:
        xquery = xquery.pop()
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"mapname": mapname, "xtime": time.perf_counter() - tic},
        )

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")
    
    return xquery


@router.post(
    "/surftimer/insertMapTier",
    name="Add Map Tier",
    tags=["SurfTimer", "ck_maptier"],
)
def insertMapTier(
    request: Request,
    response: Response,
    mapname: str,
    tier: int,
):
    """```c
    char[] sql_insertmaptier = ....
    ```"""
    tic = time.perf_counter()
    append_request_log(request)

    xquery = insertQuery(surftimer.queries.sql_insertmaptier.format(mapname, tier))

    if xquery < 1:
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"inserted": xquery, "xtime": time.perf_counter() - tic},
        )

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")
    # output = ResponseInsertQuery(xquery)

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}


@router.put(
    "/surftimer/updateMapTier",
    name="Update Map Tier",
    tags=["SurfTimer", "ck_maptier"],
)
def updateMapTier(
    request: Request,
    response: Response,
    mapname: str,
    tier: int,
):
    """```c
    char[] sql_updatemaptier = ....
    ```"""
    tic = time.perf_counter()
    append_request_log(request)

    xquery = insertQuery(surftimer.queries.sql_updatemaptier.format(tier, mapname))

    if xquery < 1:
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"inserted": xquery, "xtime": time.perf_counter() - tic},
        )

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")
    # output = ResponseInsertQuery(xquery)

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}


@router.put(
    "/surftimer/updateMapperName",
    name="Update Mapper Name",
    tags=["SurfTimer", "ck_maptier"],
)
def updateMapperName(
    request: Request,
    response: Response,
    mapper: str,
    mapname: int,
):
    """```c
    char[] sql_updateMapperName = ....
    ```"""
    tic = time.perf_counter()
    append_request_log(request)

    xquery = insertQuery(surftimer.queries.sql_updateMapperName.format(mapper, mapname))

    if xquery < 1:
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"inserted": xquery, "xtime": time.perf_counter() - tic},
        )

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")
    # output = ResponseInsertQuery(xquery)

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}
