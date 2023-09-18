from fastapi import APIRouter, Request, Response, status
from sql import selectQuery
from globals import get_cache, set_cache
import time, json
import surftimer.queries

router = APIRouter()


@router.get(
    "/surftimer/point_calc_finishedStages",
    name="Count Player Finished Stages",
    tags=["strays", "Points Calculation"],
)
def point_calc_finishedStages(
    request: Request,
    response: Response,
    steamid32: str,
    style: int,
):
    """```char sql_stray_point_calc_finishedStages[] = ....```\n"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"point_calc_finishedStages:{steamid32}-{style}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_stray_point_calc_finishedStages.format(steamid32, style)
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
    "/surftimer/point_calc_finishedMaps",
    name="Count Player Finished Maps",
    tags=["strays", "Points Calculation"],
)
def point_calc_finishedMaps(
    request: Request,
    response: Response,
    steamid32: str,
    style: int,
):
    """```char sql_stray_point_calc_finishedMaps[] = ....```\n"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"point_calc_finishedStages:{steamid32}-{style}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    xquery = selectQuery(
        surftimer.queries.sql_stray_point_calc_finishedMaps.format(
            style, style, steamid32, style
        )
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
    "/surftimer/recalculatePoints",
    name="Points Recalculation",
    tags=["Refactored", "Points Calculation"],
)
def recalculatePoints(
    request: Request,
    response: Response,
    steamid32: str,
    style: int,
):
    """Combines all the queries for point calculation into 1 endpoint"""
    tic = time.perf_counter()

    # Player Name for the selected Style
    player_name_query = selectQuery(
        surftimer.queries.sql_stray_point_calc_playerRankName.format(steamid32, style)
    )
    if len(player_name_query) <= 0:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    else:
        player_name_query = player_name_query.pop()
        # name = str(player_name_query[0])

    ## Bonuses
    finished_bonuses_query = selectQuery(
        surftimer.queries.sql_stray_point_calc_countFinishedBonus.format(
            style, style, steamid32, style
        )
    )
    if len(finished_bonuses_query) <= 0:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    ## Stages
    finished_stages_query = selectQuery(
        surftimer.queries.sql_stray_point_calc_finishedStages.format(steamid32, style)
    )
    if len(finished_stages_query) <= 0:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    ## Maps
    finished_maps_query = selectQuery(
        surftimer.queries.sql_stray_point_calc_finishedMaps.format(
            style, style, steamid32, style
        )
    )
    if len(finished_maps_query) <= 0:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    # Create the JSON output
    output = {
        **player_name_query,  # Replace with your desired name
        "maps": finished_maps_query,
        "stages": finished_stages_query,
        "bonuses": finished_bonuses_query,
    }

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    return output
