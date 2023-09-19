from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from sql import selectQuery, insertQuery
from globals import get_cache, set_cache
from pydantic import BaseModel
from decimal import Decimal
import simplejson as json
import time, surftimer.queries


class PersonalRecordModel(BaseModel):
    """Body for adding or updating **prinfo** entry"""

    steamid32: str
    name: str = None
    mapname: str
    runtime: Decimal = None
    zonegroup: int
    PRtimeinzone: int
    PRcomplete: int
    PRattempts: int
    PRstcomplete: int


router = APIRouter()


@router.get(
    "/surftimer/selectPR",
    name="Get Personal Record Info",
    tags=["ck_prinfo"],
)
async def selectPR(
    request: Request,
    response: Response,
    steamid32: str,
    mapname: str,
    zonegroup: int,
):
    """`char[] sql_selectPR = ....`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectPR:{steamid32}-{mapname}-{zonegroup}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_selectPR.format(steamid32, mapname, zonegroup)
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


@router.get(
    "/surftimer/PRinfoByName",
    name="Get Personal Record Info by Name",
    tags=["ck_prinfo", "strays"],
)
async def PRinfoByName(
    request: Request,
    response: Response,
    mapname: str,
    zonegroup: int,
    steamid32: str,
):
    """`char[] sql_stray_PRinfoByName = ....`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"PRinfoByName:{mapname}-{zonegroup}-{steamid32}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_stray_PRinfoByName.format(mapname, zonegroup, steamid32)
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
    "/surftimer/insertPR",
    name="Add Personal Record Info",
    tags=["ck_prinfo"],
)
async def insertPR(
    request: Request,
    response: Response,
    data: PersonalRecordModel,
):
    """```c
    char[] sql_insertReplayCPTicks = ....
    ```"""
    tic = time.perf_counter()

    xquery = insertQuery(
        surftimer.queries.sql_insertPR.format(
            data.steamid32,
            data.name,
            data.mapname,
            data.runtime,
            data.zonegroup,
            data.PRtimeinzone,
            data.PRcomplete,
            data.PRattempts,
            data.PRstcomplete,
        )
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
    "/surftimer/updatePrInfo",
    name="Update Personal Record Info",
    tags=["ck_prinfo"],
)
async def updatePrInfo(
    request: Request,
    response: Response,
    data: PersonalRecordModel,
):
    """```c
    char[] sql_updatePrinfo = ....
    ```\n
    and\n
    ```c
    char[] sql_updatePrinfo_withruntime = ....
    ```\n"""
    tic = time.perf_counter()

    if data.runtime is None:
        xquery = insertQuery(
            surftimer.queries.sql_updatePrinfo.format(
                data.PRtimeinzone,
                data.PRcomplete,
                data.PRattempts,
                data.PRstcomplete,
                data.steamid32,
                data.mapname,
                data.zonegroup,
            )
        )
    else:
        xquery = insertQuery(
            surftimer.queries.sql_updatePrinfo_withruntime.format(
                data.PRtimeinzone,
                data.PRcomplete,
                data.PRattempts,
                data.PRstcomplete,
                data.runtime,
                data.steamid32,
                data.mapname,
                data.zonegroup,
            )
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


@router.put(
    "/surftimer/clearPRruntime",
    name="Clear Personal Record Time",
    tags=["ck_prinfo"],
)
async def clearPRruntime(
    request: Request,
    response: Response,
    steamid32: str,
    mapname: str,
    zonegroup: int,
):
    """```c
    char[] sql_clearPRruntime = ....
    ```\n"""
    tic = time.perf_counter()

    xquery = insertQuery(
        surftimer.queries.sql_clearPRruntime.format(steamid32, mapname, zonegroup)
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
