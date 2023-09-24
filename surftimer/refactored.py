from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from decimal import Decimal
import simplejson as json
from sql import selectQuery, insertQuery
from globals import set_cache, get_cache, all_styles
import time, surftimer.queries, math


class PlayerMapDataModel(BaseModel):
    """Used by the game servers to load player data for each map"""

    options_data: object
    points_data: list
    bonus_data: list
    checkpoints_data: list  # `Checkpoints = Stages` for Personal Map Run Stage times on *Staged* maps


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
    ```char sql_selectStageTimes[] = ....```\n
    ```char sql_selectStageAttempts[] = ....```\n
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

    if not options_data:
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    points_data = selectQuery(
        surftimer.queries.sql_selectRankedPlayer.format(steamid32)
    )

    bonus_data = selectQuery(
        surftimer.queries.sql_selectPersonalBonusRecords.format(steamid32, mapname)
    )

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

    checkpoints_data = selectQuery(
        surftimer.queries.sql_selectCheckpointsData.format(mapname, steamid32)
    )

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    PlayerMapData = {
        "options_data": options_data.pop(),
        "points_data": points_data,
        "bonus_data": bonus_data,
        "checkpoints_data": checkpoints_data,  # counts as personal map run stages for *Staged* maps - WRCP is different
    }

    # Cache the data in Redis
    set_cache(cache_key, PlayerMapData)

    return PlayerMapData


@router.get(
    "/surftimer/getMapInitData",
    name="Map data",
    tags=["Refactored"],
)
def getMapInitData(
    request: Request,
    response: Response,
    mapname: str,
):
    """combines the following:\n
    ```char sql_selectMapRecord[] = ....```\n
    and maybe more to output a single object with **map** data"""
    tic = time.perf_counter()

    # Check if data is cached in Redis
    cache_key = f"getMapInitData:{mapname}"
    cached_data = get_cache(cache_key)

    if cached_data is not None:
        print(f"[Redis] Loaded '{cache_key}' ({time.perf_counter() - tic:0.4f}s)")
        response.headers["content-type"] = "application/json"
        response.status_code = status.HTTP_200_OK
        response.body = json.loads(cached_data, use_decimal=True, parse_nan=True)
        return response

    map_record_runs_data = selectQuery(
        surftimer.queries.sql_selectMapRecordsNew.format(mapname, mapname)
    )

    # if not map_record_runs_data:
    #     response.headers["content-type"] = "application/json"
    #     response.status_code = status.HTTP_204_NO_CONTENT
    #     return response
    # total_bonuses = surftimer.queries.sql_selectBonusCount.format(mapname)
    map_bonus_data = selectQuery(
        surftimer.queries.sql_selectBonusData.format(mapname, mapname)
    )

    # bonus_data = selectQuery(
    #     surftimer.queries.sql_selectPersonalBonusRecords.format(steamid32, mapname)
    # )

    # checkpoints_data = selectQuery(
    #     surftimer.queries.sql_selectCheckpointsData.format(mapname, steamid32)
    # )

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    MapData = {
        "map_record_runs_data": map_record_runs_data,
        "map_bonus_data": map_bonus_data,
        # "bonus_data": bonus_data,
        # "checkpoints_data": checkpoints_data,  # counts as personal map run stages for *Staged* maps
    }

    # Cache the data in Redis
    set_cache(cache_key, MapData)

    return MapData


@router.get(
    "/surftimer/internalRecalculation",
    name="Internal recalculation",
    tags=["Refactored", "Points Calculation"],
)
def internalRecalculation(
    request: Request,
    response: Response,
):
    """combines all the logic and queries used for player points calculation inside API:\n
    ```char sql_selectRankedPlayers[] = ....```\n
    ```char sql_stray_point_calc_playerRankName[] = ....```\n
    and maybe more to output a single object with **map** data"""
    tic = time.perf_counter()

    initiate_points_calculation(0)

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")
    return {"data": "Started recalculation"}


def initiate_points_calculation(style: int):
    top_list = selectQuery(surftimer.queries.sql_selectRankedPlayers)
    idx = 0
    # with open("_recalc.json") as r:
    #     calc_log = json.load(r)

    for player in top_list:
        if idx == 1:
            break

        if style != 0:
            # Player Name for the selected Style
            select_name_query = selectQuery(
                surftimer.queries.sql_stray_point_calc_playerRankName.format(
                    steamid32, style
                )
            ).pop()
            name = select_name_query.pop() if select_name_query else name
        else:
            name = player["name"]

        steamid32 = player["steamid"]
        print(f"{name} - {steamid32}")
        player["calc_data"] = get_player_data_for_calculation(steamid32, style, name)

        idx = idx + 1

        # # Calculation Log
        # calc_log.append(player)

        # with open("_recalc.json", "w") as json_file:
        #     json.dump(calc_log, json_file, indent=4, separators=(",", ": "))


def get_player_data_for_calculation(steamid32: str, style: int, name: str):
    """Combines all the queries for point calculation into 1 function\n
    # For Internal Calculation"""
    tic = time.perf_counter()

    if style > 0:
        # Player Name for the selected Style
        player_name_query = selectQuery(
            surftimer.queries.sql_stray_point_calc_playerRankName.format(
                steamid32, style
            )
        )
        if len(player_name_query) <= 0:
            return None
        else:
            name = player_name_query.pop()["name"]

    ## Bonuses
    finished_bonuses_query = selectQuery(
        surftimer.queries.sql_stray_point_calc_countFinishedBonus.format(
            style, style, steamid32, style
        )
    )

    ## Stages
    finished_stages_query = selectQuery(
        surftimer.queries.sql_stray_point_calc_finishedStages.format(steamid32, style)
    )

    ## Maps
    finished_maps_query = selectQuery(
        surftimer.queries.sql_stray_point_calc_finishedMaps.format(
            style, style, steamid32, style
        )
    )

    # Create the JSON output
    output = {
        # **player_name_query,  # Replace with your desired name
        "name": name,
        "maps": finished_maps_query,
        "stages": finished_stages_query,
        "bonuses": finished_bonuses_query,
    }
    output["calculated"] = calculate_points(output, 0)

    toc = time.perf_counter()
    print(f"Execution time {toc - tic:0.4f}")

    return output


def calculate_points(player_data: dict[str, list], points_for_wrcp: int):
    # print("hi")
    total_points = 0
    top_10_maps = 0
    g_GroupMaps = 0
    world_records = 0
    wrcps = 0
    wrbs = 0
    wrb_points = 0
    wrcp_points = 0
    wr_points = 0

    finished_stages = len(player_data["stages"])
    wrcps = 0
    # Calculate points from stages - World Record Stage Times
    for stage_completion in player_data["stages"]:
        if stage_completion["rank"] == 1:
            wrcps += 1
            total_points += points_for_wrcp
    wrcp_points = total_points

    finished_bonuses = len(player_data["bonuses"])
    wrbs = 0
    # Calculate points from Bonuses
    for bonus_completion in player_data["bonuses"]:
        if bonus_completion["rank"] == 1:
            wrbs = wrbs + 1
            total_points = total_points + 250
            wrb_points += 250
        elif bonus_completion["rank"] == 2:
            total_points = total_points + 235
        elif bonus_completion["rank"] == 3:
            total_points = total_points + 220
        elif bonus_completion["rank"] == 4:
            total_points = total_points + 205
        elif bonus_completion["rank"] == 5:
            total_points = total_points + 190
        elif bonus_completion["rank"] == 6:
            total_points = total_points + 175
        elif bonus_completion["rank"] == 7:
            total_points = total_points + 160
        elif bonus_completion["rank"] == 8:
            total_points = total_points + 145
        elif bonus_completion["rank"] == 9:
            total_points = total_points + 130
        elif bonus_completion["rank"] == 10:
            total_points = total_points + 100
        elif bonus_completion["rank"] == 11:
            total_points = total_points + 95
        elif bonus_completion["rank"] == 12:
            total_points = total_points + 90
        elif bonus_completion["rank"] == 13:
            total_points = total_points + 80
        elif bonus_completion["rank"] == 14:
            total_points = total_points + 70
        elif bonus_completion["rank"] == 15:
            total_points = total_points + 60
        elif bonus_completion["rank"] == 16:
            total_points = total_points + 50
        elif bonus_completion["rank"] == 17:
            total_points = total_points + 40
        elif bonus_completion["rank"] == 18:
            total_points = total_points + 30
        elif bonus_completion["rank"] == 19:
            total_points = total_points + 20
        elif bonus_completion["rank"] == 20:
            total_points = total_points + 10
        elif bonus_completion["rank"] > 20:
            total_points = total_points + 5

    finished_maps = len(player_data["maps"])
    # ----------  KSF Points System  ----------#
    g_Group1Pc = 0.03125
    g_Group2Pc = 0.0625
    g_Group3Pc = 0.125
    g_Group4Pc = 0.25
    g_Group5Pc = 0.5
    g1bot = 11
    # Calculate points from Maps
    for maps_completion in player_data["maps"]:
        totalplayers = maps_completion["total"]
        rank = maps_completion["rank"]
        tier = maps_completion["tier"]

        if maps_completion["rank"] == 1:
            wrbs = wrbs + 1

        # Group 1
        fG1top = float(totalplayers) * g_Group1Pc
        fG1top += 11.0
        g1top = math.ceil(fG1top)

        g1difference = g1top - g1bot
        if g1difference < 4:
            g1top = g1bot + 4

        # Group 2
        g2bot = g1top + 1
        fG2top = float(totalplayers) * g_Group2Pc
        fG2top += 11.0
        g2top = math.ceil(fG2top)

        g2difference = g2top - g2bot
        if g2difference < 4:
            g2top = g2bot + 4

        # Group 3
        g3bot = g2top + 1
        fG3top = float(totalplayers) * g_Group3Pc
        fG3top += 11.0
        g3top = math.ceil(fG3top)

        g3difference = g3top - g3bot
        if g3difference < 4:
            g3top = g3bot + 4

        # Group 4
        g4bot = g3top + 1
        fG4top = float(totalplayers) * g_Group4Pc
        fG4top += 11.0
        g4top = math.ceil(fG4top)

        g4difference = g4top - g4bot
        if g4difference < 4:
            g4top = g4bot + 4

        # Group 5
        g5bot = g4top + 1
        fG5top = float(totalplayers) * g_Group5Pc
        fG5top += 11.0
        g5top = math.ceil(fG5top)

        g5difference = g5top - g5bot
        if g5difference < 4:
            g5top = g5bot + 4

        if tier == 1:
            wr_points = (float(totalplayers) * 1.75) / 6
            wr_points += 58.5
            if wr_points < 250.0:
                wr_points = 250.0
        elif tier == 2:
            wr_points = (float(totalplayers) * 2.8) / 5
            wr_points += 82.15
            if wr_points < 500.0:
                wr_points = 500.0
        elif tier == 3:
            wr_points = (float(totalplayers) * 3.5) / 4
            if wr_points < 750.0:
                wr_points = 750.0
            else:
                wr_points += 117
        elif tier == 4:
            wr_points = (float(totalplayers) * 5.74) / 4
            if wr_points < 1000.0:
                wr_points = 1000.0
            else:
                wr_points += 164.25
        elif tier == 5:
            wr_points = (float(totalplayers) * 7) / 4
            if wr_points < 1250.0:
                wr_points = 1250.0
            else:
                wr_points += 234
        elif tier == 6:
            wr_points = (float(totalplayers) * 14) / 4
            if wr_points < 1500.0:
                wr_points = 1500.0
            else:
                wr_points += 328
        elif tier == 7:
            wr_points = (float(totalplayers) * 21) / 4
            if wr_points < 1750.0:
                wr_points = 1750.0
            else:
                wr_points += 420
        elif tier == 8:
            wr_points = (float(totalplayers) * 30) / 4
            if wr_points < 2000.0:
                wr_points = 2000.0
            else:
                wr_points += 560
        else:  # no tier set
            wr_points = 25.0

        iwrpoints = math.ceil(wr_points)

        # Top 10 Points
        if rank < 11:
            top_10_maps += 1
            if rank == 1:
                total_points += iwrpoints
                world_records += 1
            elif rank == 2:
                points = 0.80 * iwrpoints
                total_points += math.ceil(points)
            elif rank == 3:
                points = 0.75 * iwrpoints
                total_points += math.ceil(points)
            elif rank == 4:
                points = 0.70 * iwrpoints
                total_points += math.ceil(points)
            elif rank == 5:
                points = 0.65 * iwrpoints
                total_points += math.ceil(points)
            elif rank == 6:
                points = 0.60 * iwrpoints
                total_points += math.ceil(points)
            elif rank == 7:
                points = 0.55 * iwrpoints
                total_points += math.ceil(points)
            elif rank == 8:
                points = 0.50 * iwrpoints
                total_points += math.ceil(points)
            elif rank == 9:
                points = 0.45 * iwrpoints
                total_points += math.ceil(points)
            elif rank == 10:
                points = 0.40 * iwrpoints
                total_points += math.ceil(points)
        elif rank > 10 and rank <= g5top:
            # Group 1-5 Points
            g_GroupMaps += 1

            # Calculate Group Points
            g1points = iwrpoints * 0.25
            g2points = g1points / 1.5
            g3points = g2points / 1.5
            g4points = g3points / 1.5
            g5points = g4points / 1.5

            if rank >= g1bot and rank <= g1top:  # Group 1
                total_points += math.ceil(g1points)
                # g_Points[client][style][2] += math.ceil(g1points)
            elif rank >= g2bot and rank <= g2top:  # Group 2
                total_points += math.ceil(g2points)
                # g_Points[client][style][2] += math.ceil(g2points)
            elif rank >= g3bot and rank <= g3top:  # Group 3
                total_points += math.ceil(g3points)
                # g_Points[client][style][2] += math.ceil(g3points)
            elif rank >= g4bot and rank <= g4top:  # Group 4
                total_points += math.ceil(g4points)
                # g_Points[client][style][2] += math.ceil(g4points)
            elif rank >= g5bot and rank <= g5top:  # Group 5
                total_points += math.ceil(g5points)
                # g_Points[client][style][2] += math.ceil(g5points)

        if tier == 1:
            total_points += 25
            # g_Points[client][style][0] += 25
        elif tier == 2:
            total_points += 50
            # g_Points[client][style][0] += 50
        elif tier == 3:
            total_points += 100
            # g_Points[client][style][0] += 100
        elif tier == 4:
            total_points += 200
            # g_Points[client][style][0] += 200
        elif tier == 5:
            total_points += 400
            # g_Points[client][style][0] += 400
        elif tier == 6:
            total_points += 600
            # g_Points[client][style][0] += 600
        elif tier == 7:
            total_points += 800
            # g_Points[client][style][0] += 800
        elif tier == 8:
            total_points += 1000
            # g_Points[client][style][0] += 1000
        else:  # no tier
            total_points += 13
            # g_Points[client][style][0] += 13

    output = {
        "total": total_points,
        "finished_stages": finished_stages,
        "finished_maps": finished_maps,
        "finished_bonuses": finished_bonuses,
        "wrb_points": wrb_points,
        "wrbs": wrbs,
        "wrcp_points": wrcp_points,
        "wrcps": wrcps,
        "wr_points": wr_points,
        "world_records": world_records,
        "g1points": g1points,
        "g2points": g2points,
        "g3points": g3points,
        "g4points": g4points,
        "g5points": g5points,
    }

    print(output)
    # print(
    #     f"total: {total_points} | bonuses comp: {finished_bonuses} | wrbpoints: {wrb_points} | wrbs: {wrbs} | stages comp: {finished_stages} | wrcppoints: {wrcp_points} | wrcps: {wrcps} | maps comp: {finished_maps} | wrpoints: {wr_points} | world records: {world_records} | g1: {g1points}  | g2: {g2points} | g3: {g3points} | g4: {g4points} | g5: {g5points}"
    # )

    return output
