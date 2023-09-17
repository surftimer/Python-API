# IMPORTS
from datetime import datetime
import json, time
from fastapi import FastAPI, Request, status, Depends, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware import Middleware
from auth import VerifyToken
from threading import Thread  # Not used yet

# Templates
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

from globals import (
    token_auth_scheme,
    config,
    redis_client,
    tags_metadata,
    WHITELISTED_IPS,
    append_request_log,
    append_denied_log,
)

from sql import selectQuery, insertQuery

# Import all the endpoints for each table
from surftimer.ck_latestrecords import router as ck_latestrecords_router
from surftimer.ck_maptier import router as ck_maptier_router
from surftimer.ck_playerrank import router as ck_playerrank_router
from surftimer.ck_playeroptions2 import router as ck_playeroptions2_router
from surftimer.ck_bonus import router as ck_bonus_router
from surftimer.ck_checkpoints import router as ck_checkpoints_router
from surftimer.ck_playertemp import router as ck_playertemp_router
from surftimer.points import router as points_calculation


class IPValidatorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Get client IP
        ip = str(request.client.host)

        # Check if IP is allowed
        if ip not in WHITELISTED_IPS:
            append_denied_log(request)
            data = {"message": "Not Allowed", "ip": ip}
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=data)

        append_request_log(request)
        # Proceed if IP is allowed
        return await call_next(request)


# Swagger UI configuration - https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/
swagger_config = {
    "displayOperationId": False,  # Show operationId on the UI
    "defaultModelsExpandDepth": 1,  # The default expansion depth for models (set to -1 completely hide the models)
    "defaultModelExpandDepth": 2,
    "defaultModelRendering": "example",
    "deepLinking": True,  # Enables deep linking for tags and operations
    "useUnsafeMarkdown": True,
    "displayRequestDuration": True,
    "filter": True,
    "showExtensions": True,
    "syntaxHighlight.theme": "arta",
    "docExpansion": "none",
    "pluginLoadType": "chain",
    "tagsSorter": "alpha",
}
app = FastAPI(
    title="SurfTimer API",
    description="""by [`tslashd`](https://github.com/tslashd)""",
    version="0.0.0",
    debug=True,
    swagger_ui_parameters=swagger_config,
    middleware=[Middleware(IPValidatorMiddleware)],
    openapi_tags=tags_metadata,
)


# Attach the routes
app.include_router(ck_latestrecords_router)
app.include_router(ck_maptier_router)
app.include_router(ck_playerrank_router)
app.include_router(ck_playeroptions2_router)
app.include_router(ck_bonus_router)
app.include_router(ck_checkpoints_router)
app.include_router(ck_playertemp_router)
app.include_router(points_calculation)


@app.get("/docs2", include_in_schema=False)
async def custom_swagger_ui_html_cdn():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        # swagger_ui_dark.css CDN link
        swagger_css_url="https://cdn.jsdelivr.net/gh/Itz-fork/Fastapi-Swagger-UI-Dark/assets/swagger_ui_dark.min.css",
        swagger_ui_parameters=swagger_config,
    )


@app.get("/", include_in_schema=False)
async def home():
    data = {"message": "Suuuuh duuuud"}
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)


# SurfTimer-Mapchooser queries
@app.get(
    "/surftimer/mapchooser",
    name="Mapchooser & Nominations & RTV",
    tags=["Mapchooser"],
    include_in_schema=False,
)
async def mapchooser(
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
    tic = time.perf_counter()

    json_data = []

    # Check if data is cached in Redis
    cache_key = f"mapchooser:{type}_{tier_min}_{tier_max}_{tier}_{steamid}_{style}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        # Return cached data
        # print(json.loads(cached_data))
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )
    # This needs to be dynamic depending on tickrates
    db = "surftimer_test"

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

    # Cache the data in Redis
    redis_client.set(
        cache_key,
        json.dumps(json_data),
        ex=config["REDIS"]["EXPIRY"],
    )

    return json_data


# new code 👇
@app.get(
    "/api/private",
    tags=["Private"],
    name="Test Authentication Tokens",
    include_in_schema=False,
)
async def private(
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
