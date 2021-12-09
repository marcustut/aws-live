from flask import Flask, send_from_directory, send_file, request
from flask_cors import CORS
from flask_expects_json import expects_json
from pymysql import cursors
from os import PathLike, path
import boto3
import pymysql
from config import Config
from error import blueprint as error_blueprint
from handler import handle_create_one_employee, handle_delete_one_employee, handle_fetch_many_employee, handle_fetch_one_employee, handle_update_one_employee
from schema import create_employee_schema, update_employee_schema

bundleExist = path.isfile('./web/dist/index.html')

# initialize the config (setup environment var)
config = Config()

# setup flask
app = Flask(__name__)
cors = CORS(app, origins=["http://localhost:3333"] if config.app_env != "production" else None)

# register blueprints
app.register_blueprint(error_blueprint)

# connect to rds (mysql)
db_conn = pymysql.connect(
    host=config.database_host,
    port=3306,
    user=config.database_user,
    password=config.database_password,
    db=config.database_db,
    charset='utf8mb4',
    cursorclass=cursors.DictCursor
)

@app.route("/", methods=['GET'])
def index_page():
    return send_file('web/dist/index.html')


@app.route("/<path:path>", methods=['GET'])
def send_static_files(path: PathLike):
    return send_from_directory('web/dist', path) if bundleExist else 'No html files'


@app.route("/employee/<string:username>", methods=['GET', 'PUT', 'DELETE'])
@expects_json(update_employee_schema, ignore_for=['GET', 'DELETE'])
def employee(username: str):
    if request.method == "GET":
        return handle_fetch_one_employee(db_conn, username)
    elif request.method == "DELETE":
        return handle_delete_one_employee(db_conn, username)
    else:
        return handle_update_one_employee(db_conn, username, request.json, config.s3_bucket_id)


@app.route("/employee", methods=['POST'])
@expects_json(create_employee_schema)
def create_employee():
    return handle_create_one_employee(db_conn, request.json, config.s3_bucket_id)


@app.route("/employees", methods=['GET'])
def employees():
    return handle_fetch_many_employee(db_conn, request.args)


if __name__ == '__main__':
    # TODO: Check whether web/dist folder exists

    debug = False if config.app_env == "production" else True
    app.run(host='0.0.0.0', port=5000, debug=debug)
