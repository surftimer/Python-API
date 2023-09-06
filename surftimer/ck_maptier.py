from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from sql import selectQuery, insertQuery
from globals import get_cache, set_cache
import time, json
import surftimer.queries
from pydantic import BaseModel

router = APIRouter()

class MaptierModel(BaseModel):
    mapname: str
    tier: int = None
    mappername: str = None

# ck_maptier
@router.get(
    "/surftimer/selectMapTier",
    name="Get Map Tier",
    tags=["ck_maptier"],
)
async def selectMapTier(
    request: Request,
    response: Response,
    mapname: str,
):
    """`char[] sql_selectMapTier = ....`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectMapTier:{mapname}"
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
    tags=["ck_maptier"],
)
async def insertMapTier(
    request: Request,
    response: Response,
    data: MaptierModel,
):
    """```c
    char[] sql_insertmaptier = ....
    ```"""
    tic = time.perf_counter()

    xquery = insertQuery(surftimer.queries.sql_insertmaptier.format(data.mapname, data.tier))
    
    content_data = {"inserted": xquery, "xtime": time.perf_counter() - tic}
    if xquery < 1:
        response.body = json.dumps(content_data).encode('utf-8')
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return response

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")
    
    response.body = json.dumps(content_data).encode('utf-8')
    response.status_code = status.HTTP_201_CREATED
    return response


@router.put(
    "/surftimer/updateMapTier",
    name="Update Map Tier",
    tags=["ck_maptier"],
)
async def updateMapTier(
    request: Request,
    response: Response,
    data: MaptierModel,
):
    """```c
    char[] sql_updatemaptier = ....
    ```"""
    tic = time.perf_counter()

    xquery = insertQuery(surftimer.queries.sql_updatemaptier.format(data.tier, data.mapname))

    content_data = {"updated": xquery, "xtime": time.perf_counter() - tic}
    if xquery < 1:
        response.body = json.dumps(content_data).encode('utf-8')
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return response

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    response.body = json.dumps(content_data).encode('utf-8')
    response.status_code = status.HTTP_200_OK
    return response

@router.put(
    "/surftimer/updateMapperName",
    name="Update Mapper Name",
    tags=["ck_maptier"],
)
async def updateMapperName(
    request: Request,
    response: Response,
    data: MaptierModel,
):
    """```c
    char[] sql_updateMapperName = ....
    ```"""
    tic = time.perf_counter()

    xquery = insertQuery(surftimer.queries.sql_updateMapperName.format(data.mappername, data.mapname))

    content_data = {"updated": xquery, "xtime": time.perf_counter() - tic}
    if xquery < 1:
        response.body = json.dumps(content_data).encode('utf-8')
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return response

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    response.body = json.dumps(content_data).encode('utf-8')
    response.status_code = status.HTTP_200_OK
    return response