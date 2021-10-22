import json
import os
import uuid

from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
cors = CORS(app)
import sqlite3 as sql
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def hello_world():
    data = parse_data()
    dlist = {i: data[i] for i in range(0, len(data))}
    return jsonify(dlist)

def parse_data(username, filepath):
    try :
        file = open(filepath, 'r')
        distibution = [0] * 10
        count = 0
        rows = []
        while True:
            line = file.readline()
            if not line:
                break

            splitted = line.split()

            count += 1
            l = len(splitted)
            s = splitted[: l - 4]
            listToStr = ' '.join([str(elem) for elem in s])

            rows.append([listToStr, splitted[l - 4], splitted[l - 3], splitted[l - 2], splitted[l - 1]])

            value = splitted[l - 4]
            if value.isnumeric():
                distibution[int(value[0])] += 1


        dlist = {i: distibution[i] for i in range(0, len(distibution))}
        distibution_str = json.dumps(dlist)
    finally:
        file.close()

    with sql.connect("database.db") as con:
        cur = con.cursor()

        cur.execute("INSERT INTO uploads (user, distibution) VALUES(?,?)", (username, distibution_str,))
        upload_id = cur.lastrowid
        details = map(lambda item: tuple(item + [upload_id]), rows)


        cur.executemany(
            "INSERT INTO upload_details ( 'name', 'population', 'c3', 'c4', 'c5', 'upload_id') VALUES(?, ?, ?, ?, ?, ?)",
            list(details))

        con.commit()

    return distibution


@app.route('/uploads', methods=['GET', 'POST'])
def uploads():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        username = request.form['user']
        if uploaded_file.filename != '':
            filename = str(uuid.uuid4()) + secure_filename(uploaded_file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print('path', path)
            uploaded_file.save(path)
            parse_data(username, path)
        return 'ok'
    else:
        con = sql.connect("database.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("select * from uploads order by id desc")
        rows = cur.fetchall()
        print(type(rows))
        return json.dumps([dict(ix) for ix in rows])

@app.route('/uploads/<upload_id>', methods=['GET'])
def upload_info(upload_id=0):
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from uploads where id=?", (upload_id,))
    data = cur.fetchone()
    if data is None:
        return json.dumps('no data found')
    return json.dumps( dict(data))

if __name__ == '__main__':
    app.run()

@app.route('/uploads/<upload_id>/details', methods=['GET'])
def upload_details(upload_id=0):
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from uploads where id=?", (upload_id,))
    data = cur.fetchone()
    if data is None:
        return json.dumps('no data found'), 404

    cur.execute("select * from upload_details where upload_id=?", (upload_id,))
    rows = cur.fetchall()
    result = [dict(ix) for ix in rows]
    return json.dumps(result)

if __name__ == '__main__':
    app.run()