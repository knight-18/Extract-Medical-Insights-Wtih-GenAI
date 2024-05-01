from flask import Flask, jsonify
import subprocess
import summarization_lib as summarize
from flask import request
from flask_cors import CORS, cross_origin
from waitress import serve


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/summarize', methods=['POST'])
@cross_origin()
def get_summary():
    req_body = request.get_json()
    print(req_body)
    response_content = summarize.get_summary(return_intermediate_steps=False) #call the model through the supporting library
    print(response_content)
    return jsonify({'response': response_content})


@app.route('/cal', methods=['GET'])
def get_cal():
    result = subprocess.check_output(['cal']).decode('utf-8')
    return jsonify({'calendar': result.strip()})

#route to serve a get request with apploication/json as content type
@app.route('/json', methods=['GET'])
def get_json():
    return jsonify({'message': 'Hello World'})

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8080)
