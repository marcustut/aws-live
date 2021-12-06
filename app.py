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

# setup flask
app = Flask(__name__)
cors = CORS(app)

# register blueprints
app.register_blueprint(error_blueprint)

# initialize the config (setup environment var)
config = Config()

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
        return handle_update_one_employee(db_conn, username, request.json)


@app.route("/employee", methods=['POST'])
@expects_json(create_employee_schema)
def create_employee():
    return handle_create_one_employee(db_conn, request.json)


@app.route("/employees", methods=['GET'])
def employees():
    return handle_fetch_many_employee(db_conn, request.args)

# @app.route("/addemp", methods=['POST'])
# def AddEmp():
#     emp_id = request.form['emp_id']
#     first_name = request.form['first_name']
#     last_name = request.form['last_name']
#     pri_skill = request.form['pri_skill']
#     location = request.form['location']
#     emp_image_file = request.files['emp_image_file']

#     insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
#     cursor = db_conn.cursor()

#     if emp_image_file.filename == "":
#         return "Please select a file"

#     try:

#         cursor.execute(insert_sql, (emp_id, first_name, last_name, pri_skill, location))
#         db_conn.commit()
#         emp_name = "" + first_name + " " + last_name
#         # Uplaod image file in S3 #
#         emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
#         s3 = boto3.resource('s3')

#         try:
#             print("Data inserted in MySQL RDS... uploading image to S3...")
#             s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
#             bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
#             s3_location = (bucket_location['LocationConstraint'])

#             if s3_location is None:
#                 s3_location = ''
#             else:
#                 s3_location = '-' + s3_location

#             object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
#                 s3_location,
#                 custombucket,
#                 emp_image_file_name_in_s3)

#         except Exception as e:
#             return str(e)

#     finally:
#         cursor.close()

#     print("all modification done...")
#     return render_template('AddEmpOutput.html', name=emp_name)


if __name__ == '__main__':
    # TODO: Check whether web/dist folder exists

    debug = False if config.app_env == "production" else True
    app.run(host='0.0.0.0', port=5000, debug=debug)
