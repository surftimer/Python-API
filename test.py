from sql import *

# Test
t = selectQuery(
    """SELECT 
	mapname
    FROM surftimer.ck_maptier;"""
)

print(f"Length: {len(t)}")
