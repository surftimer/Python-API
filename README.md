![Downloads](https://img.shields.io/github/downloads/tslashd/st-api/total?style=flat-square) ![Last commit](https://img.shields.io/github/last-commit/tslashd/st-api?style=flat-square) ![Open issues](https://img.shields.io/github/issues/tslashd/st-api?style=flat-square) ![Closed issues](https://img.shields.io/github/issues-closed/tslashd/st-api?style=flat-square) ![Size](https://img.shields.io/github/repo-size/tslashd/st-api?style=flat-square) 

**Use this at your own risk!**

# SurfTimer FastAPI
This is a project to build an API for SurfTimer plugin and implement functionality to use it instead of MySQL connection.
Idea for this came about when I did some refactoring for `SurfTimer-Mapchooser` to get it's data from an API instead of MySQL and the processing time *drastically* decreased, so why not try it for `SurfTimer` itself?

There is still quite a bit of queries to be transferred from all `*.sp` files in `SurfTimer` source code to the main `queries.sp` and to switch using them as variables instead of straight queries in `Format(...);`.

Everyone is welcome to **PR** code if they want to help out. I cannot promise that this will be 100% usable at any point in time, but you can give it go using my `SurfTimer` fork for it [here](https://github.com/tslashd/SurfTimer/tree/py-fastapi-integration)


## Pre-Requisites
- Install dependancies `pip install -r requirements.txt`
- Copy `config.json.example` to `config.json` and populate
- Create `requests.json` and `denied.json` files
- Run it `uvicorn main:app --port <YOUR_PORT_HERE> --host 0.0.0.0 --reload`
- Check it out at `https://<yourDomain>.com/docs`


### To Do
- [ ] ck_announcements
- [x] ck_bonus
- [x] ck_checkpoints
- [x] ck_latestrecords
- [x] ck_maptier
- [x] ck_playeroptions2
- [x] ck_playerrank
- [x] ck_playertemp - Partially
- [ ] ck_playertimes
- [x] ck_spawnlocations - ST Code
- [ ] ck_vipadmins
- [ ] ck_wrcps
- [x] ck_zones - ST Code
- [x] ck_prinfo - ST Code
- [x] ck_replays - ST Code
- [ ] check tables data type
- [ ] ...? 