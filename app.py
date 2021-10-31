from elasticsearch import Elasticsearch
from flask import Flask
from flask import flash, render_template, request, redirect, jsonify
import re
from Search import search

es = Elasticsearch([{'host': 'localhost', 'port':9200}])
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        results = search(request.form['nm'])
        return render_template('index.html', results = results)
    return render_template('index.html', results = '')

if __name__ == "__main__":
    app.run(debug=True)