# IMPORTS
from datetime import datetime
import json, time
from fastapi import FastAPI, Request, status, Depends, Response
from fastapi.responses import JSONResponse
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

    def __init__(self, inserted, execution):
        self.inserted = inserted
        self.execution = execution

    def to_dict(self):
        """Makes it readable for `print()`"""
        return {"inserted": self.inserted, "execution": self.execution}


app = FastAPI()


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
@app.get("/surftimer/mapchooser")
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


# SurfTimer
@app.get("/surftimer/latestrecords")
def selectLatestRecord(request: Request, response: Response):
    """Retrieves the last 50 records\n
    ```char sql_selectLatestRecords[] = ....```"""
    append_request_log(request)

    tic = time.perf_counter()

    xquery = selectQuery(surftimer.queries.sql_selectLatestRecords)

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    return xquery


@app.post("/surftimer/latestrecords")
def insertLatestRecord(
    request: Request, steamid: str, name: str, runtime: float, mapname: str
):
    """Inserts a new record to the table\n
    ```char sql_insertLatestRecords[] = ....```"""
    append_request_log(request)

    tic = time.perf_counter()

    sql = surftimer.queries.sql_insertLatestRecords.format(
        steamid, name, runtime, mapname
    )
    xquery = insertQuery(sql)
    # xquery = 1
    # time.sleep(3)

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    # Prepare the response
    response = ResponseInsertQuery(xquery, float(format(toc - tic, ".4f")))

    return response


# new code 👇
@app.get("/api/private")
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
