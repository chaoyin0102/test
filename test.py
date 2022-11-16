#coding=utf-8
import json
import mysql.connector

# open JSON file
json_data = open("/data/taipei-attractions.json").read()
raw_data = json.loads(json_data)
data = raw_data["result"]["results"]

# make the connection with mysql
trip_db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "**********",
    database = "new_db"
)
cursor = trip_db.cursor()

# filter images
def filter_image(arr):
    new_images = []
    for i in range(len(arr)):
        if arr[i][-3:] == "jpg" or "JPG" or "png" or "PNG":
            new_images.append(arr[i])
        else:
            continue
    return new_images

# get attraction
for attr in data:
    id = attr["_id"]
    name = attr["name"]
    category = attr["CAT"]
    transport = attr["direction"]
    description = attr["description"]
    address = attr["address"]
    mrt = attr["MRT"]
    latitude = attr["latitude"]
    longitude = attr["longitude"]
    images = attr["file"].split("https")

    # 把 https 加回圖片
    images = ["https" + i for i in images][1:]
    new_image = "".join(filter_image(images))

    # insert data into mysql
    cursor.execute("INSERT INTO attactions (id, name, catagory, transport, description, address, mrt, latitude, longitude, images) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id,name,category,description,address[0],transport[0],mrt[0],float(latitude[0]),float(longitude[0]), new_image))
        
trip_db.commit()
trip_db.close()
    


# _id ID
# name 景點名稱
# direction 交通方式
# description 景點描述
# CAT 分類
# date 日期
# address 地址
# file 圖片
# MRT 捷運站
# latitude 緯度
# longitude 經度
