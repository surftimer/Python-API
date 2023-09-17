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
