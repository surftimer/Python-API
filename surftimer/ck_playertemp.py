from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from sql import selectQuery, insertQuery
from globals import append_request_log, get_cache, set_cache
from pydantic import BaseModel
import time, json, surftimer.queries


router = APIRouter()


class PlayerTemp(BaseModel):
    cords1: str
    cords2: str
    cords3: str
    angle1: str
    angle2: str
    angle3: str
    runtimeTmp: str
    steamid: str
    mapname: str
    EncTickrate: str
    Stage: int
    zonegroup: int


# ck_playertemp
@router.post(
    "/surftimer/insertPlayerTmp",
    name="Insert Player Temp",
    tags=["ck_playertemp"],
)
async def insertPlayerTmp(request: Request, response: Response, data: PlayerTemp):
    """```c
    char[] sql_insertPlayerTmp = ....
    ```"""
    tic = time.perf_counter()
    append_request_log(request)

    xquery = insertQuery(
        surftimer.queries.sql_insertPlayerTmp.format(
            data.cords1,
            data.cords2,
            data.cords3,
            data.angle1,
            data.angle2,
            data.angle3,
            data.runtimeTmp,
            data.steamid,
            data.mapname,
            data.EncTickrate,
            data.Stage,
            data.zonegroup,
        )
    )

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
    "/surftimer/updatePlayerTmp",
    name="Update Player Temp",
    tags=["ck_playertemp"],
)
async def updatePlayerTmp(request: Request, response: Response, data: PlayerTemp):
    """```c
    char[] sql_updatePlayerOptions = ....
    ```"""
    tic = time.perf_counter()
    append_request_log(request)

    xquery = insertQuery(
        surftimer.queries.sql_updatePlayerTmp.format(
            data.cords1,
            data.cords2,
            data.cords3,
            data.angle1,
            data.angle2,
            data.angle3,
            data.runtimeTmp,
            data.steamid,
            data.mapname,
            data.EncTickrate,
            data.Stage,
            data.zonegroup,
        )
    )

    if xquery < 1:
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"updated": xquery, "xtime": time.perf_counter() - tic},
        )

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")
    # output = ResponseInsertQuery(xquery)

    return {"updated": xquery, "xtime": time.perf_counter() - tic}


@router.delete(
    "/surftimer/deletePlayerTmp",
    name="Delete Player Temp",
    tags=["ck_playertemp"],
)
async def deletePlayerTmp(
    request: Request,
    response: Response,
    steamid32: str,
):
    """```char sql_deletePlayerTmp[] = ....```"""
    tic = time.perf_counter()

    append_request_log(request)

    xquery = insertQuery(surftimer.queries.sql_deletePlayerTmp.format(steamid32))

    if xquery <= 0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"xtime": time.perf_counter() - tic},
        )

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}


@router.get(
    "/surftimer/selectPlayerTmp",
    name="Get Player Temp",
    tags=["ck_playertemp"],
)
async def selectPlayerTmp(
    request: Request, response: Response, steamid32: str, mapname: str
):
    """`char[] sql_selectPlayerTmp = ....`"""
    tic = time.perf_counter()
    append_request_log(request)

    # Check if data is cached in Redis
    cache_key = f"selectPlayerTmp:{steamid32}-{mapname}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(
        surftimer.queries.sql_selectPlayerTmp.format(steamid32, mapname)
    )

    if xquery:
        xquery = xquery.pop()
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content=json.loads(cached_data)
        )

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    return xquery