from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sql import selectQuery, insertQuery
from globals import get_cache, set_cache
import time, json
import surftimer.queries

router = APIRouter()


class LatestRec(BaseModel):
    steamid32: str
    name: str
    runtime: float
    mapname: str

# ck_latestrecords
@router.get(
    "/surftimer/selectLatestRecords",
    name="Get Latest Records",
    tags=["ck_latestrecords"],
)
async def selectLatestRecord(request: Request, response: Response):
    """Retrieves the last 50 records\n
    ```char sql_selectLatestRecords[] = ....```"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"selectLatestRecord"
    cached_data = get_cache(cache_key)

    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")

        return JSONResponse(
            status_code=status.HTTP_200_OK, content=json.loads(cached_data)
        )

    xquery = selectQuery(surftimer.queries.sql_selectLatestRecords)

    if len(xquery) <= 0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"xtime": time.perf_counter() - tic},
        )

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    # Cache the data in Redis
    set_cache(cache_key, xquery)

    return xquery


@router.post(
    "/surftimer/insertLatestRecords",
    name="Add Latest Record",
    tags=["ck_latestrecords"],
)
async def insertLatestRecord(
    request: Request,
    response: Response,
    data: LatestRec
):
    """Inserts a new record to the table\n
    ```char sql_insertLatestRecords[] = ....```"""
    tic = time.perf_counter()

    sql = surftimer.queries.sql_insertLatestRecords.format(
        data.steamid32, data.name, data.runtime, data.mapname
    )
    xquery = insertQuery(sql)
    # xquery = 0
    # time.sleep(3)

    if xquery < 1:
        JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"inserted": xquery, "xtime": time.perf_counter() - tic},
        )

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    return {"inserted": xquery, "xtime": time.perf_counter() - tic}
