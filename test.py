from flask import *
from mysql.connector import pooling

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

# connect with database by pooling
connection_pool = pooling.MySQLConnectionPool(
    pool_name="connection_pool",
    pool_size=5,
    pool_reset_session=True,
    host="localhost",
    user="root",
    password="******",
    database="new_db"
)

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")

# API of attraction
# 1-2-1
@app.route("/api/attractions")
def attractions():
    try:
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor(dictionary=True)

        page = request.args.get("page", type=int)
        keyword = request.args.get("keyword")

        # keyword
        if keyword:
            cursor.execute(
                f'SELECT * FROM `attractions2` WHERE `category` LIKE "{keyword}" or `name` LIKE "%{keyword}%"'
            )
            count = cursor.fetchall()
            if len(count) == 0:
                return jsonify({
                    "error" : True,
                    "message" : "查無相關景點",  
                })
            
            else:
                if len(count) - page * 12 > 12:
                    nextPage = page +1
                else:
                    nextPage = None

                dataList = []
                for i in range(len(count) - page*12):
                    dataList.append({"id": count[i]["id"],
                                    "name": count[i]["name"],
                                     "category": count[i]["category"],
                                     "description": count[i]["description"],
                                     "address": count[i]["address"],
                                     "transport": count[i]["transport"],
                                     "mrt": count[i]["mrt"],
                                     "lat": count[i]["lat"],
                                     "lng": count[i]["lng"],
                                     "images": count[i]["images"].split(",")
                                     })
                    
                cursor.close()
                connection_object.close()

            return jsonify({
                    "nextPage": nextPage,
                    "data": dataList
                })

        # without keyword
        else:        
            cursor.execute(
                f'SELECT * FROM attractions2 LIMIT {page*12}, 13'
            )
            items = cursor.fetchall()

            if len(items) == 0:
                return jsonify({
                    "error": True,
                    "message": "查無相關景點"
                })

            else:
                if len(items) == 13:
                    nextPage = page + 1
                    items = items[:-1]
                else:
                    nextPage = None

            itemList = []
            for j in range(len(items)):
                itemList.append({
                    "id": items[j]["id"],
                    "name": items[j]["name"],
                    "category": items[j]["category"],
                    "description": items[j]["description"],
                    "address": items[j]["address"],
                    "transport": items[j]["transport"],
                    "mrt": items[j]["mrt"],
                    "lat": items[j]["lat"],
                    "lng": items[j]["lng"],
                    "images": items[j]["images"].split(",")
                }),
            
            return jsonify({
                "nextPage": nextPage,
                "data":itemList
            })
    except 500:
        return jsonify({
            "error": True,
            "message": "伺服器內部錯誤"
        }), 500
    finally:
        cursor.close()
        connection_object.close()


# 1-2-2
@app.route("/api/attraction/<attractionId>")
def attractionId(attractionId):
    try:
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor(dictionary = True)

        cursor.execute(
            "SELECT * FROM `attractions2` WHERE `id` = %s" % attractionId
        )
        data = cursor.fetchone()


        # 景點編號輸入正確
        if data !=None:
            # data= json.loads(data)
            return jsonify({
                "data": {
                    "id": data["id"],
                    "name": data["name"],
                    "category": data["category"],
                    "description": data["description"],
                    "address": data["address"],
                    "transport": data["transport"],
                    "mrt": data["mrt"],
                    "lat": data["lat"],
                    "lng": data["lng"],
                    "images": data["images"].split(",")
                }
            })
        else:
            return jsonify({
                 "error" : True,
                 "message" : "景點編號不正確"
            }), 400

    except 500:
        return jsonify({
            "error": True,
            "message": "伺服器內部錯誤"
        }), 500

    finally:
        cursor.close()
        connection_object.close()

# 1-2-3
@app.route("/api/categories")
def categories():
    try:
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor(dictionary=True)

        cursor.execute("SELECT DISTINCT `category` FROM `attractions`")
        categories = cursor.fetchall()
        print(categories)

        categoriesList = []
        for data in categories:
            categoriesList.append(data["category"])

        return jsonify({"data": categoriesList})

    except 500:
        return jsonify({
            "error": True,
            "message": "伺服器內部錯誤"
        }), 500

    finally:
        cursor.close()
        connection_object.close()

@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

if __name__ == "__main__":
	app.run(port=3000, debug=True)
