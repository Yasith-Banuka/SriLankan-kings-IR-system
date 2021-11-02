from elasticsearch import Elasticsearch
from flask import Flask
from flask import flash, render_template, request, redirect, jsonify
import requests
import re
import json

from werkzeug.wrappers import Response
from Search import search, autocomplete

es = Elasticsearch([{'host': 'localhost', 'port':9200}])
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        results = search(request.form['nm'])
        return render_template('index.html', results = results)
    return render_template('index.html', results = '')

@app.route('/pipe', methods=["GET", "POST"])
def pipe():
    data = request.form.get("data")
    payload = {}
    headers= {}
    url = "http://127.0.0.1:4000/autocomplete?query="+str(data)
    response = autocomplete(str(data))
    return json.dumps(response)

if __name__ == "__main__":
    app.run(debug=True)