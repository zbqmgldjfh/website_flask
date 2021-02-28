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
import math
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

@app.route("/list")
def lists():
    # 페이지 값 (값이 없는 경우 기본값 1)
    page = request.args.get("page", 1, type=int)
    # 한페이지 당 몇개의 개시물을 출력할지
    limit = request.args.get("limit", 10, type=int)

    search = request.args.get("search", -1, type=int)
    keyword = request.args.get("keyword", type=str)

    #최종적으로 완성된 쿼리를 만들 변수 
    query = {}
    search_list = []

    if search == 0:
        search_list.append({"title": {"$regex": keyword}})
    elif search == 1:
        search_list.append({"contents": {"$regex": keyword}})
    elif search == 2:
        search_list.append({"title": {"$regex": keyword}})
        search_list.append({"contents": {"$regex": keyword}})
    elif search == 3:
        search_list.append({"name": {"$regex": keyword}})

    if len(search_list) > 0:
        query = {"$or": search_list}

    print(query)

    board = mongo.db.board
    datas = board.find({}).skip((page-1) * limit).limit(limit)

    #게시물의 총 갯수
    tot_count = board.find(query).count()
    #마지막 페이지의 수 구하기
    last_page_num = math.ceil(tot_count / limit)
    #페이지 블럭을 5개씩 표기
    block_size = 5
    # 현재 블럭의 위치
    block_num = int((page - 1) / block_size) 
    # 블럭 시작위치
    block_start = int((block_size * block_num) + 1)
    # 블럭 끝 위치
    block_last = math.ceil(block_start + (block_size - 1))

    return render_template("list.html", datas=datas, limit=limit, page=page, 
    block_start=block_start, block_last=block_last, last_page_num=last_page_num,
    search=search, keyword=keyword)

@app.route("/view/<idx>")
def board_view(idx):
    #idx = request.args.get("idx")
    if idx is not None:
        page = request.args.get("page")
        search = request.args.get("search")
        keyword = request.args.get("keyword")
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

            return render_template("view.html", result = result, page=page, search=search, keyword=keyword)
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
