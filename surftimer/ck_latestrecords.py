from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sql import selectQuery, insertQuery
from globals import get_cache, set_cache, default_serializer
import time
import simplejson as json
import surftimer.queries
from decimal import Decimal

router = APIRouter()


class LatestRec(BaseModel):
    steamid32: str
    name: str
    runtime: Decimal
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
    
    content_data = {"inserted": xquery, "xtime": time.perf_counter() - tic}
    if xquery < 1:
        # response.body = json.dumps(content_data).encode('utf-8')
        response.headers['content-type'] = 'application/json'
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return response

    # Prepare the response
    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    response.body = json.dumps(content_data).encode('utf-8')
    response.status_code = status.HTTP_201_CREATED
    return response
