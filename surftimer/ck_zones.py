from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from sql import selectQuery, insertQuery
from globals import get_cache, set_cache
from pydantic import BaseModel
from decimal import Decimal
import simplejson as json
import time, surftimer.queries


class ZonesModel(BaseModel):
    """Body for adding or updating **zones** entry"""

    mapname: str
    zoneid: int
    zonetype: int
    zonetypeid: int
    pointa_x: Decimal
    pointa_y: Decimal
    pointa_z: Decimal
    pointb_x: Decimal
    pointb_y: Decimal
    pointb_z: Decimal
    vis: int
    team: int
    zonegroup: int
    zonename: str = None
    hookname: str
    targetname: str
    onejumplimit: int
    prespeed: int


router = APIRouter()


@router.post(
    "/surftimer/insertZones",
    name="Add Zone",
    tags=["ck_zones"],
)
async def insertZones(
    request: Request,
    response: Response,
    data: ZonesModel,
):
    """```c
    char[] sql_insertZones = ....
    ```"""
    tic = time.perf_counter()

    xquery = insertQuery(
        surftimer.queries.sql_insertZones.format(
            data.mapname,
            data.zoneid,
            data.zonetype,
            data.zonetypeid,
            data.pointa_x,
            data.pointa_y,
            data.pointa_z,
            data.pointb_x,
            data.pointb_y,
            data.pointb_z,
            data.vis,
            data.team,
            data.zonegroup,
            data.zonename,
            data.hookname,
            data.targetname,
            data.onejumplimit,
            data.prespeed,
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
    "/surftimer/updateSpawnLocations2",
    name="Update Spawn Location",
    tags=["ck_zones"],
)
async def updateSpawnLocations(
    request: Request,
    response: Response,
    data: ZonesModel,
):
    """```c
    char[] sql_updateZone = ....
    ```\n"""
    tic = time.perf_counter()

    xquery = insertQuery(
        surftimer.queries.sql_updateZone.format(
            data.zonetype,
            data.zonetypeid,
            data.pointa_x,
            data.pointa_y,
            data.pointa_z,
            data.pointb_x,
            data.pointb_y,
            data.pointb_z,
            data.vis,
            data.team,
            data.onejumplimit,
            data.prespeed,
            data.hookname,
            data.targetname,
            data.zonegroup,
            data.zoneid,
            data.mapname,
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


@router.get(
    "/surftimer/selectzoneTypeIds",
    name="Get Zone Type IDs",
    tags=["ck_zones"],
)
async def selectzoneTypeIds(
    request: Request,
    response: Response,
    mapname: str,
    zonetype: int,
    zonegroup: int,
):
    """`char[] sql_selectzoneTypeIds = ....`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectzoneTypeIds:{mapname}-{zonetype}-{zonegroup}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_selectzoneTypeIds.format(mapname, zonetype, zonegroup)
    )

    if xquery:
        xquery = xquery.pop()
    else:
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    # if len(xquery) <= 0:
    #     response.headers["content-type"] = "application/json"
    #     response.status_code = status.HTTP_204_NO_CONTENT
    #     return response

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    return xquery


@router.get(
    "/surftimer/selectMapZones",
    name="Get Map Zones",
    tags=["ck_zones"],
)
async def selectMapZones(
    request: Request,
    response: Response,
    mapname: str,
):
    """`char[] sql_selectMapZones = ....`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectMapZones:{mapname}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(surftimer.queries.sql_selectMapZones.format(mapname))

    # if len(xquery) <= 0:
    #     xquery = xquery.pop()
    # else:
    #     response.headers["content-type"] = "application/json"
    #     response.status_code = status.HTTP_204_NO_CONTENT
    #     return response

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
    "/surftimer/selectTotalBonusCount",
    name="Get Total Bonuses",
    tags=["ck_zones"],
)
async def selectTotalBonusCount(
    request: Request,
    response: Response,
):
    """`char[] sql_selectTotalBonusCount = ....`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectMapZones:"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(surftimer.queries.sql_selectTotalBonusCount)

    # if len(xquery) <= 0:
    #     xquery = xquery.pop()
    # else:
    #     response.headers["content-type"] = "application/json"
    #     response.status_code = status.HTTP_204_NO_CONTENT
    #     return response

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
    "/surftimer/selectZoneIds",
    name="Get Zone IDs",
    tags=["ck_zones"],
)
async def selectZoneIds(
    request: Request,
    response: Response,
    mapname: str,
):
    """`char[] sql_selectZoneIds = ....`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectZoneIds:{mapname}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(surftimer.queries.sql_selectZoneIds.format(mapname))

    # if xquery:
    #     xquery = xquery.pop()
    # else:
    #     response.headers["content-type"] = "application/json"
    #     response.status_code = status.HTTP_204_NO_CONTENT
    #     return response

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
    "/surftimer/selectBonusesInMap",
    name="Get Bonuses In Map",
    tags=["ck_zones"],
)
async def selectBonusesInMap(
    request: Request,
    response: Response,
    mapname: str,
):
    """`char[] sql_selectBonusesInMap = ....`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectBonusesInMap:{mapname}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(surftimer.queries.sql_selectBonusesInMap.format(mapname))

    # if xquery:
    #     xquery = xquery.pop()
    # else:
    #     response.headers["content-type"] = "application/json"
    #     response.status_code = status.HTTP_204_NO_CONTENT
    #     return response

    if len(xquery) <= 0:
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    return xquery


@router.delete(
    "/surftimer/deleteMapZones",
    name="Delete Map Zones",
    tags=["ck_zones"],
)
async def deleteMapZones(
    request: Request,
    response: Response,
    mapname: str,
):
    """```char sql_deleteMapZones[] = ....```"""
    tic = time.perf_counter()

    xquery = insertQuery(surftimer.queries.sql_deleteMapZones.format(mapname))

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


@router.delete(
    "/surftimer/deleteZone",
    name="Delete Specific Zone",
    tags=["ck_zones"],
)
async def deleteZone(
    request: Request,
    response: Response,
    mapname: str,
    zoneid: int,
):
    """```char sql_deleteZone[] = ....```"""
    tic = time.perf_counter()

    xquery = insertQuery(surftimer.queries.sql_deleteZone.format(mapname, zoneid))

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


@router.delete(
    "/surftimer/deleteZonesInGroup",
    name="Delete Specific Zonegroup",
    tags=["ck_zones"],
)
async def deleteZonesInGroup(
    request: Request,
    response: Response,
    mapname: str,
    zonegroup: int,
):
    """```char sql_deleteZonesInGroup[] = ....```"""
    tic = time.perf_counter()

    xquery = insertQuery(surftimer.queries.sql_deleteZonesInGroup.format(mapname, zonegroup))

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


@router.put(
    "/surftimer/setZoneNames",
    name="Set Zone Name",
    tags=["ck_zones"],
)
async def setZoneNames(
    request: Request,
    response: Response,
    zonename: str,
    mapname: str,
    zonegroup: int,
):
    """```c
    char[] sql_setZoneNames = ....
    ```\n"""
    tic = time.perf_counter()

    xquery = insertQuery(
        surftimer.queries.sql_setZoneNames.format(zonename, mapname, zonegroup
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

