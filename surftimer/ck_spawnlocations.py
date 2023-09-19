from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from sql import selectQuery, insertQuery
from globals import get_cache, set_cache
from pydantic import BaseModel
from decimal import Decimal
import simplejson as json
import time, surftimer.queries


class SpawnLocationsModel(BaseModel):
    """Body for adding or updating **spawnlocations** entry"""

    mapname: str
    pos_x: Decimal
    pos_y: Decimal
    pos_z: Decimal
    ang_x: Decimal
    ang_y: Decimal
    ang_z: Decimal
    vel_x: Decimal
    vel_y: Decimal
    vel_z: Decimal
    zonegroup: int
    teleside: int


router = APIRouter()


@router.get(
    "/surftimer/selectSpawnLocations",
    name="Get Spawn Locations",
    tags=["ck_spawnlocations"],
)
async def selectSpawnLocations(
    request: Request,
    response: Response,
    mapname: str,
):
    """`char[] sql_selectSpawnLocations = ....`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectSpawnLocations:{mapname}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(surftimer.queries.sql_selectSpawnLocations.format(mapname))

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
    "/surftimer/getSpawnPoints",
    name="Get Spawn Points - can merge this ig?",
    tags=["ck_spawnlocations", "strays"],
)
async def getSpawnPoints(
    request: Request,
    response: Response,
    mapname: str,
):
    """`char[] sql_stray_getSpawnPoints = ....`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"getSpawnPoints:{mapname}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(surftimer.queries.sql_stray_getSpawnPoints.format(mapname))

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
    "/surftimer/insertSpawnLocations",
    name="Add Spawn Location",
    tags=["ck_spawnlocations"],
)
async def insertSpawnLocations(
    request: Request,
    response: Response,
    data: SpawnLocationsModel,
):
    """```c
    char[] sql_insertSpawnLocations = ....
    ```"""
    tic = time.perf_counter()

    xquery = insertQuery(
        surftimer.queries.sql_insertSpawnLocations.format(
            data.mapname,
            data.pos_x,
            data.pos_y,
            data.pos_z,
            data.ang_x,
            data.ang_y,
            data.ang_z,
            data.vel_x,
            data.vel_y,
            data.vel_z,
            data.zonegroup,
            data.teleside,
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
    "/surftimer/updateSpawnLocations",
    name="Update Spawn Location",
    tags=["ck_spawnlocations"],
)
async def updateSpawnLocations(
    request: Request,
    response: Response,
    data: SpawnLocationsModel,
):
    """```c
    char[] sql_updateSpawnLocations = ....
    ```\n"""
    tic = time.perf_counter()

    xquery = insertQuery(
        surftimer.queries.sql_updateSpawnLocations.format(
            data.pos_x,
            data.pos_y,
            data.pos_z,
            data.ang_x,
            data.ang_y,
            data.ang_z,
            data.vel_x,
            data.vel_y,
            data.vel_z,
            data.mapname,
            data.zonegroup,
            data.teleside,
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


@router.delete(
    "/surftimer/deleteSpawnLocations",
    name="Delete Spawn Locations",
    tags=["ck_spawnlocations"],
)
async def deleteCheckpoints(
    request: Request,
    response: Response,
    mapname: str,
    zonegroup: int,
    teleside: int,
):
    """```char sql_deleteSpawnLocations[] = ....```"""
    tic = time.perf_counter()

    xquery = insertQuery(
        surftimer.queries.sql_deleteSpawnLocations.format(mapname, zonegroup, teleside)
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
