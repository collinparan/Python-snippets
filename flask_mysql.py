from flask import Flask, request, redirect, Response, jsonify
from flasgger import Swagger
import mysql.connector

conn = mysql.connector.connect(host='127.0.0.1', port=3306, database='db', user='user', password='password')

app = Flask(__name__)
Swagger(app)

@app.route('/api', methods=['POST'])
def index():
    """
    The Flask MySQL API
    Call this api to get data from a database
    ---
    tags:
      - flask_mysql
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - sql_statement
          properties:
            sql_statement:
              type: string
              description: The SQL query.
              default: SELECT * FROM db.fruit
    responses:
      500:
        description: API query Error!
      200:
        description: Returned data
    """
    statement = request.json['sql_statement']
    cursor = conn.cursor()
    cursor.execute(statement)
    rv = cursor.fetchall()
    return jsonify(rv)
    cursor.close()
    conn.close()

@app.route("/", methods=['GET'])
def redir():
    return redirect("/apidocs")

if __name__ == "__main__":
    app.run(debug=True, port=80)
