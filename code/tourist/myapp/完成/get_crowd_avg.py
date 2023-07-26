import psycopg2
import os
import csv
import json
from sqltool import Postgres
tool = Postgres()

def get_avg():
    total_avg = []
    for week in range(1,8):
        get_avg = tool.read(f"SELECT crowd FROM myapp_crowd_opening WHERE week = '{week}' ;")
        # print(get_avg)
        avg_list = [0]*24
        print('初始',avg_list)
        count = 0
        for avg in get_avg:
            # print(avg[0])
            if avg[0] != []:
                for i in range(24):
                    avg_list[i] += avg[0][i]
                count+=1
        avg_list = [int(round(x/count,0)) for x in avg_list]
        total_avg.append(avg_list)
    return total_avg



avg_list = get_avg()
for a in avg_list:
    print(a)
# input_avg(avg_list)