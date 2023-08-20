# IMPORTS
from datetime import datetime
import json, time
from fastapi import FastAPI, Request, status, Depends, Response
from fastapi.responses import JSONResponse, HTMLResponse
from threading import Thread  # Not used yet


from sql import selectQuery, insertQuery, syncQuery
import surftimer.queries  # Containing all SurfTimer queries from `queries.sp`


# Auth
from auth import VerifyToken  # 👈 new import
from fastapi.security import HTTPBearer  # 👈 new imports

token_auth_scheme = HTTPBearer()

# Config
with open("config.json", "r") as f:
    config = json.load(f)

# Requests Log
with open("requests.json") as fp:
    log = json.load(fp)

# Whitelisted IPs
WHITELISTED_IPS = config["WHITELISTED_IPS"]


def append_request_log(request: Request):
    """Logs some general info about the request recieved in `requests.json`"""
    log.append(
        {
            "url": str(request.url),
            "ip": request.client.host,
            "method": request.method,
            "headers": dict(request.headers),
            "time": str(datetime.now()),
        }
    )
    with open("requests.json", "w") as json_file:
        json.dump(log, json_file, indent=4, separators=(",", ": "))


# Responses
class ResponseInsertQuery:
    """This is to be used for all `INSERT` queries if possible"""

    def __init__(self, inserted):
        self.inserted = inserted

    def to_dict(self):
        """Makes it readable for `print()`"""
        return {"inserted": self.inserted}


# Swagger UI configuration
swagger_config = {
    "displayOperationId": False,  # Show operationId on the UI
    "defaultModelsExpandDepth": -1,  # The default expansion depth for models (set to -1 completely hide the models)
    "deepLinking": True,  # Enables deep linking for tags and operations
    "useUnsafeMarkdown": True,
}
app = FastAPI(
    title="SurfTimer API",
    description="""by [`tslashd`](https://github.com/tslashd)""",
    version="0.0.0",
    debug=False,
    swagger_ui_parameters=swagger_config,
)


@app.middleware("http")
async def validate_ip(request: Request, call_next):
    # Get client IP
    ip = str(request.client.host)

    # Check if IP is allowed
    if ip not in WHITELISTED_IPS:
        data = {"message": f"IP {ip} is not allowed to access this resource."}
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=data)

    # Proceed if IP is allowed
    return await call_next(request)


@app.get("/")
def home():
    data = {"message": "Suuuuh duuuud"}
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)


# SurfTimer-Mapchooser queries
@app.get(
    "/surftimer/mapchooser", name="Mapchooser & Nominations & RTV", tags=["Mapchooser"]
)
def mapchooser(
    request: Request,
    type: int,
    server_tier: str = None,
    tier_min: int = None,
    tier_max: int = None,
    tier: int = None,
    steamid: str = None,
    style: int = None,
):
    """All queries for `st-mapchooser, st-rtv, st-nominations` are contained here with types for the different ones.\n
    Above mentioned plugins need to be reworked to use API Calls, below is actual improvement from this implementation:\n
    ```fix
    Old (1220 maps):
    ===== [Nominations] BuildMapMenu took 12.726562s
    ===== [Nominations] BuildTierMenus took 12.379882s

    New (1220 maps):
    ===== [Nominations] Build ALL menus took 0.015625s
    ```"""
    json_data = []

    # This needs to be dynamic depending on tickrates
    db = "surftimer_test"

    tic = time.perf_counter()
    switch_case = {
        # sql_SelectMapList - Mapchooser/Nominations
        1: f"""SELECT {db}.ck_zones.mapname, tier as maptier, count({db}.ck_zones.zonetype = 3) as stages, bonus as bonuses
            FROM {db}.ck_zones 
            INNER JOIN {db}.ck_maptier on {db}.ck_zones.mapname = {db}.ck_maptier.mapname 
            LEFT JOIN (
                SELECT mapname as map_2, MAX({db}.ck_zones.zonegroup) as bonus 
                FROM {db}.ck_zones 
                GROUP BY mapname
            ) as a on {db}.ck_zones.mapname = a.map_2 
            WHERE (zonegroup = 0 AND (zonetype = 1 or zonetype = 5 or zonetype = 3)) 
            GROUP BY mapname, tier, bonus 
            ORDER BY mapname ASC""",
        # sql_SelectMapListRange - Mapchooser/Nominations
        2: f"""SELECT {db}.ck_zones.mapname, tier as maptier, count({db}.ck_zones.zonetype = 3) as stages, bonus as bonuses
            FROM {db}.ck_zones 
            INNER JOIN {db}.ck_maptier on {db}.ck_zones.mapname = {db}.ck_maptier.mapname 
            LEFT JOIN (
                SELECT mapname as map_2, MAX({db}.ck_zones.zonegroup) as bonus 
                FROM {db}.ck_zones 
                GROUP BY mapname
            ) as a on {db}.ck_zones.mapname = a.map_2 
            WHERE (zonegroup = 0 AND (zonetype = 1 or zonetype = 5 or zonetype = 3)) 
            AND tier >= {tier_min} AND tier <= {tier_max} 
            GROUP BY mapname, tier, bonus 
            ORDER BY mapname ASC""",
        # sql_SelectMapListSpecific - Mapchooser/Nominations
        3: f"""SELECT {db}.ck_zones.mapname, tier as maptier, count({db}.ck_zones.zonetype = 3) as stages, bonus as bonuses
            FROM {db}.ck_zones 
            INNER JOIN {db}.ck_maptier on {db}.ck_zones.mapname = {db}.ck_maptier.mapname 
            LEFT JOIN (
                SELECT mapname as map_2, MAX({db}.ck_zones.zonegroup) as bonus 
                FROM {db}.ck_zones 
                GROUP BY mapname
            ) as a on {db}.ck_zones.mapname = a.map_2 
            WHERE (zonegroup = 0 AND (zonetype = 1 or zonetype = 5 or zonetype = 3)) 
            AND tier = {tier} 
            GROUP BY mapname, tier, bonus 
            ORDER BY mapname ASC""",
        # sql_SelectIncompleteMapList - Nominations
        4: f"""SELECT mapname 
            FROM {db}.ck_maptier 
            WHERE tier > 0 
            AND mapname 
            NOT IN (
                SELECT mapname FROM {db}.ck_playertimes WHERE steamid = '{steamid}' AND style = {style}) ORDER BY tier ASC, mapname ASC""",
        # sql_SelectRank - Mapchooser/RockTheVote
        5: f"""SELECT COUNT(*) AS playerrank
            FROM {db}.ck_playerrank 
            WHERE style = 0 
            AND points >= (SELECT points FROM {db}.ck_playerrank WHERE steamid = '{steamid}' AND style = 0)""",
        # sql_SelectPoints - Mapchooser/RockTheVote
        6: f"""SELECT points AS playerpoints
            FROM {db}.ck_playerrank 
            WHERE steamid = '{steamid}' 
            AND style = 0""",
    }

    query = switch_case.get(type)
    if query is None:
        return "Invalid query number."

    if type == 2 and (tier_min is None or tier_max is None):
        return "Tier min and max values are required for query 2."

    if type == 3 and tier is None:
        return "Tier value is required for query 3."

    if type == 4 and (steamid is None or style is None):
        return "SteamID and Style values are required for query 4."

    if type == 5 and (steamid is None):
        return "SteamID value is required for this query."

    if type == 6 and (steamid is None):
        return "SteamID value is required for this query."

    xquery = selectQuery(query)

    for result in xquery:
        json_data.append(result)

    print(
        f"Q_Type: {type} | T_Min: {tier_min} | T_Max: {tier_max} | Tier: {tier} | SteamID: {steamid} | Style: {style}"
    )
    # Local storage of data
    # filename = 'surftimer/mapchooser.json'
    # # create_json_file(json_data, filename)
    # with open(filename, 'w') as file:
    #     json.dump(json_data, file, indent=4, separators=(',', ': '))
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    return json_data


# ck_latestrecords
@app.get(
    "/surftimer/selectLatestRecords",
    name="Get Latest Records",
    tags=["SurfTimer", "ck_latestrecords"],
)
def selectLatestRecord(request: Request, response: Response):
    """Retrieves the last 50 records\n
    ```char sql_selectLatestRecords[] = ....```"""
    tic = time.perf_counter()

    append_request_log(request)

    xquery = selectQuery(surftimer.queries.sql_selectLatestRecords)

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    return xquery


@app.post(
    "/surftimer/insertLatestRecords",
    name="Add Latest Record",
    tags=["SurfTimer", "ck_latestrecords"],
)
def insertLatestRecord(
    request: Request,
    response: Response,
    steamid32: str,
    name: str,
    runtime: float,
    mapname: str,
):
    """Inserts a new record to the table\n
    ```char sql_insertLatestRecords[] = ....```"""
    tic = time.perf_counter()
    append_request_log(request)

    sql = surftimer.queries.sql_insertLatestRecords.format(
        steamid32, name, runtime, mapname
    )
    # xquery = insertQuery(sql)
    xquery = 0
    # time.sleep(3)

    if xquery < 1:
        JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"inserted": xquery, "xtime": time.perf_counter() - tic},
        )

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")
    # output = ResponseInsertQuery(xquery)

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}


# ck_maptier
@app.get(
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

    xquery = selectQuery(surftimer.queries.sql_selectMapTier.format(mapname)).pop()

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")
    xquery["xtime"] = time.perf_counter() - tic
    return xquery


@app.post(
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
        JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"inserted": xquery, "xtime": time.perf_counter() - tic},
        )

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")
    # output = ResponseInsertQuery(xquery)

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}


@app.post(
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
        JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"inserted": xquery, "xtime": time.perf_counter() - tic},
        )

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")
    # output = ResponseInsertQuery(xquery)

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}


@app.post(
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
        JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"inserted": xquery, "xtime": time.perf_counter() - tic},
        )

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")
    # output = ResponseInsertQuery(xquery)

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}


# ck_playeroptions2
@app.post(
    "/surftimer/insertPlayerOptions",
    name="Insert Player Options",
    tags=["SurfTimer", "ck_playeroptions2"],
)
def insertPlayerOptions(request: Request, response: Response, steamid32: str):
    """```c
    char[] sql_insertPlayerOptions = ....
    ```"""
    tic = time.perf_counter()
    append_request_log(request)

    xquery = insertQuery(surftimer.queries.sql_insertPlayerOptions.format(steamid32))

    if xquery < 1:
        JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"inserted": xquery, "xtime": time.perf_counter() - tic},
        )

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")
    # output = ResponseInsertQuery(xquery)

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}


@app.get(
    "/surftimer/selectPlayerOptions",
    name="Get Player Options",
    tags=["SurfTimer", "ck_playeroptions2"],
)
def selectPlayerOptions(request: Request, response: Response, steamid32: str):
    """`char[] sql_selectPlayerOptions = ....`"""
    tic = time.perf_counter()
    append_request_log(request)

    xquery = selectQuery(surftimer.queries.sql_selectPlayerOptions.format(steamid32))

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        xquery = {"steamid32": steamid32}

    toc = time.perf_counter()
    xquery["xtime"] = toc - tic
    print(f"Execution time {toc - tic:0.4f}")
    return xquery


@app.post(
    "/surftimer/updatePlayerOptions",
    name="Update Player Options",
    tags=["SurfTimer", "ck_playeroptions2"],
)
def updatePlayerOptions(
    request: Request,
    response: Response,
    timer: int,
    hide: int,
    sounds: int,
    chat: int,
    viewmodel: int,
    autobhop: int,
    checkpoints: int,
    gradient: int,
    speedmode: int,
    centrespeed: int,
    centrehud: int,
    teleside: int,
    module1c: int,
    module2c: int,
    module3c: int,
    module4c: int,
    module5c: int,
    module6c: int,
    sidehud: int,
    module1s: int,
    module2s: int,
    module3s: int,
    module4s: int,
    module5s: int,
    prestrafe: int,
    cpmessages: int,
    wrcpmessages: int,
    hints: int,
    csd_update_rate: int,
    csd_pos_x: int,
    csd_pos_y: int,
    csd_r: int,
    csd_g: int,
    csd_b: int,
    prespeedmode: int,
    steamid32: str,
):
    """```c
    char[] sql_updatePlayerOptions = ....
    ```"""
    tic = time.perf_counter()
    append_request_log(request)

    xquery = insertQuery(
        surftimer.queries.sql_updatePlayerOptions.format(
            timer,
            hide,
            sounds,
            chat,
            viewmodel,
            autobhop,
            checkpoints,
            gradient,
            speedmode,
            centrespeed,
            centrehud,
            teleside,
            module1c,
            module2c,
            module3c,
            module4c,
            module5c,
            module6c,
            sidehud,
            module1s,
            module2s,
            module3s,
            module4s,
            module5s,
            prestrafe,
            cpmessages,
            wrcpmessages,
            hints,
            csd_update_rate,
            csd_pos_x,
            csd_pos_y,
            csd_r,
            csd_g,
            csd_b,
            prespeedmode,
            steamid32,
        )
    )

    if xquery < 1:
        JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"inserted": xquery, "xtime": time.perf_counter() - tic},
        )

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")
    # output = ResponseInsertQuery(xquery)

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}


# ck_playerrank
@app.post(
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
        JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"inserted": xquery, "xtime": time.perf_counter() - tic},
        )

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")
    # output = ResponseInsertQuery(xquery)

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}


@app.post(
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
        JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"inserted": xquery, "xtime": time.perf_counter() - tic},
        )

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")
    # output = ResponseInsertQuery(xquery)

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}


@app.post(
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
        JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"inserted": xquery, "xtime": time.perf_counter() - tic},
        )

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")
    # output = ResponseInsertQuery(xquery)

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}


@app.post(
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
        JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"inserted": xquery, "xtime": time.perf_counter() - tic},
        )

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")
    # output = ResponseInsertQuery(xquery)

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}


@app.get(
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

    xquery = selectQuery(surftimer.queries.sql_selectPlayerName.format(steamid32))

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        xquery = {"steamid32": steamid32}

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")
    xquery["xtime"] = time.perf_counter() - tic
    return xquery


@app.post(
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
        JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"inserted": xquery, "xtime": time.perf_counter() - tic},
        )

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")
    # output = ResponseInsertQuery(xquery)

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}


@app.get(
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

    xquery = selectQuery(surftimer.queries.sql_selectTopPlayers.format(style))

    if xquery:
        xquery = xquery
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        xquery = {"style": style}

    toc = time.perf_counter()

    print(f"Execution time {toc - tic:0.4f}")
    # xquery["xtime"] = time.perf_counter() - tic
    return xquery


@app.get(
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

    return xquery


@app.get(
    "/surftimer/selectRankedPlayers",
    name="Select Ranked Players",
    tags=["SurfTimer", "ck_playerrank"],
)
def selectRankedPlayers(request: Request, response: Response):
    """`char[] sql_selectRankedPlayers = ....`"""
    tic = time.perf_counter()
    append_request_log(request)

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

    return xquery


@app.get(
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


@app.get(
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


@app.get(
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
    return xquery


# new code 👇
@app.get("/api/private", tags=["Private"], name="Test Authentication Tokens")
def private(
    response: Response, token: str = Depends(token_auth_scheme)
):  # 👈 updated code
    """A valid access token is required to access this route"""

    result = VerifyToken(token.credentials).verify()  # 👈 updated code

    # 👇 new code
    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    # 👆 new code

    dt = datetime.fromtimestamp(int(result["exp"]))
    formatted_datetime = dt.strftime("%H:%M:%S %d-%m-%Y")
    print("expiry:", formatted_datetime)

    return result
