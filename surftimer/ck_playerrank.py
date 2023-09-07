from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from sql import selectQuery, insertQuery
from globals import get_cache, set_cache
from pydantic import BaseModel
import time, json
import surftimer.queries


class UpdatePlayerPoints(BaseModel):
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
        response.body = json.dumps(content_data).encode('utf-8')
        response.headers['content-type'] = 'application/json'
        response.status_code = status.HTTP_304_NOT_MODIFIED
        response.headers['content-type'] = 'application/json'
        return response

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    response.body = json.dumps(content_data).encode('utf-8')
    response.status_code = status.HTTP_201_CREATED
    response.headers['content-type'] = 'application/json'
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
    xquery = insertQuery(sql)

    content_data = {"updated": xquery, "xtime": time.perf_counter() - tic}
    if xquery < 1:
        response.body = json.dumps(content_data).encode('utf-8')
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
    xquery = insertQuery(sql)

    content_data = {"updated": xquery, "xtime": time.perf_counter() - tic}
    if xquery < 1:
        response.body = json.dumps(content_data).encode('utf-8')
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
        response.body = json.dumps(content_data).encode('utf-8')
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
    "/surftimer/selectPlayerName",
    name="Select Player Name",
    tags=["ck_playerrank"],
)
async def selectPlayerName(
    request: Request,
    response: Response,
    steamid32: str,
):
    """`char[] sql_selectPlayerName = ....`"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectPlayerName:{steamid32}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(surftimer.queries.sql_selectPlayerName.format(steamid32))

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        xquery = {"steamid32": steamid32}

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
        response.body = json.dumps(content_data).encode('utf-8')
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
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(surftimer.queries.sql_selectTopPlayers.format(style))

    if xquery:
        xquery = xquery
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        xquery = {"style": style}

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
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(
        surftimer.queries.sql_selectRankedPlayersRank.format(style, steamid32, style)
    )

    if xquery:
        xquery = xquery
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        xquery = {"steamid32": steamid32}
        xquery["xtime"] = time.perf_counter() - tic

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
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(surftimer.queries.sql_selectRankedPlayers)
    # xquery = []

    if len(xquery) > 0:
        xquery = xquery
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        xquery = {}
        xquery["xtime"] = time.perf_counter() - tic

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
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(surftimer.queries.sql_CountRankedPlayers.format(style))

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        xquery = {"style": style}

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
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )
    xquery = selectQuery(surftimer.queries.sql_CountRankedPlayers2.format(style))

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        xquery = {"style": style}

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
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(
        surftimer.queries.sql_selectPlayerProfile.format(steamid32, style)
    )

    if xquery:
        xquery = xquery.pop()
    else:
        xquery = {"steamid32": steamid32, "style": style}
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=xquery)

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
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(
        surftimer.queries.sql_selectPlayerRankUnknown.format(name)
    )

    if xquery:
        xquery = xquery.pop()
    else:
        xquery = {"name": name}
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=xquery)

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery
