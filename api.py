
from flask import Flask, render_template, url_for, jsonify, request
import sqlite3

def conn_db():
    return sqlite3.connect("GEO_DB.db")

app = Flask(__name__)

@app.route('/by_id', methods=["GET"])
def get_by_id():
    id = request.args.get("pid")
    conn = conn_db()
    c = conn.cursor()
    c.execute("SELECT * FROM citizens WHERE personalid = ?", (id,))
    results = c.fetchall()
    columns = [description[0] for description in c.description]
    data_list = [dict(zip(columns, i)) for i in results]
    conn.close()
    return jsonify({f"Found {len(data_list)} results": data_list})

@app.route('/by_fullname', methods=["GET"])
def get_by_fullname():
    name = request.args.get("fname")
    lastname = request.args.get("lname")
    conn = conn_db()
    c = conn.cursor()
    c.execute("SELECT * FROM citizens WHERE firstname = ? AND lastname = ?", (name,lastname))
    results = c.fetchall()
    columns = [description[0] for description in c.description]
    data_list = [dict(zip(columns, i)) for i in results]
    conn.close()
    return jsonify({f"Found {len(data_list)} results": data_list})

@app.route("/filter", methods=["GET"])
def full_filter():
    p_id = request.args.get("pid")
    firstname = request.args.get("fname")
    lastname = request.args.get("lname")
    fathername = request.args.get("dname")
    region = request.args.get("region")
    birthday = request.args.get("bday")

    query = "SELECT * FROM citizens WHERE id > 0"
    if p_id:
        query += f" AND personalid = '{p_id}'"

    if firstname:
        query += f" AND firstname = '{firstname}'"

    if lastname:
        query += f" AND lastname = '{lastname}'"

    if fathername:
        query += f" AND fathername = '{fathername}'"
        
    if region:
        query += f" AND region = '{region}'"
        
    if birthday:
        query += f" AND birthday = '{birthday}'"
        

    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    data_list = [dict(zip(columns, i)) for i in results]
    return jsonify({f"Found {len(data_list)} results": data_list})

if __name__ == '__main__':
    app.run(debug=True,port=6969)

