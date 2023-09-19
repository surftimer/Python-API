from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from sql import selectQuery, insertQuery, insert_escaped_query
from globals import get_cache, set_cache
from pydantic import BaseModel
import time, json
import surftimer.queries


class UpdatePlayerPoints(BaseModel):
    """Body for updating **player rank** entry"""

    name: str
    points: int
    wrpoints: int
    wrbpoints: int
    wrcppoints: int
    top10points: int
    groupspoints: int
    mappoints: int
    bonuspoints: int
    finishedmapspro: int
    finishedbonuses: int
    finishedstages: int
    wrs: int
    wrbs: int
    wrcps: int
    top10s: int
    groups: int
    country: str = None
    countryCode: str = None
    continentCode: str = None
    steamid32: str
    style: int


class InsertPlayerModel(BaseModel):
    """Body for adding a **player rank** entry"""

    steamid32: str
    steamid64: int
    name: str
    country: str
    countryCode: str
    continentCode: str
    joined: int
    style: int


router = APIRouter()


# ck_playerrank
@router.post(
    "/surftimer/insertPlayerRank",
    name="Add Player Rank",
    tags=["ck_playerrank"],
)
async def insertPlayerRank(
    request: Request,
    response: Response,
    data: InsertPlayerModel,
):
    """```char sql_insertPlayerRank[] = ....```"""
    tic = time.perf_counter()

    sql = surftimer.queries.sql_insertPlayerRank.format(
        data.steamid32,
        data.steamid64,
        data.name,
        data.country,
        data.countryCode,
        data.continentCode,
        data.joined,
        data.style,
    )
    xquery = insertQuery(sql)

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
    response.headers["content-type"] = "application/json"
    return response


@router.put(
    "/surftimer/updatePlayerRankPoints",
    name="Update Player Rank Points 1",
    tags=["ck_playerrank"],
)
async def updatePlayerRankPoints(
    request: Request,
    response: Response,
    data: UpdatePlayerPoints,
):
    """```char sql_updatePlayerRankPoints[] = ....```"""
    tic = time.perf_counter()

    sql = surftimer.queries.sql_updatePlayerRankPoints.format(
        data.name,
        data.points,
        data.wrpoints,
        data.wrbpoints,
        data.wrcppoints,
        data.top10points,
        data.groupspoints,
        data.mappoints,
        data.bonuspoints,
        data.finishedmapspro,
        data.finishedbonuses,
        data.finishedstages,
        data.wrs,
        data.wrbs,
        data.wrcps,
        data.top10s,
        data.groups,
        data.steamid32,
        data.style,
    )

    xquery = insert_escaped_query(sql)

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
    "/surftimer/updatePlayerRankPoints2",
    name="Update Player Rank Points 2",
    tags=["ck_playerrank"],
)
async def updatePlayerRankPoints2(
    request: Request,
    response: Response,
    data: UpdatePlayerPoints,
):
    """```char sql_updatePlayerRankPoints2[] = ....```"""
    tic = time.perf_counter()

    sql = surftimer.queries.sql_updatePlayerRankPoints2.format(
        data.name,
        data.points,
        data.wrpoints,
        data.wrbpoints,
        data.wrcppoints,
        data.top10points,
        data.groupspoints,
        data.mappoints,
        data.bonuspoints,
        data.finishedmapspro,
        data.finishedbonuses,
        data.finishedstages,
        data.wrs,
        data.wrbs,
        data.wrcps,
        data.top10s,
        data.groups,
        data.country,
        data.countryCode,
        data.continentCode,
        data.steamid32,
        data.style,
    )
    xquery = insert_escaped_query(sql)

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
    "/surftimer/updatePlayerRank",
    name="Update Player Rank",
    tags=["ck_playerrank"],
)
async def updatePlayerRank(
    request: Request,
    response: Response,
    finishedmaps: str,
    finishedmapspro: str,
    steamid32: str,
    style: str,
):
    """```char sql_updatePlayerRank[] = ....```"""
    tic = time.perf_counter()

    sql = surftimer.queries.sql_updatePlayerRank.format(
        finishedmaps,
        finishedmapspro,
        steamid32,
        style,
    )
    xquery = insertQuery(sql)

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
    "/surftimer/selectPlayerName",
    name="Select Player Name",
    tags=["ck_playerrank"],
    deprecated=True,
)
async def selectPlayerName(
    request: Request,
    response: Response,
    steamid32: str,
):
    """`char[] sql_selectPlayerName = ....`. \n
    Merged with `sql_stray_point_calc_playerRankName`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectPlayerName:{steamid32}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(surftimer.queries.sql_selectPlayerName.format(steamid32))

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")
    xquery["xtime"] = time.perf_counter() - tic

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.put(
    "/surftimer/updateLastSeenMySQL",
    name="Update Last Seen",
    tags=["ck_playerrank"],
)
async def updateLastSeen(
    request: Request,
    response: Response,
    steamid32: str,
):
    """```char sql_UpdateLastSeenMySQL[] = ....```"""
    tic = time.perf_counter()

    sql = surftimer.queries.sql_UpdateLastSeenMySQL.format(steamid32)
    xquery = insertQuery(sql)

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
    "/surftimer/selectTopPlayers",
    name="Select Top Players",
    tags=["ck_playerrank"],
)
async def selectTopPlayers(
    request: Request,
    response: Response,
    style: int,
):
    """`char[] sql_selectTopPlayers = ....`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectTopPlayers:{style}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(surftimer.queries.sql_selectTopPlayers.format(style))

    if xquery:
        xquery = xquery
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/selectRankedPlayersRank",
    name="Select Ranked Players Rank",
    tags=["ck_playerrank"],
)
async def selectRankedPlayersRank(
    request: Request,
    response: Response,
    style: int,
    steamid32: str,
):
    """`char[] sql_selectRankedPlayersRank = ....`\n
    Done 2/4 query executions in ST code for this T_T"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectTopPlayers:{style}_{steamid32}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_selectRankedPlayersRank.format(style, steamid32, style)
    )

    if xquery:
        xquery = xquery
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")
    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/selectRankedPlayers",
    name="Select Ranked Players",
    tags=["ck_playerrank"],
)
async def selectRankedPlayers(request: Request, response: Response):
    """`char[] sql_selectRankedPlayers = ....`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectRankedPlayers"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(surftimer.queries.sql_selectRankedPlayers)
    # xquery = []

    if len(xquery) > 0:
        xquery = xquery
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/selectRankedPlayer",
    name="Select Ranked Players",
    tags=["ck_playerrank"],
)
async def selectRankedPlayer(request: Request, response: Response, steamid32: str):
    """`char[] sql_selectRankedPlayer = ....`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectRankedPlayer"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(surftimer.queries.sql_selectRankedPlayer.format(steamid32))
    # xquery = []

    if len(xquery) > 0:
        xquery = xquery
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/countRankedPlayers",
    name="Count Ranked Players",
    tags=["ck_playerrank"],
)
async def countRankedPlayers(
    request: Request,
    response: Response,
    style: int,
):
    """This is technically not ***Ranked*** players, it's all `steamid` count in `ck_playerrank`\n
    `char[] sql_CountRankedPlayers = ....`"""
    tic = time.perf_counter()

    cache_key = f"countRankedPlayers:{style}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(surftimer.queries.sql_CountRankedPlayers.format(style))

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)
    return xquery


@router.get(
    "/surftimer/countRankedPlayers2",
    name="Count Ranked Players 2",
    tags=["ck_playerrank"],
)
async def countRankedPlayers2(
    request: Request,
    response: Response,
    style: int,
):
    """This ***DOES*** check for player points being higher than 0\n
    `char[] sql_CountRankedPlayers2 = ....`"""
    tic = time.perf_counter()

    cache_key = f"countRankedPlayers2:{style}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(surftimer.queries.sql_CountRankedPlayers2.format(style))

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/selectPlayerProfile",
    name="Select Player Profile",
    tags=["ck_playerrank"],
)
async def selectPlayerProfile(
    request: Request,
    response: Response,
    steamid32: str,
    style: int,
):
    """`char[] sql_selectPlayerProfile = ....`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectTopPlayers:{steamid32}_{style}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_selectPlayerProfile.format(steamid32, style)
    )

    if xquery:
        xquery = xquery.pop()
    else:
        # response.body = json.dumps(content_data).encode('utf-8')
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/selectUnknownPlayerProfile",
    name="Select Unknown Player Profile",
    tags=["ck_playerrank"],
)
async def selectUnknownPlayerProfile(
    request: Request,
    response: Response,
    name: str,
):
    """`SELECT steamid, name, points FROM ck_playerrank WHERE name LIKE '%c%s%c' ORDER BY points DESC LIMIT 0, 1;`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectUnknownPlayerProfile:{name}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(surftimer.queries.sql_selectPlayerRankUnknown.format(name))

    if xquery:
        xquery = xquery.pop()
    else:
        # response.body = json.dumps(content_data).encode('utf-8')
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.put(
    "/surftimer/updatePlayerConnections",
    name="Update Player Connections",
    tags=["ck_playerrank"],
)
async def updatePlayerConnections(
    request: Request,
    response: Response,
    steamid32: str,
):
    """```UPDATE ck_playerrank SET connections = connections + 1 WHERE steamid = '%s';```"""
    tic = time.perf_counter()

    sql = surftimer.queries.sql_updatePlayerConnections.format(steamid32)
    xquery = insertQuery(sql)

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
    "/surftimer/deleteWipePlayerRank",
    name="Wipe Player Rank",
    tags=["ck_playerrank", "strays", "Wipe"],
)
def deleteWipePlayerRank(
    request: Request,
    response: Response,
    steamid32: str,
):
    """```char sql_stray_deleteWipePlayerRank[] = ....```\n
    Wipes all `playerrank` entries for player"""
    tic = time.perf_counter()

    xquery = insertQuery(
        surftimer.queries.sql_stray_deleteWipePlayerRank.format(steamid32)
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


@router.get(
    "/surftimer/point_calc_playerRankName",
    name="Select Player Name",
    tags=["ck_playerrank", "strays", "Points Calculation"],
)
async def point_calc_playerRankName(
    request: Request,
    response: Response,
    steamid32: str,
    style: int,
):
    """```char sql_stray_point_calc_playerRankName[] = ....```"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"point_calc_playerRankName:{steamid32}-{style}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_stray_point_calc_playerRankName.format(steamid32, style)
    )

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.delete(
    "/surftimer/cleanupPlayerRank",
    name="Cleanup Player Rank",
    tags=["ck_playerrank", "strays"],
)
def cleanupPlayerRank(
    request: Request,
    response: Response,
):
    """```char sql_stray_cleanupPlayerRank[] = ....```\n
    Deletes all `playerrank` entries for player with no points"""
    tic = time.perf_counter()

    xquery = insertQuery(surftimer.queries.sql_stray_cleanupPlayerRank.format())

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


@router.get(
    "/surftimer/specificCountryRank",
    name="Country Rank",
    tags=["ck_playerrank", "strays"],
)
async def specificCountryRank(
    request: Request,
    response: Response,
    country: str,
    style: int,
):
    """`char[] sql_stray_specificCountryRank = ....`"""
    tic = time.perf_counter()

    cache_key = f"specificCountryRank:{country}-{style}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_stray_specificCountryRank.format(country, style)
    )

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/getPlayerPointsByName",
    name="Player Points by Name",
    tags=["ck_playerrank", "strays"],
)
async def getPlayerPointsByName(
    request: Request,
    response: Response,
    name: str,
    style: int,
):
    """`char[] sql_stray_getPlayerPointsByName = ....`"""
    tic = time.perf_counter()

    cache_key = f"getPlayerPointsByName:{name}-{style}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_stray_getPlayerPointsByName.format(name, style)
    )

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/continentPlayerRankByName",
    name="Continent Player Rank",
    tags=["ck_playerrank", "strays"],
)
async def continentPlayerRankByName(
    request: Request,
    response: Response,
    name: str,
):
    """`char[] sql_stray_continentPlayerRankByName = ....`"""
    tic = time.perf_counter()

    cache_key = f"countryRankGetPlayerByName:{name}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_stray_continentPlayerRankByName.format(name)
    )

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/getPlayerCountryRank",
    name="Player Country Rank",
    tags=["ck_playerrank", "strays"],
)
async def getPlayerCountryRank(
    request: Request,
    response: Response,
    country: str,
    style: int,
    points: int,
):
    """`char[] sql_stray_getPlayerCountryRank = ....`"""
    tic = time.perf_counter()

    cache_key = f"getPlayerCountryRank:{country}-{style}-{points}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_stray_getPlayerCountryRank.format(country, style, points)
    )

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/getPlayerCountryByName",
    name="Player Country by Name",
    tags=["ck_playerrank", "strays"],
)
async def getPlayerCountryByName(
    request: Request,
    response: Response,
    name: str,
    style: int,
):
    """`char[] sql_stray_countryRankPlayerCountryRankByName = ....`"""
    tic = time.perf_counter()

    cache_key = f"getPlayerCountry:{name}-{style}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_stray_countryRankPlayerCountryRankByName.format(
            name, style
        )
    )

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/countryTop",
    name="Country Top 100",
    tags=["ck_playerrank", "strays"],
)
async def countryTop(
    request: Request,
    response: Response,
    country: str,
    style: int,
):
    """`char[] sql_stray_countryTop = ....`"""
    tic = time.perf_counter()

    cache_key = f"getPlayerCountryRank:{country}-{style}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(surftimer.queries.sql_stray_countryTop.format(country, style))

    if len(xquery) <= 0:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/countryTopAllCountries",
    name="All Countries in Top",
    tags=["ck_playerrank", "strays"],
)
async def countryTopAllCountries(
    request: Request,
    response: Response,
    style: int,
):
    """`char[] sql_stray_countryTopAllCountries = ....`"""
    tic = time.perf_counter()

    cache_key = f"countryTopAllCountries:{style}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_stray_countryTopAllCountries.format(style)
    )

    if len(xquery) <= 0:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/specificContinentRank",
    name="Continent Rank",
    tags=["ck_playerrank", "strays"],
)
async def specificContinentRank(
    request: Request,
    response: Response,
    continentCode: str,
    style: int,
):
    """`char[] sql_stray_specificContinentRank = ....`"""
    tic = time.perf_counter()

    cache_key = f"specificContinentRank:{style}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_stray_specificContinentRank.format(continentCode, style)
    )

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/continentPlayerPoints",
    name="Continent Player Points",
    tags=["ck_playerrank", "strays"],
    deprecated=True,
)
async def continentPlayerPoints(
    request: Request,
    response: Response,
    continentCode: str,
    style: int,
):
    """`char[] sql_stray_continentPlayerPoints = ....`\n
    same as `/surftimer/getPlayerPointsByName`"""
    tic = time.perf_counter()

    cache_key = f"continentPlayerPoints:{style}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_stray_continentPlayerPoints.format(continentCode, style)
    )

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/continentPlayerRank",
    name="Player Continent Rank",
    tags=["ck_playerrank", "strays"],
)
async def continentPlayerRank(
    request: Request,
    response: Response,
    continentCode: str,
    style: int,
    points: int,
):
    """`char[] sql_stray_continentPlayerRank = ....`"""
    tic = time.perf_counter()

    cache_key = f"continentPlayerRank:{continentCode}-{style}-{points}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_stray_continentPlayerRank.format(
            continentCode, style, points
        )
    )

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/continentGetPlayerContinentByName",
    name="Player Continent by Name",
    tags=["ck_playerrank", "strays"],
)
async def continentGetPlayerContinentByName(
    request: Request,
    response: Response,
    name: str,
    style: int,
):
    """`char[] sql_stray_continentGetPlayerContinentByName = ....`"""
    tic = time.perf_counter()

    cache_key = f"continentGetPlayerContinentByName:{name}-{style}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_stray_continentGetPlayerContinentByName.format(
            name, style
        )
    )

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/continentTop",
    name="Continent Top",
    tags=["ck_playerrank", "strays"],
)
async def continentTop(
    request: Request,
    response: Response,
    continentCode: str,
    style: int,
):
    """`char[] sql_stray_continentTop = ....`"""
    tic = time.perf_counter()

    cache_key = f"continentTop:{continentCode}-{style}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_stray_continentTop.format(continentCode, style)
    )

    if len(xquery) <= 0:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/continentNames",
    name="All Continent Names",
    tags=["ck_playerrank", "strays"],
)
async def continentNames(
    request: Request,
    response: Response,
    style: int,
):
    """`char[] sql_stray_continentNames = ....`"""
    tic = time.perf_counter()

    cache_key = f"continentNames:{style}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(surftimer.queries.sql_stray_continentNames.format(style))

    if len(xquery) <= 0:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/viewPlayerRank",
    name="Player Rank",
    tags=["ck_playerrank", "strays"],
)
async def viewPlayerRank(
    request: Request,
    response: Response,
    style: int,
    steamid32: str,
):
    """`char[] sql_stray_viewPlayerRank = ....`"""
    tic = time.perf_counter()

    cache_key = f"viewPlayerRank:{style}-{steamid32}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_stray_viewPlayerRank.format(style, steamid32, style)
    )

    if len(xquery) <= 0:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/getNextRankPoints",
    name="Player Points to Next Rank",
    tags=["ck_playerrank", "strays"],
)
async def getNextRankPoints(
    request: Request,
    response: Response,
    style: int,
    limit: int,
):
    """`char[] sql_stray_getNextRankPoints = ....`"""
    tic = time.perf_counter()

    cache_key = f"getNextRankPoints:{style}-{limit}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_stray_getNextRankPoints.format(style, limit)
    )

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/viewPlayerInfo",
    name="Player Info - TO BE MERGED",
    tags=["ck_playerrank", "strays"],
)
async def viewPlayerInfo(
    request: Request,
    response: Response,
    steamid32: str,
):
    """To be merged with a `SELECT *` *(?)*\n
    `char[] sql_stray_viewPlayerInfo = ....`"""
    tic = time.perf_counter()

    cache_key = f"viewPlayerInfo:{steamid32}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(surftimer.queries.sql_stray_viewPlayerInfo.format(steamid32))

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/rankCommand",
    name="/rank command?",
    tags=["ck_playerrank", "strays"],
)
async def rankCommand(
    request: Request,
    response: Response,
    limit: int,
):
    """`char[] sql_stray_rankCommand = ....`"""
    tic = time.perf_counter()

    cache_key = f"rankCommand:{limit}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(surftimer.queries.sql_stray_rankCommand.format(limit))

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/rankCommandSelf",
    name="Player Points to Next Rank",
    tags=["ck_playerrank", "strays"],
)
async def rankCommandSelf(
    request: Request,
    response: Response,
    steamid32: str,
):
    """`char[] sql_stray_rankCommandSelf = ....`"""
    tic = time.perf_counter()

    cache_key = f"rankCommandSelf:{steamid32}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_stray_rankCommandSelf.format(steamid32)
    )

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/selectPlayerRankUnknown",
    name="Unknown Player Info - TO BE MERGED",
    tags=["ck_playerrank", "strays"],
)
async def selectPlayerRankUnknown(
    request: Request,
    response: Response,
    name: str,
):
    """`char[] sql_stray_selectPlayerRankUnknown = ....`"""
    tic = time.perf_counter()

    cache_key = f"selectPlayerRankUnknown:{name}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_stray_selectPlayerRankUnknown.format(name)
    )

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.get(
    "/surftimer/selectPlayerRankByName",
    name="Unknown Player Info - TO BE MERGED",
    tags=["ck_playerrank", "strays"],
)
async def selectPlayerRankByName(
    request: Request,
    response: Response,
    style: int,
    name: str,
):
    """`char[] sql_stray_playerRankByName = ....`"""
    tic = time.perf_counter()

    cache_key = f"playerRankByName:{style}-{name}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_stray_playerRankByName.format(style, name)
    )

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery
