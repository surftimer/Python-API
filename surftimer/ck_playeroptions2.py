from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from sql import selectQuery, insertQuery
from globals import append_request_log, get_cache, set_cache
from pydantic import BaseModel
import time, json, surftimer.queries


router = APIRouter()


class PlayerOptions(BaseModel):
    timer: int
    hide: int
    sounds: int
    chat: int
    viewmodel: int
    autobhop: int
    checkpoints: int
    gradient: int
    speedmode: int
    centrespeed: int
    centrehud: int
    teleside: int
    module1c: int
    module2c: int
    module3c: int
    module4c: int
    module5c: int
    module6c: int
    sidehud: int
    module1s: int
    module2s: int
    module3s: int
    module4s: int
    module5s: int
    prestrafe: int
    cpmessages: int
    wrcpmessages: int
    hints: int
    csd_update_rate: int
    csd_pos_x: int
    csd_pos_y: int
    csd_r: int
    csd_g: int
    csd_b: int
    prespeedmode: int
    steamid32: str


# ck_playeroptions2
@router.post(
    "/surftimer/insertPlayerOptions",
    name="Insert Player Options",
    tags=["ck_playeroptions2"],
)
def insertPlayerOptions(request: Request, response: Response, steamid32: str):
    """```c
    char[] sql_insertPlayerOptions = ....
    ```"""
    tic = time.perf_counter()
    append_request_log(request)

    xquery = insertQuery(surftimer.queries.sql_insertPlayerOptions.format(steamid32))

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
    "/surftimer/selectPlayerOptions",
    name="Get Player Options",
    tags=["ck_playeroptions2"],
)
def selectPlayerOptions(request: Request, response: Response, steamid32: str):
    """`char[] sql_selectPlayerOptions = ....`"""
    tic = time.perf_counter()
    append_request_log(request)

    # Check if data is cached in Redis
    cache_key = f"selectPlayerOptions_{steamid32}"
    cached_data = get_cache(cache_key)
    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(surftimer.queries.sql_selectPlayerOptions.format(steamid32))

    if xquery:
        xquery = xquery.pop()
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content=json.loads(cached_data)
        )

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    return xquery


@router.put(
    "/surftimer/updatePlayerOptions",
    name="Update Player Options",
    tags=["ck_playeroptions2"],
)
def updatePlayerOptions(request: Request, response: Response, data: PlayerOptions):
    """```c
    char[] sql_updatePlayerOptions = ....
    ```"""
    tic = time.perf_counter()
    append_request_log(request)

    xquery = insertQuery(
        surftimer.queries.sql_updatePlayerOptions.format(
            data.timer,
            data.hide,
            data.sounds,
            data.chat,
            data.viewmodel,
            data.autobhop,
            data.checkpoints,
            data.gradient,
            data.speedmode,
            data.centrespeed,
            data.centrehud,
            data.teleside,
            data.module1c,
            data.module2c,
            data.module3c,
            data.module4c,
            data.module5c,
            data.module6c,
            data.sidehud,
            data.module1s,
            data.module2s,
            data.module3s,
            data.module4s,
            data.module5s,
            data.prestrafe,
            data.cpmessages,
            data.wrcpmessages,
            data.hints,
            data.csd_update_rate,
            data.csd_pos_x,
            data.csd_pos_y,
            data.csd_r,
            data.csd_g,
            data.csd_b,
            data.prespeedmode,
            data.steamid32,
        )
    )

    if xquery < 1:
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"updated": xquery, "xtime": time.perf_counter() - tic},
        )

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")
    # output = ResponseInsertQuery(xquery)

    return {"updated": xquery, "xtime": time.perf_counter() - tic}
