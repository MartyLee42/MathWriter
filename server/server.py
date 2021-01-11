from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import pymysql
import json

app = Flask(__name__)

cors = CORS(app)

@app.route("/api/conspect", methods=['POST', 'GET','DELETE'])
@cross_origin()
def conspect():
    con = pymysql.connect('localhost', 'root','rootroot', "MathWriter")
    cur = con.cursor()

    if request.method == "POST":
        title = request.json["title"]
        prev_title = None
        if "prev_title" in request.json:
            prev_title = request.json["prev_title"]

        if prev_title:
            res = cur.execute("""INSERT INTO conspect (title, prev_title) VALUES (%s, %s)""", (title, prev_title))
            id = str(con.insert_id())
            con.commit()
        else:
            res = cur.execute("""INSERT INTO conspect (title) VALUES (%s)""", title)
            id = str(con.insert_id())
            con.commit()
        return """{"status" : "ok", "id" : """ + id +"}"

    if request.method == "DELETE":
        id = request.json["id"]
        res = cur.execute("""DELETE FROM conspect where conspect_id = %s""", id)
        con.commit()
        print(res)
        return """{"status" : "ok"}"""

    if request.method == "GET":
        res = cur.execute("""SELECT * FROM conspect""")
        res = cur.fetchall()
        used = {x[0]: 0 for x in res}
        name_to_id = {x[1]: x[0] for x in res if x[1]}
        id_to_name = {name_to_id[y]:y for y in name_to_id}
        tree = {x[0]: [] for x in res}

        first_level = [x[0] for x in res if x[2] is None]

        for x in res :
            if x[2]:
                tree[name_to_id[x[2]]].append(x[0])


        return {"tree" : tree, "id_to_name": id_to_name, "first_level" : first_level}




@app.route("/api/conspect/<conspect_id>/texts", methods=['POST', 'GET'])
@cross_origin()
def conspect_texts(conspect_id):
    con = pymysql.connect('localhost', 'root','rootroot', "MathWriter")
    cur = con.cursor()

    if request.method == "POST":
        text = request.json["text"]
        print(text)

        cur.execute("""
                INSERT INTO conspect_text(conspect_id, content) VALUES(%s, %s);
            """, (conspect_id, text))
        id = str(con.insert_id())
        print(id)
        con.commit()
        return """{"status" : "ok", "id" : """ + id +"}"

    if request.method == "GET":
        cur.execute("""SELECT * FROM conspect_text WHERE conspect_id = %s ORDER BY text_id""", conspect_id)
        conspect_texts = cur.fetchall()
        print(conspect_texts)

        res = {"texts" : [{"text": x[2], "id" : x[0]} for x in conspect_texts]}

        return res


@app.route("/api/conspect/<conspect_id>/texts/<text_id>", methods=['POST', 'GET'])
@cross_origin()
def conspect_texts_by_id(conspect_id, text_id):
    con = pymysql.connect('localhost', 'root','rootroot', "MathWriter")
    cur = con.cursor()

    if request.method == "POST":
        text = request.json["text"]

        cur.execute("""
                UPDATE conspect_text SET content = %s WHERE conspect_id = %s AND text_id = %s;
            """, (text, conspect_id, text_id))
        con.commit()
        return """{"status" : "ok"}"""

    if request.method == "GET":
        cur.execute("""SELECT * FROM conspect_text WHERE text_id = %s""", text_id)
        conspect_texts = cur.fetchone()
        print(conspect_texts)

        res = {"texts" : {"text": conspect_texts[2], "id" : conspect_texts[0]}}

        return res


def dfs(v, used, tree):
    pass


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
