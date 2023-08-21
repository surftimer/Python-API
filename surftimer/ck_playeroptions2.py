from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from sql import selectQuery, insertQuery
from globals import redis_client, config, append_request_log
import time, json
import surftimer.queries

router = APIRouter()



# ck_playeroptions2
@router.post(
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
    tags=["SurfTimer", "ck_playeroptions2"],
)
def selectPlayerOptions(request: Request, response: Response, steamid32: str):
    """`char[] sql_selectPlayerOptions = ....`"""
    tic = time.perf_counter()
    append_request_log(request)

    # Check if data is cached in Redis
    cached_data = redis_client.get(f"selectPlayerOptions_{steamid32}")
    if cached_data:
        # Return cached data
        # print(json.loads(cached_data))
        print(
            f"[Redis] Loaded 'selectPlayerOptions_{steamid32}' ({time.perf_counter() - tic:0.4f}s)"
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(surftimer.queries.sql_selectPlayerOptions.format(steamid32))

    if xquery:
        xquery = xquery.pop()
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        xquery = {"steamid32": steamid32}

    # Cache the data in Redis
    redis_client.set(
        f"selectPlayerOptions_{steamid32}",
        json.dumps(xquery),
        ex=config["REDIS"]["EXPIRY"],
    )

    toc = time.perf_counter()
    xquery["xtime"] = toc - tic
    print(f"Execution time {toc - tic:0.4f}")
    return xquery


@router.post(
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
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"inserted": xquery, "xtime": time.perf_counter() - tic},
        )

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")
    # output = ResponseInsertQuery(xquery)

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}

