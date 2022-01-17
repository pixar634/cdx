import os
import sqlite3
from sqlite3 import Error
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("codex.db")
    except sqlite3.error as e:
        print(e)
    return conn

# fetch all users
@app.route("/users", methods=["GET"])
@cross_origin()
def all_users():
    conn = db_connection()
    cursor = conn.cursor()
    users = None

    cursor = conn.execute("select * from users")
    users = [
        dict(id=row[0], email=row[1], name=row[2])
        for row in cursor.fetchall()
    ]

    if users is not None:
        return jsonify(users), 200
    else:
        return "Something is wrong", 404


# fetch all projects
@app.route("/projects", methods=["GET"])
@cross_origin()
def all_projects():
    conn = db_connection()
    cursor = conn.cursor()
    projects = None

    cursor = conn.execute("select * from projects")
    projects = [
        dict(id=row[0], project_name=row[1], project_description=row[2],
             project_notes=row[3], project_attachment=row[4], user_access_id=row[5])
        for row in cursor.fetchall()
    ]

    if projects is not None:
        return jsonify(projects), 200
    else:
        return "Something is wrong", 404


# add new project
@app.route("/postprojects", methods=["POST"])
@cross_origin()
def post_projects():
    conn = db_connection()
    cursor = conn.cursor()
    content = request.json
    project_name = content['project_name']
    project_description = content['project_description']
    project_notes = content['project_notes']
    user_access_id = content['user_access_id']
    # project_attachments = request.form['project_attachments']
    sql = """insert into projects (project_name , project_description , project_notes,user_access_id)
            
        values (?,?,?,?)"""
    cursor = cursor.execute(
        sql, (project_name, project_description, project_notes, user_access_id))
    conn.commit()
    return "Successful", 200


if __name__ == "__main__":
    app.run(debug=true)
