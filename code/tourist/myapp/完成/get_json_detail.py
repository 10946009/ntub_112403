import requests
from bs4 import BeautifulSoup
import psycopg2
import os
import csv
import json
from sqltool import Postgres
import time
import re
tool = Postgres()

all_attractions_detail = tool.read("SELECT place_id,detail FROM myapp_attractions;")
all_attractions_detail = [all_attractions_detail[x][0] for x in range(len(all_attractions_detail)) if all_attractions_detail[x][1] == '']
with open("臺北市區路段資料.csv", newline="", encoding="utf-8") as csvfile:
    address_list = list(csv.reader(csvfile))
    list(address_list)
    for address in address_list[1:]:
        # try:
        with open(f"{address[0]}{address[1]}景點營業時間.json", encoding="utf-8") as file:
            data_opening_phone = json.load(file)
            for num in range(len(data_opening_phone)):
            #     print(data_opening_phone["results"][num]["place_id"])
                try:
                    wek = data_opening_phone[num]['result']['editorial_summary']['overview']
                    placeid = data_opening_phone[num]['result']['place_id']
                    
                    if placeid in all_attractions_detail:
                        print(placeid,wek)
                        data = tool.read(
                            f"SELECT * FROM myapp_attractions WHERE place_id ILIKE '{placeid}';"
                        )
                        sql =f"UPDATE myapp_attractions SET detail = %s WHERE place_id = %s;"
                        tool.update(sql,(wek,placeid))
                except:
                    continue

# for placeid in all_attractions_placeid:


