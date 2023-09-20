from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from decimal import Decimal
import simplejson as json
from sql import selectQuery, insertQuery
from globals import set_cache, get_cache, all_styles
import time, surftimer.queries


router = APIRouter()


@router.get(
    "/surftimer/getPlayerInitData",
    name="Player map data",
    tags=["Refactored"],
)
def getPlayerInitData(
    request: Request,
    response: Response,
    steamid32: str,
    mapname: str,
):
    """combines the following:\n
    ```char sql_selectPlayerOptions[] = ....```\n
    ```char sql_selectPersonalBonusRecords[] = ....```\n
    ```char sql_selectCheckpoints[] = ....```\n
    ```char sql_selectPlayerRankBonusCount[] = ....```\n
    and maybe more to output a single object with player data"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"getPlayerInitData:{steamid32}-{mapname}"
    cached_data = get_cache(cache_key)

    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    options_data = selectQuery(
        surftimer.queries.sql_selectPlayerOptions.format(steamid32)
    )

    points_data = selectQuery(
        surftimer.queries.sql_selectRankedPlayer.format(steamid32)
    )

    bonus_data = selectQuery(
        surftimer.queries.sql_selectPersonalBonusRecords.format(steamid32, mapname)
    )

    checkpoints_data = selectQuery(
        surftimer.queries.sql_selectCheckpoints.format(mapname, steamid32)
    )

    # if len(bonus_data) <= 0:
    #     response.headers["content-type"] = "application/json"
    #     response.status_code = status.HTTP_204_NO_CONTENT
    #     return response

    for completion in bonus_data:
        zonegroup = completion["zonegroup"]
        rank_query = selectQuery(
            surftimer.queries.sql_selectPlayerRankBonusCount.format(
                steamid32,
                mapname,
                zonegroup,
                mapname,
                zonegroup,
            )
        )
        completion["rank"] = rank_query.pop()["COUNT(steamid)"]

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")
    
    output = {
        "options_data": options_data.pop(),
        "points_data": points_data,
        "bonus_data": bonus_data,
        "checkpoints_data": checkpoints_data,
    }

    # Cache the data in Redis
    set_cache(cache_key, output)

    return output
