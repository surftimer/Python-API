from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from sql import selectQuery
from globals import redis_client, config, append_request_log
import time, json
import surftimer.queries

router = APIRouter()



# ck_playerrank
@router.post(
    "surftimer/insertPlayerRank",
    name="Add Player Rank",
    tags=["SurfTimer", "ck_playerrank"],
)
def insertPlayerRank(
    request: Request,
    response: Response,
    steamid32,
    steamid64,
    name,
    country,
    countryCode,
    continentCode,
    joined,
    style,
):
    tic = time.perf_counter()
    append_request_log(request)

    xquery = surftimer.queries.sql_insertPlayerRank.format(
        steamid32,
        steamid64,
        name,
        country,
        countryCode,
        continentCode,
        joined,
        style,
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


@router.post(
    "surftimer/updatePlayerRankPoints",
    name="Update Player Rank Points 1",
    tags=["SurfTimer", "ck_playerrank"],
)
def updatePlayerRankPoints(
    request: Request,
    response: Response,
    name: str,
    points: str,
    wrpoints: int,
    wrbpoints: int,
    wrcppoints: int,
    top10points: int,
    groupspoints: int,
    mappoints: int,
    bonuspoints: int,
    finishedmapspro: str,
    finishedbonuses: int,
    finishedstages: int,
    wrs: int,
    wrbs: int,
    wrcps: int,
    top10s: int,
    groups: int,
    steamid32: str,
    style: int,
):
    tic = time.perf_counter()
    append_request_log(request)

    xquery = surftimer.queries.sql_updatePlayerRankPoints.format(
        name,
        points,
        wrpoints,
        wrbpoints,
        wrcppoints,
        top10points,
        groupspoints,
        mappoints,
        bonuspoints,
        finishedmapspro,
        finishedbonuses,
        finishedstages,
        wrs,
        wrbs,
        wrcps,
        top10s,
        groups,
        steamid32,
        style,
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


@router.post(
    "surftimer/updatePlayerRankPoints2",
    name="Update Player Rank Points 2",
    tags=["SurfTimer", "ck_playerrank"],
)
def updatePlayerRankPoints2(
    request: Request,
    response: Response,
    name: str,
    points: str,
    wrpoints: int,
    wrbpoints: int,
    wrcppoints: int,
    top10points: int,
    groupspoints: int,
    mappoints: int,
    bonuspoints: int,
    finishedmapspro: str,
    finishedbonuses: int,
    finishedstages: int,
    wrs: int,
    wrbs: int,
    wrcps: int,
    top10s: int,
    groups: int,
    country: str,
    countryCode: str,
    continentCode: str,
    steamid32: str,
    style: int,
):
    tic = time.perf_counter()
    append_request_log(request)

    xquery = surftimer.queries.sql_updatePlayerRankPoints2.format(
        name,
        points,
        wrpoints,
        wrbpoints,
        wrcppoints,
        top10points,
        groupspoints,
        mappoints,
        bonuspoints,
        finishedmapspro,
        finishedbonuses,
        finishedstages,
        wrs,
        wrbs,
        wrcps,
        top10s,
        groups,
        country,
        countryCode,
        continentCode,
        steamid32,
        style,
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


@router.post(
    "surftimer/updatePlayerRank",
    name="Update Player Rank Points 2",
    tags=["SurfTimer", "ck_playerrank"],
)
def updatePlayerRank(
    request: Request,
    response: Response,
    finishedmaps: str,
    finishedmapspro: str,
    steamid32: str,
    style: str,
):
    tic = time.perf_counter()
    append_request_log(request)

    xquery = surftimer.queries.sql_updatePlayerRank.format(
        finishedmaps,
        finishedmapspro,
        steamid32,
        style,
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


@router.get(
    "/surftimer/selectPlayerName",
    name="Select Player Name",
    tags=["SurfTimer", "ck_playerrank"],
)
def selectPlayerName(
    request: Request,
    response: Response,
    steamid32: str,
):
    """`char[] sql_selectPlayerName = ....`"""
    tic = time.perf_counter()
    append_request_log(request)

    # Check if data is cached in Redis
    cached_data = redis_client.get(f"selectPlayerName_{steamid32}")
    if cached_data:
        # Return cached data
        # print(json.loads(cached_data))
        print(
            f"[Redis] Loaded 'selectPlayerName_{steamid32}' ({time.perf_counter() - tic:0.4f}s)"
        )
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
    redis_client.set(
        f"selectPlayerName_{steamid32}",
        json.dumps(xquery),
        ex=config["REDIS"]["EXPIRY"],
    )
    return xquery


@router.post(
    "surftimer/updateLastSeenMySQL",
    name="Update Last Seen",
    tags=["SurfTimer", "ck_playerrank"],
)
def updateLastSeen(
    request: Request,
    response: Response,
    steamid32: str,
):
    tic = time.perf_counter()
    append_request_log(request)

    xquery = surftimer.queries.sql_UpdateLastSeenMySQL.format(steamid32)

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


@router.get(
    "/surftimer/selectTopPlayers",
    name="Select Top Players",
    tags=["SurfTimer", "ck_playerrank"],
)
def selectTopPlayers(
    request: Request,
    response: Response,
    style: int,
):
    """`char[] sql_selectTopPlayers = ....`"""
    tic = time.perf_counter()
    append_request_log(request)

    # Check if data is cached in Redis
    cached_data = redis_client.get(f"selectTopPlayers_{style}")
    if cached_data:
        # Return cached data
        # print(json.loads(cached_data))
        print(
            f"[Redis] Loaded 'selectTopPlayers_{style}' ({time.perf_counter() - tic:0.4f}s)"
        )
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
    # xquery["xtime"] = time.perf_counter() - tic

    # Cache the data in Redis
    redis_client.set(
        f"selectTopPlayers_{style}",
        json.dumps(xquery),
        ex=config["REDIS"]["EXPIRY"],
    )
    return xquery


@router.get(
    "/surftimer/selectRankedPlayersRank",
    name="Select Ranked Players Rank",
    tags=["SurfTimer", "ck_playerrank"],
)
def selectRankedPlayersRank(
    request: Request,
    response: Response,
    style: int,
    steamid32: str,
):
    """`char[] sql_selectRankedPlayersRank = ....`"""
    tic = time.perf_counter()
    append_request_log(request)

    # Check if data is cached in Redis
    cached_data = redis_client.get(f"selectTopPlayers_{style}_{steamid32}")
    if cached_data:
        # Return cached data
        # print(json.loads(cached_data))
        print(
            f"[Redis] Loaded 'selectTopPlayers_{style}_{steamid32}' ({time.perf_counter() - tic:0.4f}s)"
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(
        surftimer.queries.sql_selectRankedPlayersRank.format(style, steamid32, style)
    )
    print(surftimer.queries.sql_selectRankedPlayersRank.format(style, steamid32, style))

    if xquery:
        xquery = xquery
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        xquery = {"steamid32": steamid32}
        xquery["xtime"] = time.perf_counter() - tic

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")
    # Cache the data in Redis
    redis_client.set(
        f"selectTopPlayers_{style}_{steamid32}",
        json.dumps(xquery),
        ex=config["REDIS"]["EXPIRY"],
    )
    return xquery


@router.get(
    "/surftimer/selectRankedPlayers",
    name="Select Ranked Players",
    tags=["SurfTimer", "ck_playerrank"],
)
def selectRankedPlayers(request: Request, response: Response):
    """`char[] sql_selectRankedPlayers = ....`"""
    tic = time.perf_counter()
    append_request_log(request)

    # Check if data is cached in Redis
    cached_data = redis_client.get(f"selectRankedPlayers")
    if cached_data:
        # Return cached data
        # print(json.loads(cached_data))
        print(
            f"[Redis] Loaded 'selectRankedPlayers' ({time.perf_counter() - tic:0.4f}s)"
        )
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
    redis_client.set(
        f"selectRankedPlayers",
        json.dumps(xquery),
        ex=config["REDIS"]["EXPIRY"],
    )
    return xquery


@router.get(
    "/surftimer/countRankedPlayers",
    name="Count Ranked Players",
    tags=["SurfTimer", "ck_playerrank"],
)
def countRankedPlayers(
    request: Request,
    response: Response,
    style: int,
):
    """This is technically not ***Ranked*** players, it's all `steamid` count in `ck_playerrank`\n
    `char[] sql_CountRankedPlayers = ....`"""
    tic = time.perf_counter()
    append_request_log(request)

    xquery = selectQuery(surftimer.queries.sql_CountRankedPlayers.format(style))

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        xquery = {"style": style}

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")
    xquery["xtime"] = time.perf_counter() - tic
    return xquery


@router.get(
    "/surftimer/countRankedPlayers2",
    name="Count Ranked Players 2",
    tags=["SurfTimer", "ck_playerrank"],
)
def countRankedPlayers2(
    request: Request,
    response: Response,
    style: int,
):
    """This ***DOES*** check for player points being higher than 0\n
    `char[] sql_CountRankedPlayers2 = ....`"""
    tic = time.perf_counter()
    append_request_log(request)

    xquery = selectQuery(surftimer.queries.sql_CountRankedPlayers2.format(style))

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        xquery = {"style": style}

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")
    xquery["xtime"] = time.perf_counter() - tic
    return xquery


@router.get(
    "/surftimer/selectPlayerProfile",
    name="Select Player Profile",
    tags=["SurfTimer", "ck_playerrank"],
)
def selectPlayerProfile(
    request: Request,
    response: Response,
    steamid32: str,
    style: int,
):
    """`char[] sql_selectPlayerProfile = ....`"""
    tic = time.perf_counter()
    append_request_log(request)

    # Check if data is cached in Redis
    cached_data = redis_client.get(f"selectTopPlayers_{steamid32}_{style}")
    if cached_data:
        # Return cached data
        # print(json.loads(cached_data))
        print(
            f"[Redis] Loaded 'selectTopPlayers_{steamid32}_{style}' ({time.perf_counter() - tic:0.4f}s)"
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(
        surftimer.queries.sql_selectPlayerProfile.format(steamid32, style)
    )

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        xquery = {"steamid32": steamid32}

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")
    xquery["xtime"] = time.perf_counter() - tic

    # Cache the data in Redis
    redis_client.set(
        f"selectTopPlayers_{steamid32}_{style}",
        json.dumps(xquery),
        ex=config["REDIS"]["EXPIRY"],
    )
    return xquery

