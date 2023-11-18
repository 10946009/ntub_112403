from .viewsConst import WEATHER_API_KEY
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
DATAID = "F_D0047_063"

# 发送GET请求
def get_weather_data(address,year,mouth,day,nowtime):#地址、年、月、日、時(分鐘單位)
    url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-063?Authorization={WEATHER_API_KEY}&elementName="
    weather_data = {}
    mouth = str(mouth).zfill(2) #補0
    day = str(day).zfill(2) #補0
    nowtime =(nowtime // 60) % 24
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        for d in data['records']['locations'][0]['location']: #抓區域
            if d['locationName'] in address: #同區域
                for item in d['weatherElement']:
                    for time in item['time']: #抓項目
                        start_day,start_time = time['startTime'].split(' ')
                        end_day,end_time = time['endTime'].split(' ')
                        if f"{year}-{mouth}-{day}" in start_day and nowtime >= int(start_time[:2]):
                            weather_data[item['description']] = time['elementValue'][0]['value']
                        
                        if f"{year}-{mouth}-{day}" in end_day and nowtime < int(end_time[:2]):
                            weather_data[item['description']] = time['elementValue'][0]['value']
    else:
        return print("暫無資料")
    for k,v in weather_data.items():
        if v == " ":
            weather_data[k] = "暫無資料"
    # print("------------------------------------------------------------------")
    # print(weather_data["天氣預報綜合描述"])
    try:
        return weather_data["天氣預報綜合描述"]
    except:
        return "暫無資料"
# print(get_weather_data("南港區",2023,11,7,1080))
