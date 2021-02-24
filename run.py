from flask import Flask
from flask import request
from flask import render_template
from flask_pymongo import PyMongo
from datetime import datetime
from bson.objectid import ObjectId
from flask import abort
from flask import redirect
from flask import url_for
import time

app = Flask(__name__)  #flask 인스턴스 생성
app.config["MONGO_URI"] = "mongodb://localhost:27017/myweb"
mongo = PyMongo(app)

@app.template_filter("formatdatetime")
def format_datetime(value):
    if value is None:
        return ""

    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    value = datetime.fromtimestamp((int(value) / 1000)) + offset
    return value.strftime("%Y-%m-%d %H:%M:%S")

@app.route("/view/<idx>")
def board_view(idx):
    #idx = request.args.get("idx")
    if idx is not None:
        board = mongo.db.board
        data = board.find_one({"_id": ObjectId(idx)})

        if data is not None:
            result = {
                "id": data.get("_id"),
                "name": data.get("name"),
                "title": data.get("title"),
                "contents": data.get("contents"),
                "pubdata": data.get("pubdata"),
                "view": data.get("view")
            }

            return render_template("view.html", result = result)
    return abort(404)

@app.route("/write", methods=["GET", "POST"])
def board_write():
    if request.method == "POST":
        name = request.form.get("name")
        title = request.form.get("title")
        contents = request.form.get("contents")
        current_utc_time = round(datetime.utcnow().timestamp() * 1000)

        board = mongo.db.board
        post = {
            "name": name,
            "title": title,
            "contents": contents,
            "pubdata": current_utc_time,
            "view": 0,
        }

        x = board.insert_one(post)
        print(x.inserted_id)
        return redirect(url_for("board_view", idx = x.inserted_id))
    else:
        return render_template("write.html")

if __name__ == "__main__":
    app.run(debug=True)
