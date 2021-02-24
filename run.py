from flask import Flask
from flask import request
from flask import render_template
from flask_pymongo import PyMongo
from datetime import datetime

app = Flask(__name__)  #flask 인스턴스 생성
app.config["MONGO_URI"] = "mongodb://localhost:27017/myweb"
mongo = PyMongo(app)

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

        board.insert_one(post)

        return ""
    else:
        return render_template("write.html")

if __name__ == "__main__":
    app.run(debug=True)
