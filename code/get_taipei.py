import csv
with open('臺北市區路段資料.csv',newline='',encoding='utf-8')as csvfile:
    sp = list(csv.reader(csvfile))[1:]
    list(sp)
    for i in sp:
        print(i)