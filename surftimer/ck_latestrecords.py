from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from sql import selectQuery
from globals import redis_client, config, append_request_log
import time, json
import surftimer.queries

router = APIRouter()


# ck_latestrecords
@router.get(
    "/surftimer/selectLatestRecords",
    name="Get Latest Records",
    tags=["SurfTimer", "ck_latestrecords"],
)
def selectLatestRecord(request: Request, response: Response):
    """Retrieves the last 50 records\n
    ```char sql_selectLatestRecords[] = ....```"""
    tic = time.perf_counter()

    append_request_log(request)

    # # Check if data is cached in Redis -- Errors out in here for some reason 
    # cached_data = redis_client.get("selectLatestRecord")
    # if cached_data:
    #     # Return cached data
    #     # print(json.loads(cached_data))
    #     print(
    #         f"[Redis] Loaded 'selectLatestRecord' ({time.perf_counter() - tic:0.4f}s)"
    #     )
    #     return JSONResponse(
    #         status_code=status.HTTP_200_OK, content=json.loads(cached_data)
    #     )

    xquery = selectQuery(surftimer.queries.sql_selectLatestRecords)

    if len(xquery) <= 0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"xtime": time.perf_counter() - tic},
        )

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    redis_client.set(
        f"selectLatestRecord",
        str(xquery),
        ex=config["REDIS"]["EXPIRY"],
    )

    return xquery


@router.post(
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
