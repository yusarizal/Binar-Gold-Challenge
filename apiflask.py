from flask import Flask, jsonify, request
from flasgger import Swagger, LazyString, LazyJSONEncoder 
from flasgger import swag_from
import re

#Flask and Swagger Initialization 
app = Flask(__name__)

app.json_encoder = LazyJSONEncoder
swagger_template = dict(
info = {
    'title': LazyString(lambda:'API Documentation for Data Processing and Modeling'),
    'version': LazyString(lambda:'1.0.0'),
    'description': LazyString(lambda:'Dokumentasi API untuk Data Processing dan Modeling'),
    }, 
    host = LazyString(lambda: request.host)    
)
swagger_config = {
    "headers": [],
    "specs":[
        {
            "endpoint":'docs',
            "route":'/docs.json',
        }
    ],
    "static_url_path":"/flasgger_static",
    "swagger_ui": True,
    "specs_route":"/docs"
}
swagger = Swagger(app,template=swagger_template, 
                config=swagger_config)


#HOMEPAGE
@swag_from("docs/hello.yml", methods = ['GET'])
@app.route('/', methods = ['GET'])
def hello_world(): 
    json_response = {
        'status code': 200,
        'description' : 'Home/Beranda',
        'data': 'Tweet and Word Cleaning',
    }
    response_data = jsonify(json_response)
    return response_data

#CHECKING DATABASES
@swag_from("docs/check_database.yml", methods = ['GET'])
@app.route("/databases", methods = ['GET'])
def database_check():
    query = "select * from databases"
    select_tweet = c.execute(query)
    tweet = [
        dict(id=row[0], original=row[1], cleansed=row[2])
        for row in select_tweet.fetchall()
    ]
    

    json_response = {
        'status code': 200,
        'description' : 'Home',
        'data': tweet,
    }
    response_data = jsonify(json_response)
    return response_data

#INPUT TEXT
@swag_from("docs/text_process.yml", methods = ['POST'])
@app.route('/text-clean', methods = ['POST'])
def text_cleaning():
    text = request.form.get("text")
    cleansed = textprep(text)
    query = "insert into databases (original,cleansed) values (? , ?)"
    values = (text,cleansed)
    c.execute(query,values)
    db.commit()

    json_response = {
        'status code': 200,
        'description': 'API text cleaning',
        'data': cleansed,
    }
    response_data = jsonify(json_response)
    return response_data

#INPUT CSV
@swag_from("docs/input_csv.yml",methods=['POST'])
@app.route("/csv-clean", methods=['POST'])
def csv_cleaning():
    file = request.files["file"]
    try:
        df = pd.read_csv(file, encoding='iso-8859-1')
    except:
        df = pd.read_csv(file, encoding='utf-8')
    col_1 = df.iloc[:,0]
    for text in col_1:
        bersih = textprep(text)
        query = "insert into databases (original,cleansed) values(?,?)"
        values = (text, bersih)
        c.execute(query, values)
        db.commit()
    json_response = {
        'status code': 200,
        'description': 'API text cleaning',
        'data': 'File successfully uploaded',
    }
    response_data = jsonify(json_response)
    return response_data
    
##ACCESSING TEXT



if __name__ == '__main__':
    app.run()    