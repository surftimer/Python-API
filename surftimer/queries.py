"""Containing all SurfTimer queries from `queries.sp`"""
## ck_announcements
sql_createAnnouncements = "CREATE TABLE IF NOT EXISTS `ck_announcements` (`id` int(11) NOT NULL AUTO_INCREMENT, `server` varchar(256) NOT NULL DEFAULT 'Beginner', `name` varchar(64) NOT NULL, `mapname` varchar(128) NOT NULL, `mode` int(11) NOT NULL DEFAULT '0', `time` varchar(32) NOT NULL, `group` int(12) NOT NULL DEFAULT '0', PRIMARY KEY (`id`))DEFAULT CHARSET=utf8mb4;"

## ck_bonus
sql_createBonus = "CREATE TABLE IF NOT EXISTS ck_bonus (steamid VARCHAR(32), name VARCHAR(64), mapname VARCHAR(32), runtime decimal(12,6) NOT NULL DEFAULT '-1.000000', velStartXY SMALLINT(6) NOT NULL DEFAULT 0, velStartXYZ SMALLINT(6) NOT NULL DEFAULT 0, velStartZ SMALLINT(6) NOT NULL DEFAULT 0, zonegroup INT(12) NOT NULL DEFAULT 1, style INT(11) NOT NULL DEFAULT 0, PRIMARY KEY(steamid, mapname, zonegroup, style)) DEFAULT CHARSET=utf8mb4;"
sql_createBonusIndex = (
    "CREATE INDEX bonusrank ON ck_bonus (mapname,runtime,zonegroup,style);"
)

sql_insertBonus = "INSERT INTO ck_bonus (steamid, name, mapname, runtime, zonegroup, velStartXY, velStartXYZ, velStartZ) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
sql_updateBonus = "UPDATE ck_bonus SET runtime = '{}', name = '{}', velStartXY = {}, velStartXYZ = {}, velStartZ = {} WHERE steamid = '{}' AND mapname = '{}' AND zonegroup = {} AND style = 0"
sql_selectBonusCount = "SELECT zonegroup, style, count(1) FROM ck_bonus WHERE mapname = '{}' GROUP BY zonegroup, style;"
sql_selectPersonalBonusRecords = "SELECT runtime, zonegroup, style FROM ck_bonus WHERE steamid = '{}' AND mapname = '{}' AND runtime > '0.0'"
sql_selectPlayerRankBonus = "SELECT name FROM ck_bonus WHERE runtime <= (SELECT runtime FROM ck_bonus WHERE steamid = '{}' AND mapname= '{}' AND runtime > 0.0 AND zonegroup = {} AND style = 0) AND mapname = '{}' AND zonegroup = {} AND style = 0;"
sql_selectFastestBonus = "SELECT t1.name, t1.runtime, t1.zonegroup, t1.style, t1.velStartXY, t1.velStartXYZ, t1.velstartZ from ck_bonus t1 where t1.mapname = '{}' and t1.runtime = (select min(t2.runtime) from ck_bonus t2 where t2.mapname = t1.mapname and t2.zonegroup = t1.zonegroup and t2.style = t1.style);"
sql_deleteBonus = "DELETE FROM ck_bonus WHERE mapname = '{}'"
sql_selectAllBonusTimesinMap = (
    "SELECT zonegroup, runtime from ck_bonus WHERE mapname = '{}';"
)
sql_selectTopBonusSurfers = "SELECT db2.steamid, db1.name, db2.runtime as overall, db1.steamid, db2.mapname FROM ck_bonus as db2 INNER JOIN ck_playerrank as db1 on db2.steamid = db1.steamid WHERE db2.mapname = '{}' AND db2.style = {} AND db1.style = {} AND db2.runtime > -1.0 AND zonegroup = {} ORDER BY overall ASC LIMIT 100;"

## ck_checkpoints
sql_createCheckpoints = "CREATE TABLE IF NOT EXISTS ck_checkpoints (steamid VARCHAR(32), mapname VARCHAR(32), cp INT(11) NOT NULL, time decimal(12,6) NOT NULL DEFAULT '-1.000000', zonegroup INT(12) NOT NULL DEFAULT 0, PRIMARY KEY(steamid, mapname, cp, zonegroup)) DEFAULT CHARSET=utf8mb4;"
sql_InsertOrUpdateCheckpoints = "INSERT INTO ck_checkpoints (steamid, mapname, cp, time, stage_time, stage_attempts, zonegroup) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}') ON DUPLICATE KEY UPDATE time='{}', stage_time='{}', stage_attempts='{}';"
sql_selectCheckpoints = "SELECT zonegroup, cp, time FROM ck_checkpoints WHERE mapname='{}' AND steamid = '{}';"
sql_selectCheckpointsinZoneGroup = "SELECT cp, time FROM ck_checkpoints WHERE mapname='{}' AND steamid = '{}' AND zonegroup = {};"
sql_selectRecordCheckpoints = "SELECT zonegroup, cp, `time` FROM ck_checkpoints WHERE steamid = '{}' AND mapname='{}' UNION SELECT a.zonegroup, b.cp, b.time FROM ck_bonus a LEFT JOIN ck_checkpoints b ON a.steamid = b.steamid AND a.zonegroup = b.zonegroup WHERE a.mapname = '{}' GROUP BY a.zonegroup;"
sql_deleteCheckpoints = "DELETE FROM ck_checkpoints WHERE mapname = '{}'"
sql_selectStageTimes = (
    "SELECT cp, stage_time FROM ck_checkpoints WHERE mapname = '{}' AND steamid = '{}';"
)
sql_selectStageAttempts = "SELECT cp, stage_attempts FROM ck_checkpoints WHERE mapname = '{}' AND steamid = '{}';"

## ck_latestrecords
sql_createLatestRecords = "CREATE TABLE IF NOT EXISTS ck_latestrecords (steamid VARCHAR(32), name VARCHAR(64), runtime decimal(12,6) NOT NULL DEFAULT '-1.000000', map VARCHAR(32), date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(steamid,map,date)) DEFAULT CHARSET=utf8mb4;"
sql_insertLatestRecords = "INSERT INTO ck_latestrecords (steamid, name, runtime, map) VALUES('{}','{}','{}','{}');"
sql_selectLatestRecords = (
    "SELECT name, runtime, map, date FROM ck_latestrecords ORDER BY date DESC LIMIT 50"
)

## ck_maptier
sql_createMapTier = "CREATE TABLE IF NOT EXISTS ck_maptier (mapname VARCHAR(54) NOT NULL, tier INT(12), maxvelocity FLOAT NOT NULL DEFAULT '3500.0', announcerecord INT(11) NOT NULL DEFAULT '0', gravityfix INT(11) NOT NULL DEFAULT '1', ranked INT(11) NOT NULL DEFAULT '1', PRIMARY KEY(mapname)) DEFAULT CHARSET=utf8mb4;"
sql_selectMapTier = "SELECT tier, ranked, mapper FROM ck_maptier WHERE mapname = '{}'"
sql_insertmaptier = "INSERT INTO ck_maptier (mapname, tier) VALUES ('{}', '{}');"
sql_updatemaptier = "UPDATE ck_maptier SET tier = {} WHERE mapname ='{}'"
sql_updateMapperName = "UPDATE ck_maptier SET mapper = '{}' WHERE mapname = '{}'"

## ck_playeroptions2
sql_createPlayerOptions = "CREATE TABLE IF NOT EXISTS `ck_playeroptions2` (`steamid` varchar(32) NOT NULL DEFAULT '', `timer` int(11) NOT NULL DEFAULT '1', `hide` int(11) NOT NULL DEFAULT '0', `sounds` int(11) NOT NULL DEFAULT '1', `chat` int(11) NOT NULL DEFAULT '0', `viewmodel` int(11) NOT NULL DEFAULT '1', `autobhop` int(11) NOT NULL DEFAULT '1', `checkpoints` int(11) NOT NULL DEFAULT '1', `gradient` int(11) NOT NULL DEFAULT '3', `speedmode` int(11) NOT NULL DEFAULT '0', `centrespeed` int(11) NOT NULL DEFAULT '0', `centrehud` int(11) NOT NULL DEFAULT '1', teleside int(11) NOT NULL DEFAULT '0', `module1c` int(11) NOT NULL DEFAULT '1', `module2c` int(11) NOT NULL DEFAULT '2', `module3c` int(11) NOT NULL DEFAULT '3', `module4c` int(11) NOT NULL DEFAULT '4', `module5c` int(11) NOT NULL DEFAULT '5', `module6c` int(11) NOT NULL DEFAULT '6', `sidehud` int(11) NOT NULL DEFAULT '1', `module1s` int(11) NOT NULL DEFAULT '5', `module2s` int(11) NOT NULL DEFAULT '0', `module3s` int(11) NOT NULL DEFAULT '0', `module4s` int(11) NOT NULL DEFAULT '0', `module5s` int(11) NOT NULL DEFAULT '0', prestrafe int(11) NOT NULL DEFAULT '0', cpmessages int(11) NOT NULL DEFAULT '1', wrcpmessages int(11) NOT NULL DEFAULT '1', hints int(11) NOT NULL DEFAULT '1', csd_update_rate int(11) NOT NULL DEFAULT '1' , csd_pos_x float(11) NOT NULL DEFAULT '0.5' , csd_pos_y float(11) NOT NULL DEFAULT '0.3' , csd_r int(11) NOT NULL DEFAULT '255', csd_g int(11) NOT NULL DEFAULT '255', csd_b int(11) NOT NULL DEFAULT '255', PRIMARY KEY (`steamid`)) DEFAULT CHARSET=utf8mb4;"
sql_insertPlayerOptions = "INSERT INTO ck_playeroptions2 (steamid) VALUES ('{}');"
sql_selectPlayerOptions = "SELECT timer, hide, sounds, chat, viewmodel, autobhop, checkpoints, gradient, speedmode, centrespeed, centrehud, teleside, module1c, module2c, module3c, module4c, module5c, module6c, sidehud, module1s, module2s, module3s, module4s, module5s, prestrafe, cpmessages, wrcpmessages, hints, csd_update_rate, csd_pos_x, csd_pos_y, csd_r, csd_g, csd_b, prespeedmode FROM ck_playeroptions2 where steamid = '{}';"
sql_updatePlayerOptions = "UPDATE ck_playeroptions2 SET timer = {}, hide = {}, sounds = {}, chat = {}, viewmodel = {}, autobhop = {}, checkpoints = {}, gradient = {}, speedmode = {}, centrespeed = {}, centrehud = {}, teleside = {}, module1c = {}, module2c = {}, module3c = {}, module4c = {}, module5c = {}, module6c = {}, sidehud = {}, module1s = {}, module2s = {}, module3s = {}, module4s = {}, module5s = {}, prestrafe = {}, cpmessages = {}, wrcpmessages = {}, hints = {}, csd_update_rate = {}, csd_pos_x = {}, csd_pos_y = {}, csd_r= {}, csd_g = {}, csd_b = {}, prespeedmode = {} where steamid = '{}'"

## ck_playerrank
sql_createPlayerRank = "CREATE TABLE IF NOT EXISTS `ck_playerrank` (`steamid` varchar(32) NOT NULL DEFAULT '', `steamid64` varchar(64) DEFAULT NULL, `name` varchar(64) DEFAULT NULL, `country` varchar(32) DEFAULT NULL, `countryCode` varchar(3) DEFAULT NULL, `continentCode` varchar(3) DEFAULT NULL, `points` int(12) DEFAULT '0', `wrpoints` int(12) NOT NULL DEFAULT '0', `wrbpoints` int(12) NOT NULL DEFAULT '0', `wrcppoints` int(11) NOT NULL DEFAULT '0', `top10points` int(12) NOT NULL DEFAULT '0', `groupspoints` int(12) NOT NULL DEFAULT '0', `mappoints` int(11) NOT NULL DEFAULT '0', `bonuspoints` int(12) NOT NULL DEFAULT '0', `finishedmaps` int(12) DEFAULT '0', `finishedmapspro` int(12) DEFAULT '0', `finishedbonuses` int(12) NOT NULL DEFAULT '0', `finishedstages` int(12) NOT NULL DEFAULT '0', `wrs` int(12) NOT NULL DEFAULT '0', `wrbs` int(12) NOT NULL DEFAULT '0', `wrcps` int(12) NOT NULL DEFAULT '0', `top10s` int(12) NOT NULL DEFAULT '0', `groups` int(12) NOT NULL DEFAULT '0', `lastseen` int(64) DEFAULT NULL, `joined` int(64) NOT NULL, `timealive` int(64) NOT NULL DEFAULT '0', `timespec` int(64) NOT NULL DEFAULT '0', `connections` int(64) NOT NULL DEFAULT '1', `readchangelog` int(11) NOT NULL DEFAULT '0', `style` int(11) NOT NULL DEFAULT '0', PRIMARY KEY (`steamid`, `style`)) DEFAULT CHARSET=utf8mb4;"
sql_insertPlayerRank = "INSERT INTO ck_playerrank (steamid, steamid64, name, country, countryCode, continentCode, joined, style) VALUES('{}', '{}', '{}', '{}', '{}', '{}', {}, {})"
sql_updatePlayerRankPoints = "UPDATE ck_playerrank SET name ='{}', points ='{}', wrpoints = {}, wrbpoints = {}, wrcppoints = {}, top10points = {}, groupspoints = {}, mappoints = {}, bonuspoints = {}, finishedmapspro='{}', finishedbonuses = {}, finishedstages = {}, wrs = {}, wrbs = {}, wrcps = {}, top10s = {}, `groups` = {} where steamid='{}' AND style = {};"
sql_updatePlayerRankPoints2 = "UPDATE ck_playerrank SET name ='{}', points ='{}', wrpoints = {}, wrbpoints = {}, wrcppoints = {}, top10points = {}, groupspoints = {}, mappoints = {}, bonuspoints = {}, finishedmapspro='{}', finishedbonuses = {}, finishedstages = {}, wrs = {}, wrbs = {}, wrcps = {}, top10s = {}, `groups` = {}, country = '{}', countryCode = '{}', continentCode = '{}' where steamid='{}' AND style = {};"
sql_updatePlayerRank = "UPDATE ck_playerrank SET finishedmaps ='{}', finishedmapspro='{}' where steamid='{}' AND style = '{}';"
sql_selectPlayerName = "SELECT name FROM ck_playerrank where steamid = '{}'"
sql_UpdateLastSeenMySQL = (
    "UPDATE ck_playerrank SET lastseen = UNIX_TIMESTAMP() where steamid = '{}';"
)
sql_UpdateLastSeenSQLite = (
    "UPDATE ck_playerrank SET lastseen = date('now') where steamid = '{}';"
)
sql_selectTopPlayers = "SELECT name, points, finishedmapspro, steamid FROM ck_playerrank WHERE style = {} ORDER BY points DESC LIMIT 100"
sql_selectRankedPlayer = "SELECT steamid, name, points, finishedmapspro, country, lastseen, timealive, timespec, connections, readchangelog, style, countryCode, continentCode from ck_playerrank where steamid='{}';"
sql_selectRankedPlayersRank = "SELECT name FROM ck_playerrank WHERE style = {} AND points >= (SELECT points FROM ck_playerrank WHERE steamid = '{}' AND style = {}) ORDER BY points;"
sql_selectRankedPlayers = "SELECT steamid, name from ck_playerrank where points > 0 AND style = 0 ORDER BY points DESC LIMIT 0, 1067;"
sql_CountRankedPlayers = "SELECT COUNT(steamid) FROM ck_playerrank WHERE style = {};"
sql_CountRankedPlayers2 = (
    "SELECT COUNT(steamid) FROM ck_playerrank where points > 0 AND style = {};"
)
sql_selectPlayerProfile = "SELECT steamid, steamid64, name, country, points, wrpoints, wrbpoints, wrcppoints, top10points, groupspoints, mappoints, bonuspoints, finishedmapspro, finishedbonuses, finishedstages, wrs, wrbs, wrcps, top10s, `groups`, lastseen, countryCode, continentCode FROM ck_playerrank WHERE steamid = '{}' AND style = '{}';"

## ck_playertemp
sql_createPlayertmp = "CREATE TABLE IF NOT EXISTS ck_playertemp (steamid VARCHAR(32), mapname VARCHAR(32), cords1 FLOAT NOT NULL DEFAULT '-1.0', cords2 FLOAT NOT NULL DEFAULT '-1.0', cords3 FLOAT NOT NULL DEFAULT '-1.0', angle1 FLOAT NOT NULL DEFAULT '-1.0',angle2 FLOAT NOT NULL DEFAULT '-1.0',angle3 FLOAT NOT NULL DEFAULT '-1.0', EncTickrate INT(12) DEFAULT '-1.0', runtimeTmp decimal(12,6) NOT NULL DEFAULT '-1.000000', Stage INT, zonegroup INT NOT NULL DEFAULT 0, PRIMARY KEY(steamid,mapname)) DEFAULT CHARSET=utf8mb4;"
sql_insertPlayerTmp = "INSERT INTO ck_playertemp (cords1, cords2, cords3, angle1,angle2,angle3,runtimeTmp,steamid,mapname,EncTickrate,Stage,zonegroup) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}', '{}', '{}', {}, {});"
sql_updatePlayerTmp = "UPDATE ck_playertemp SET cords1 = '{}', cords2 = '{}', cords3 = '{}', angle1 = '{}', angle2 = '{}', angle3 = '{}', runtimeTmp = '{}', mapname ='{}', EncTickrate='{}', Stage = {}, zonegroup = {} WHERE steamid = '{}';"
sql_deletePlayerTmp = "DELETE FROM ck_playertemp where steamid = '{}';"
sql_selectPlayerTmp = "SELECT cords1,cords2,cords3, angle1, angle2, angle3,runtimeTmp, EncTickrate, Stage, zonegroup FROM ck_playertemp WHERE steamid = '{}' AND mapname = '{}';"

## ck_playertimes
sql_createPlayertimes = "CREATE TABLE IF NOT EXISTS ck_playertimes (steamid VARCHAR(32), mapname VARCHAR(32), name VARCHAR(64), runtimepro decimal(12,6) NOT NULL DEFAULT '-1.000000', velStartXY SMALLINT(6) NOT NULL DEFAULT 0, velStartXYZ SMALLINT(6) NOT NULL DEFAULT 0, velStartZ SMALLINT(6) NOT NULL DEFAULT 0, style INT(11) NOT NULL DEFAULT '0', PRIMARY KEY(steamid, mapname, style)) DEFAULT CHARSET=utf8mb4;"
sql_createPlayertimesIndex = (
    "CREATE INDEX maprank ON ck_playertimes (mapname, runtimepro, style);"
)
sql_insertPlayer = (
    "INSERT INTO ck_playertimes (steamid, mapname, name) VALUES('{}', '{}', '{}');"
)
sql_insertPlayerTime = "INSERT INTO ck_playertimes (steamid, mapname, name, runtimepro, style, velStartXY, velStartXYZ, velStartZ) VALUES('{}', '{}', '{}', '{}', {}, {}, {}, {});"
sql_updateRecordPro = "UPDATE ck_playertimes SET name = '{}', runtimepro = '{}', velStartXY = '{}', velStartXYZ = '{}', velStartZ = '{}' WHERE steamid = '{}' AND mapname = '{}' AND style = {};"
sql_selectPlayer = (
    "SELECT steamid FROM ck_playertimes WHERE steamid = '{}' AND mapname = '{}';"
)
sql_selectMapRecord = "SELECT t1.runtimepro, t1.name, t1.steamid, t1.style, t1.velStartXY, t1.velStartXYZ, t1.velstartZ FROM ck_playertimes t1 JOIN ( SELECT MIN(runtimepro) AS min_runtime, style, mapname FROM ck_playertimes GROUP BY mapname, style ) AS t2 ON t1.runtimepro = t2.min_runtime AND t1.mapname = t2.mapname AND t1.style = t2.style WHERE t1.mapname = '{}'"
sql_selectPersonalAllRecords = "SELECT db1.name, db2.steamid, db2.mapname, db2.runtimepro as overall, db1.steamid, db3.tier FROM ck_playertimes as db2 INNER JOIN ck_playerrank as db1 on db2.steamid = db1.steamid INNER JOIN ck_maptier AS db3 ON db2.mapname = db3.mapname WHERE db2.steamid = '{}' AND db2.style = {} AND db1.style = {} AND db2.runtimepro > -1.0 ORDER BY mapname ASC;"
sql_selectTopSurfers = "SELECT db2.steamid, db1.name, db2.runtimepro as overall, db1.steamid, db2.mapname FROM ck_playertimes as db2 INNER JOIN ck_playerrank as db1 on db2.steamid = db1.steamid WHERE db2.mapname = '{}' AND db1.style = {} AND db2.style = {} AND db2.runtimepro > -1.0 ORDER BY overall ASC LIMIT 50;"
sql_selectTopSurfers2 = "SELECT db2.steamid, db1.name, db2.runtimepro as overall, db1.steamid, db2.mapname FROM ck_playertimes as db2 INNER JOIN ck_playerrank as db1 on db2.steamid = db1.steamid WHERE db2.mapname = '{}' AND db1.style = 0 AND db2.style = 0 AND db2.runtimepro > -1.0 ORDER BY overall ASC LIMIT 100;"
sql_selectPlayerProCount = (
    "SELECT style, count(1) FROM ck_playertimes WHERE mapname = '{}' GROUP BY style;"
)
sql_selectPlayerRankProTime = "SELECT COUNT(*) FROM ck_playertimes WHERE runtimepro <= (SELECT runtimepro FROM ck_playertimes WHERE steamid = '{}' AND mapname = '{}' AND style = 0 AND runtimepro > -1.0) AND mapname = '{}' AND style = 0 AND runtimepro > -1.0;"
sql_selectAllMapTimesinMap = (
    "SELECT runtimepro from ck_playertimes WHERE mapname = '{}';"
)

sql_selectMapRankUnknownWithMap = "SELECT `steamid`, `name`, `mapname`, `runtimepro` FROM `ck_playertimes` WHERE `mapname` = '{}' AND style = 0 ORDER BY `runtimepro` ASC LIMIT {}, 1;"
## ck_spawnlocations
sql_createSpawnLocations = "CREATE TABLE IF NOT EXISTS ck_spawnlocations (mapname VARCHAR(54) NOT NULL, pos_x FLOAT NOT NULL, pos_y FLOAT NOT NULL, pos_z FLOAT NOT NULL, ang_x FLOAT NOT NULL, ang_y FLOAT NOT NULL, ang_z FLOAT NOT NULL,  `vel_x` float NOT NULL DEFAULT '0', `vel_y` float NOT NULL DEFAULT '0', `vel_z` float NOT NULL DEFAULT '0', zonegroup INT(12) DEFAULT 0, stage INT(12) DEFAULT 0, teleside INT(11) DEFAULT 0, PRIMARY KEY(mapname, zonegroup, stage, teleside)) DEFAULT CHARSET=utf8mb4;"
sql_insertSpawnLocations = "INSERT INTO ck_spawnlocations (mapname, pos_x, pos_y, pos_z, ang_x, ang_y, ang_z, vel_x, vel_y, vel_z, zonegroup, teleside) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, {});"
sql_updateSpawnLocations = "UPDATE ck_spawnlocations SET pos_x = '{}', pos_y = '{}', pos_z = '{}', ang_x = '{}', ang_y = '{}', ang_z = '{}', vel_x = '{}', vel_y = '{}', vel_z = '{}' WHERE mapname = '{}' AND zonegroup = {} AND teleside = {};"
sql_selectSpawnLocations = "SELECT mapname, pos_x, pos_y, pos_z, ang_x, ang_y, ang_z, vel_x, vel_y, vel_z, zonegroup, stage, teleside FROM ck_spawnlocations WHERE mapname ='{}';"
sql_deleteSpawnLocations = "DELETE FROM ck_spawnlocations WHERE mapname = '{}' AND zonegroup = {} AND stage = 1 AND teleside = {};"

## ck_vipadmins (should rename this table..)
sql_createVipAdmins = "CREATE TABLE `ck_vipadmins` (`steamid` varchar(32) NOT NULL DEFAULT '', `title` varchar(128) DEFAULT '0', `namecolour` int(11) DEFAULT '0', `textcolour` int(11) NOT NULL DEFAULT '0', `joinmsg` varchar(255) DEFAULT 'none', `pbsound` varchar(256) NOT NULL DEFAULT 'none', `topsound` varchar(256) NOT NULL DEFAULT 'none', `wrsound` varchar(256) NOT NULL DEFAULT 'none', `inuse` int(11) DEFAULT '0', `vip` int(11) DEFAULT '0', `admin` int(11) NOT NULL DEFAULT '0', `zoner` int(11) NOT NULL DEFAULT '0', `active` int(11) NOT NULL DEFAULT '1', PRIMARY KEY (`steamid`), KEY `vip` (`steamid`,`vip`,`admin`,`zoner`)) DEFAULT CHARSET=utf8mb4;"

## ck_wrcps
sql_createWrcps = "CREATE TABLE IF NOT EXISTS `ck_wrcps` (`steamid` varchar(32) NOT NULL DEFAULT '', `name` varchar(64) DEFAULT NULL, `mapname` varchar(32) NOT NULL DEFAULT '', `runtimepro` decimal(12,6) NOT NULL DEFAULT '-1.000000', `velStartXY` smallint(6) NOT NULL DEFAULT 0, `velStartXYZ` smallint(6) NOT NULL DEFAULT 0, `velStartZ` smallint(6) NOT NULL DEFAULT 0, `stage` int(11) NOT NULL, `style` int(11) NOT NULL DEFAULT '0', PRIMARY KEY (`steamid`,`mapname`,`stage`,`style`), KEY `stagerank` (`mapname`,`runtimepro`,`stage`,`style`)) DEFAULT CHARSET=utf8mb4;"


## ck_zones
sql_createZones = "CREATE TABLE `ck_zones` (`mapname` varchar(54) NOT NULL, `zoneid` int(12) NOT NULL DEFAULT '-1', `zonetype` int(12) DEFAULT '-1', `zonetypeid` int(12) DEFAULT '-1', `pointa_x` float DEFAULT '-1', `pointa_y` float DEFAULT '-1', `pointa_z` float DEFAULT '-1', `pointb_x` float DEFAULT '-1', `pointb_y` float DEFAULT '-1', `pointb_z` float DEFAULT '-1', `vis` int(12) DEFAULT '0', `team` int(12) DEFAULT '0', `zonegroup` int(11) NOT NULL DEFAULT '0', `zonename` varchar(128) DEFAULT NULL, `hookname` varchar(128) DEFAULT 'None', `targetname` varchar(128) DEFAULT 'player', `onejumplimit` int(12) NOT NULL DEFAULT '1', `prespeed` int(64) NOT NULL DEFAULT '%.1f', PRIMARY KEY (`mapname`,`zoneid`)) DEFAULT CHARSET=utf8mb4;"
sql_insertZones = "INSERT INTO ck_zones (mapname, zoneid, zonetype, zonetypeid, pointa_x, pointa_y, pointa_z, pointb_x, pointb_y, pointb_z, vis, team, zonegroup, zonename, hookname, targetname, onejumplimit, prespeed) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}','{}','{}',{},{})"
sql_updateZone = "UPDATE ck_zones SET zonetype = '{}', zonetypeid = '{}', pointa_x = '{}', pointa_y ='{}', pointa_z = '{}', pointb_x = '{}', pointb_y = '{}', pointb_z = '{}', vis = '{}', team = '{}', onejumplimit = '{}', prespeed = '{}', hookname = '{}', targetname = '{}', zonegroup = '{}' WHERE zoneid = '{}' AND mapname = '{}'"
sql_selectzoneTypeIds = "SELECT zonetypeid FROM ck_zones WHERE mapname='{}' AND zonetype='{}' AND zonegroup = '{}';"
sql_selectMapZones = "SELECT zoneid, zonetype, zonetypeid, pointa_x, pointa_y, pointa_z, pointb_x, pointb_y, pointb_z, vis, team, zonegroup, zonename, hookname, targetname, onejumplimit, prespeed FROM ck_zones WHERE mapname = '{}' ORDER BY zonetypeid ASC"
sql_selectTotalBonusCount = "SELECT mapname, zoneid, zonetype, zonetypeid, pointa_x, pointa_y, pointa_z, pointb_x, pointb_y, pointb_z, vis, team, zonegroup, zonename FROM ck_zones WHERE zonetype = 3 GROUP BY mapname, zonegroup;"
sql_selectZoneIds = "SELECT mapname, zoneid, zonetype, zonetypeid, pointa_x, pointa_y, pointa_z, pointb_x, pointb_y, pointb_z, vis, team, zonegroup, zonename, hookname, targetname, onejumplimit, prespeed FROM ck_zones WHERE mapname = '{}' ORDER BY zoneid ASC"
sql_selectBonusesInMap = "SELECT mapname, zonegroup, zonename FROM `ck_zones` WHERE mapname LIKE '%c{}%c' AND zonegroup > 0 GROUP BY zonegroup;"
sql_deleteMapZones = "DELETE FROM ck_zones WHERE mapname = '{}'"
sql_deleteZone = "DELETE FROM ck_zones WHERE mapname = '{}' AND zoneid = '{}'"
sql_deleteZonesInGroup = (
    "DELETE FROM ck_zones WHERE mapname = '{}' AND zonegroup = '{}'"
)
sql_setZoneNames = (
    "UPDATE ck_zones SET zonename = '{}' WHERE mapname = '{}' AND zonegroup = '{}';"
)

sql_MainEditQuery = "SELECT steamid, name, {} FROM {} where mapname='{}' and style='{}' {}ORDER BY {} ASC LIMIT 50"
sql_MainDeleteQeury = (
    "DELETE From {} where mapname='{}' and style='{}' and steamid='{}' {}"
)


##ck_prinfo
sql_CreatePrinfo = "CREATE TABLE IF NOT EXISTS ck_prinfo (steamid VARCHAR(32), name VARCHAR(64), mapname VARCHAR(32), runtime decimal(12,6) NOT NULL DEFAULT '-1.000000', zonegroup INT(12) NOT NULL DEFAULT '0', PRtimeinzone decimal(12,6) NOT NULL DEFAULT '-1.000000', PRcomplete FLOAT NOT NULL DEFAULT '0.0', PRattempts FLOAT NOT NULL DEFAULT '0.0', PRstcomplete FLOAT NOT NULL DEFAULT '0.0', PRIMARY KEY(steamid, mapname, zonegroup)) DEFAULT CHARSET=utf8mb4;"

sql_selectPR = "SELECT steamid, name, mapname, zonegroup, PRtimeinzone, PRcomplete, PRattempts, PRstcomplete FROM ck_prinfo WHERE steamid = '{}' AND mapname = '{}' AND zonegroup= '{}';"
sql_insertPR = "INSERT INTO ck_prinfo (steamid, name, mapname, runtime, zonegroup, PRtimeinzone, PRcomplete, PRattempts, PRstcomplete) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');"

sql_selectBonusPR = "SELECT steamid, name, mapname, zonegroup, PRtimeinzone, PRcomplete, PRattempts, PRstcomplete FROM ck_prinfo WHERE steamid = '{}' AND mapname = '{}' AND zonegroup = '{}';"

sql_updatePrinfo = "UPDATE ck_prinfo SET PRtimeinzone = '{}', PRcomplete = '{}', PRattempts = '{}', PRstcomplete = '{}' WHERE steamid = '{}' AND mapname = '{}' AND zonegroup = '{}';"
sql_updatePrinfo_withruntime = "UPDATE ck_prinfo SET PRtimeinzone = '{}', PRcomplete = '{}', PRattempts = '{}', PRstcomplete = '{}', runtime = '{}' WHERE steamid = '{}' AND mapname = '{}' AND zonegroup = '{}';"

sql_clearPRruntime = "UPDATE ck_prinfo SET runtime = '0.0' WHERE steamid = '{}' AND mapname = '{}' AND zonegroup = '{}';"

##ck_replays
sql_createReplays = "CREATE TABLE IF NOT EXISTS ck_replays (mapname VARCHAR(32), cp int(12) NOT NULL DEFAULT '0', frame int(12) NOT NULL DEFAULT '0', style INT(12) NOT NULL DEFAULT '0', PRIMARY KEY(mapname, cp, style)) DEFAULT CHARSET=utf8mb4;"
sql_selectReplayCPTicksAll = "SELECT cp, frame, style FROM ck_replays WHERE mapname = '{}' AND style = '{}' ORDER BY cp ASC;"
sql_insertReplayCPTicks = (
    "INSERT INTO ck_replays (mapname, cp, frame, style) VALUES ('{}', '{}', '{}', '{}')"
)
sql_updateReplayCPTicks = (
    "UPDATE ck_replays SET frame='{}' WHERE mapname='{}' AND cp ='{}' AND style='{}';"
)

##check tables data type
sql_checkDataType = "SELECT DATA_TYPE, NUMERIC_PRECISION, NUMERIC_SCALE FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='{}' AND TABLE_NAME='{}' AND COLUMN_NAME='{}' HAVING DATA_TYPE = 'decimal' AND NUMERIC_PRECISION = 12 AND NUMERIC_SCALE = 6;"
